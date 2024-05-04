from django.shortcuts import render, redirect
from .forms import FormaKorisnik
from opg.forms import FormaOpg
from .models import User, KorisnickiProfil
from .utils import detektirajKorisnika, posalji_verifikacijski_email
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


# Ogranici pristup stranicama kupca od strane opg-a
def provjeri_korisnika_opg(user):
    if user.role == 1:
        return True
    else: 
        raise PermissionDenied

# Ogranici pristup stranicama opg-a od strane kupca
def provjeri_korisnika_kupac(user):
    if user.role == 2:
        return True
    else: 
        raise PermissionDenied


def registrirajKorisnika(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Već ste prijavljeni!')
        return redirect('nadzorna_ploca')
    elif request.method == 'POST':
        forma = FormaKorisnik(request.POST)
        if forma.is_valid():       
            # KREIRAJ KORISNIKA POMOĆU FORME
            # lozinka = forma.cleaned_data['password']
            # korisnik = forma.save(commit=False)
            # korisnik.set_password(lozinka)
            # korisnik.role = User.KUPAC
            # forma.save()

            # KREIRAJ KORISNIKA POMOĆU metode create_user() IZ MODELA
            ime = forma.cleaned_data['first_name']
            prezime = forma.cleaned_data['last_name']
            korisnicko_ime = forma.cleaned_data['username']
            email = forma.cleaned_data['email']
            lozinka = forma.cleaned_data['password']
            korisnik = User.objects.create_user(first_name=ime, last_name=prezime, username=korisnicko_ime, email=email, password=lozinka)
            korisnik.role = User.KUPAC
            korisnik.save()

            #posalji verifikacijski email
            posalji_verifikacijski_email(request, korisnik)

            messages.success(request, 'Vaš račun je uspješno registriran!')

            return redirect('registrirajKorisnika')
        else:
            print('forma nije ispravna!')
            print(forma.errors)
    else:
        forma = FormaKorisnik() 
    context = {
        'forma': forma,
    }
    return render(request, 'korisnicki_racuni/registriraj_korisnika.html', context)



def registrirajOpg(request): 
    if request.user.is_authenticated:
        messages.warning(request, 'Već ste prijavljeni!')
        return redirect('nadzorna_ploca')
    elif request.method == 'POST':
        forma = FormaKorisnik(request.POST)
        opg_forma = FormaOpg(request.POST, request.FILES)
        if forma.is_valid() and opg_forma.is_valid():
            ime = forma.cleaned_data['first_name']
            prezime = forma.cleaned_data['last_name']
            korisnicko_ime = forma.cleaned_data['username']
            email = forma.cleaned_data['email']
            lozinka = forma.cleaned_data['password']
            korisnik = User.objects.create_user(first_name=ime, last_name=prezime, username=korisnicko_ime, email=email, password=lozinka)
            korisnik.role = User.OPG
            korisnik.save()
            opg = opg_forma.save(commit=False)
            opg.korisnik = korisnik
            korisnicki_profil = KorisnickiProfil.objects.get(korisnik=korisnik)
            opg.korisnicki_profil = korisnicki_profil
            opg.save()

            #posalji verifikacijski email
            posalji_verifikacijski_email(request, korisnik)

            messages.success(request, 'Vaš račun je uspješno registriran! Sačekajte verifikaciju!')
            return redirect('registrirajOpg')
        else:
            print('forma nije ispravna!')
            print(forma.errors)
    else:
        forma = FormaKorisnik()
        opg_forma = FormaOpg()

    context = {
        'forma': forma,
        'opg_forma': opg_forma
    }

    return render(request, 'korisnicki_racuni/registriraj_opg.html', context)

def aktiviraj_racun(request, uidb64, token):
    #aktiviraj korisnika promjenom is_active u True 
    return


def prijava(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Već ste prijavljeni!')
        return redirect('mojRacun')
    elif request.method == 'POST':
        email = request.POST['email']
        lozinka = request.POST['lozinka']

        user = auth.authenticate(email=email, password=lozinka)   

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Prijavljeni ste.')
            return redirect('mojRacun')
        else:
            messages.error(request, 'Neispravni podatci za prijavu!')
            return redirect('prijava')
    return render(request, 'korisnicki_racuni/prijava.html')


def odjava(request):
    auth.logout(request)
    messages.info(request, 'Odjavljeni ste.')
    return redirect('prijava')

@login_required(login_url='prijava')
def mojRacun(request):
    user = request.user
    redirectUrl = detektirajKorisnika(user)
    return redirect(redirectUrl)

@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_kupac)
def kupac_nadzorna_ploca(request):
    return render(request, 'korisnicki_racuni/kupac_nadzorna_ploca.html')

@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_opg)
def opg_nadzorna_ploca(request):
    return render(request, 'korisnicki_racuni/opg_nadzorna_ploca.html')
