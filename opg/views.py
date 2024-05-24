from django.shortcuts import render, get_object_or_404
from .forms import FormaOpg
from korisnicki_racuni.forms import KorisnickiProfilForma
from korisnicki_racuni.models import KorisnickiProfil
from .models import Opg
# Create your views here.

def opg_profil(request):
    profil = get_object_or_404(KorisnickiProfil, korisnik = request.user)
    opg = get_object_or_404(Opg, korisnik = request.user)

    profil_forma = KorisnickiProfilForma(instance=profil)
    opg_forma = FormaOpg(instance=opg)

    context = {
        'profil_forma': profil_forma,
        'opg_forma': opg_forma,
        'profil': profil,
        'opg': opg,
    }
    return render(request, 'opg/opg_profil.html', context)
