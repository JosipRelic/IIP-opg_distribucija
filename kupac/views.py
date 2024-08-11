from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from korisnicki_racuni.forms import KorisnickiProfilForma, FormaInfoKorisnik
from korisnicki_racuni.models import KorisnickiProfil
from django.contrib import messages

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