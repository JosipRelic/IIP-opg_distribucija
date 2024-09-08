from django.http import HttpResponse, JsonResponse
import simplejson as json
from django.shortcuts import render, redirect
from e_trznica.models import Kosarica
from e_trznica.context_processors import dohvati_iznose_u_kosarici
from .forms import FormaNarudzbe
from .models import NaruceniProizvodi, Narudzba, Placanje
from .utils import generiraj_broj_narudzbe
from korisnicki_racuni.utils import posalji_obavijest_opg_verifikacija
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='prijava')
def posalji_narudzbu(request):
    proizvodi_u_kosarici = Kosarica.objects.filter(korisnik=request.user).order_by('kreirano')
    broj_proizvoda_u_kosarici = proizvodi_u_kosarici.count()
    if broj_proizvoda_u_kosarici <= 0:
        return redirect('e_trznica')
    
    ukupna_cijena_proizvoda = dohvati_iznose_u_kosarici(request)['ukupna_cijena_proizvoda']
    pdv = dohvati_iznose_u_kosarici(request)['pdv']
    ukupan_iznos = dohvati_iznose_u_kosarici(request)['ukupan_iznos']
    pdv_dict = dohvati_iznose_u_kosarici(request)['pdv_dict']

    if request.method == 'POST':
        forma_narudzbe = FormaNarudzbe(request.POST)
        
        if forma_narudzbe.is_valid():
            narudzba = Narudzba()
            narudzba.ime = forma_narudzbe.cleaned_data['ime']
            narudzba.prezime = forma_narudzbe.cleaned_data['prezime']
            narudzba.broj_telefona = forma_narudzbe.cleaned_data['broj_telefona']
            narudzba.email = forma_narudzbe.cleaned_data['email']
            narudzba.adresa = forma_narudzbe.cleaned_data['adresa']
            narudzba.drzava = forma_narudzbe.cleaned_data['drzava']
            narudzba.zupanija = forma_narudzbe.cleaned_data['zupanija']
            narudzba.grad = forma_narudzbe.cleaned_data['grad']
            narudzba.postanski_broj = forma_narudzbe.cleaned_data['postanski_broj']
            narudzba.korisnik = request.user
            narudzba.ukupno = ukupan_iznos
            narudzba.porezni_podaci = json.dumps(pdv_dict)
            narudzba.ukupno_poreza = pdv
            narudzba.nacin_placanja = request.POST['nacin_placanja']
            narudzba.save() 
            narudzba.broj_narudzbe = generiraj_broj_narudzbe(narudzba.id)
            narudzba.save()
            context = {
                'narudzba': narudzba,
                'proizvodi_u_kosarici': proizvodi_u_kosarici
            }
            return render(request, 'narudzbe/posalji_narudzbu.html', context)

        else:
            print(forma_narudzbe.errors)

    return render(request, 'narudzbe/posalji_narudzbu.html')

@login_required(login_url='prijava')
def placanje(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        broj_narudzbe = request.POST.get('broj_narudzbe')
        id_transakcije = request.POST.get('id_transakcije')
        nacin_placanja = request.POST.get('nacin_placanja')
        status = request.POST.get('status')

        narudzba = Narudzba.objects.get(korisnik=request.user, broj_narudzbe=broj_narudzbe)
        placanje = Placanje(
            korisnik=request.user, 
            id_transakcije=id_transakcije, 
            nacin_placanja=nacin_placanja, 
            iznos=narudzba.ukupno,
            status=status
        )
        placanje.save()

        narudzba.placanje = placanje
        narudzba.naruceno = True
        narudzba.save()

        proizvodi_u_kosarici = Kosarica.objects.filter(korisnik=request.user)
        for proizvod in proizvodi_u_kosarici:
            naruceni_proizvodi = NaruceniProizvodi()
            naruceni_proizvodi.narudzba = narudzba
            naruceni_proizvodi.placanje = placanje
            naruceni_proizvodi.korisnik = request.user
            naruceni_proizvodi.proizvod = proizvod.proizvod
            naruceni_proizvodi.kolicina = proizvod.kolicina
            naruceni_proizvodi.cijena = proizvod.proizvod.cijena_proizvoda
            naruceni_proizvodi.iznos = proizvod.proizvod.cijena_proizvoda * proizvod.kolicina
            naruceni_proizvodi.save()

        mail_subject = 'Hvala na narudžbi.'
        mail_template = 'narudzbe/potvrda_narudzbe_email.html'
        context = {
            'korisnik': request.user,
            'narudzba': narudzba,
            'to_email': narudzba.email
        }
        posalji_obavijest_opg_verifikacija(mail_subject, mail_template, context)

        mail_subject = 'Primili ste novu narudžbu.'
        mail_template = 'narudzbe/nova_narudzba_primljena.html'
        to_emails = []
        for proizvod in proizvodi_u_kosarici:
            if proizvod.proizvod.opg.korisnik.email not in to_emails:
                to_emails.append(proizvod.proizvod.opg.korisnik.email)
        print('to_emails --->', to_emails)
        context = {
            'narudzba': narudzba,
            'to_email': to_emails
        }
        posalji_obavijest_opg_verifikacija(mail_subject, mail_template, context)
       
        #proizvodi_u_kosarici.delete()
        response = {
            'broj_narudzbe': broj_narudzbe,
            'id_transakcije': id_transakcije
        }
        return JsonResponse(response)
    
    return HttpResponse('placanje view')


def narudzba_poslana(request):
    broj_narudzbe = request.GET.get('broj_narudzbe')
    id_transackije = request.GET.get('id_transakcije')
    
    try:
        narudzba = Narudzba.objects.get(broj_narudzbe=broj_narudzbe, placanje__id_transakcije=id_transackije, naruceno=True)
        naruceni_proizvodi = NaruceniProizvodi.objects.filter(narudzba=narudzba)

        ukupna_cijena_proizvoda = 0
        for proizvod in naruceni_proizvodi:
            ukupna_cijena_proizvoda +=(proizvod.cijena * proizvod.kolicina)

        porezni_podaci = json.loads(narudzba.porezni_podaci)  

        context = {
            'narudzba': narudzba,
            'naruceni_proizvodi': naruceni_proizvodi,
            'ukupna_cijena_proizvoda': ukupna_cijena_proizvoda,
            'porezni_podaci': porezni_podaci
        }
        return render(request, 'narudzbe/narudzba_poslana.html', context)
    except:
        return redirect('pocetna_stranica')
    