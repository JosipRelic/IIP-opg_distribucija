import simplejson as json
from django.shortcuts import render, redirect
from e_trznica.models import Kosarica
from e_trznica.context_processors import dohvati_iznose_u_kosarici
from .forms import FormaNarudzbe
from .models import Narudzba
from .utils import generiraj_broj_narudzbe

# Create your views here.
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
            return redirect('posalji_narudzbu')

        else:
            print(forma_narudzbe.errors)

    return render(request, 'narudzbe/posalji_narudzbu.html')