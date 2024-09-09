from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from korisnicki_racuni.forms import KorisnickiProfilForma, FormaInfoKorisnik
from korisnicki_racuni.models import KorisnickiProfil
from django.contrib import messages
import simplejson as json

from narudzbe.models import NaruceniProizvodi, Narudzba

# Create your views here.
@login_required(login_url='prijava')
def kupac_profil(request):
    profil = get_object_or_404(KorisnickiProfil, korisnik=request.user)
    if request.method == 'POST':
        profil_forma = KorisnickiProfilForma(request.POST, request.FILES, instance=profil)
        forma_info_korisnik = FormaInfoKorisnik(request.POST, instance=request.user)
        if profil_forma.is_valid() and forma_info_korisnik.is_valid():
            profil_forma.save()
            forma_info_korisnik.save()
            messages.success(request, 'Profil ažuriran.')
            return redirect('kupac_profil')
        else:
            print(profil_forma.errors)
            print(forma_info_korisnik.errors)
    else:       
        profil_forma = KorisnickiProfilForma(instance=profil)
        forma_info_korisnik = FormaInfoKorisnik(instance=request.user)

    context = {
        'profil': profil,
        'profil_forma': profil_forma,
        'forma_info_korisnik': forma_info_korisnik
    }
    return render(request, 'kupac/kupac_profil.html', context)

def moje_narudzbe(request):
    narudzbe = Narudzba.objects.filter(korisnik=request.user, naruceno=True)
    context = {
        'narudzbe': narudzbe,
        'broj_narudzbi': narudzbe.count(),
    }
    return render(request, 'kupac/moje_narudzbe.html', context)

def detalji_narudzbe(request, broj_narudzbe):
    narudzba = Narudzba.objects.get(broj_narudzbe=broj_narudzbe, naruceno=True)

    if not narudzba:
        print(f"Narudzba pod ovim brojem ne postoji {broj_narudzbe} ili nije narucena(naruceno=False)")
        return redirect('kupac')

    naruceni_proizvodi = NaruceniProizvodi.objects.filter(narudzba=narudzba)
    
    ukupna_cijena_proizvoda = 0

    for proizvod in naruceni_proizvodi:
        ukupna_cijena_proizvoda += (proizvod.cijena * proizvod.kolicina)
    
    porezni_podaci = json.loads(narudzba.porezni_podaci)

    context = {
        'narudzba': narudzba,
        'naruceni_proizvodi': naruceni_proizvodi,
        'ukupna_cijena_proizvoda': round(ukupna_cijena_proizvoda,2),
        'porezni_podaci': porezni_podaci
    }

    return render(request, 'kupac/detalji_narudzbe.html', context)
