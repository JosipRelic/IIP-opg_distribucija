from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import FormaOpg
from .models import Opg
from korisnicki_racuni.forms import KorisnickiProfilForma
from korisnicki_racuni.models import KorisnickiProfil
from korisnicki_racuni.views import provjeri_korisnika_opg
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_opg)
def opg_profil(request):
    profil = get_object_or_404(KorisnickiProfil, korisnik = request.user)
    opg = get_object_or_404(Opg, korisnik = request.user)

    if request.method == 'POST':
        profil_forma = KorisnickiProfilForma(request.POST, request.FILES, instance=profil)
        opg_forma = FormaOpg(request.POST, request.FILES, instance=opg)
        if profil_forma.is_valid() and opg_forma.is_valid():
            profil_forma.save()
            opg_forma.save()
            messages.success(request, 'Podatci su ažurirani.')
            return redirect('opg_profil')
        else:
            print(profil_forma.errors)
            print(opg_forma.errors)

    else:
        profil_forma = KorisnickiProfilForma(instance=profil)
        opg_forma = FormaOpg(instance=opg)

    context = {
        'profil_forma': profil_forma,
        'opg_forma': opg_forma,
        'profil': profil,
        'opg': opg,
    }
    return render(request, 'opg/opg_profil.html', context)


def kreiranje_ponude(request):
    return render(request, 'opg/kreiranje_ponude.html')