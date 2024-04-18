from django.shortcuts import render, redirect
from .forms import FormaKorisnik
from opg.forms import FormaOpg
from .models import User, KorisnickiProfil
from django.contrib import messages

# Create your views here.
def registrirajKorisnika(request):
    if request.method == 'POST':
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
    if request.method == 'POST':
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

