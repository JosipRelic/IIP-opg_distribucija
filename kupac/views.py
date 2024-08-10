from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from korisnicki_racuni.forms import KorisnickiProfilForma, FormaInfoKorisnik
from korisnicki_racuni.models import KorisnickiProfil

# Create your views here.
@login_required(login_url='prijava')
def kupac_profil(request):
    profil = get_object_or_404(KorisnickiProfil, korisnik=request.user)
    profil_forma = KorisnickiProfilForma(instance=profil)
    forma_info_korisnik = FormaInfoKorisnik(instance=request.user)

    context = {
        'profil_forma': profil_forma,
        'forma_info_korisnik': forma_info_korisnik
    }
    return render(request, 'kupac/kupac_profil.html', context)