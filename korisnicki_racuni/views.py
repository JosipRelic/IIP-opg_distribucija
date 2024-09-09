from django.shortcuts import render, redirect

from narudzbe.models import Narudzba
from .forms import FormaKorisnik
from opg.forms import FormaOpg
from .models import User, KorisnickiProfil
from .utils import detektirajKorisnika, posalji_verifikacijski_email
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from opg.models import Opg
from django.template.defaultfilters import slugify

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
            email_subject = 'Molimo Vas aktivirajte Vaš račun!'
            email_template = 'korisnicki_racuni/email/verifikacija_racuna_mailom.html'
            posalji_verifikacijski_email(request, korisnik, email_subject, email_template)

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
        return redirect('mojRacun')
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
            naziv_opga = opg_forma.cleaned_data['naziv_opga']
            opg.opg_slug = slugify(naziv_opga)+'-'+str(korisnik.pk)
            korisnicki_profil = KorisnickiProfil.objects.get(korisnik=korisnik)
            opg.korisnicki_profil = korisnicki_profil
            opg.save()

            #posalji verifikacijski email
            email_subject = 'Molimo Vas aktivirajte Vaš račun!'
            email_template = 'korisnicki_racuni/email/verifikacija_racuna_mailom.html'
            posalji_verifikacijski_email(request, korisnik, email_subject, email_template)

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
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Vaš korisnički račun je aktiviran.')
        return redirect('mojRacun')
    else:
        messages.error(request, 'Nevažeći link za aktivaciju!')
        return redirect('mojRacun')

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
    narudzbe = Narudzba.objects.filter(korisnik=request.user, naruceno=True).order_by('-kreirano')
    posljednje_narudzbe = narudzbe[:5]
    context = {
        'narudzbe': narudzbe,
        'broj_narudzbi': narudzbe.count(),
        'posljednje_narudzbe': posljednje_narudzbe
    }
    return render(request, 'korisnicki_racuni/kupac_nadzorna_ploca.html', context)

@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_opg)
def opg_nadzorna_ploca(request):
    return render(request, 'korisnicki_racuni/opg_nadzorna_ploca.html')


def zaboravljena_lozinka(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            #slanje linka za oporavak lozinke
            email_subject = 'Ponovno postavite Vašu lozinku!'
            email_template = 'korisnicki_racuni/email/mail_za_resetiranje_lozinke.html'
            posalji_verifikacijski_email(request, user, email_subject, email_template)
            messages.success(request, 'Upravo Vam je poslan link za oporavak lozinke na Vašu email adresu.')
            return redirect('prijava')
        else:
            messages.error(request, 'Korisnički račun s upisanom email adresom ne postoji!')
            return redirect('zaboravljena_lozinka')

    return render(request, 'korisnicki_racuni/zaboravljena_lozinka.html')

def resetiraj_lozinku_validacija(request, uidb64, token):
    #validacija korisnika putem dekodiranja tokena i primarnog ključa korisnika
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Molimo Vas da ponovno postavite Vašu lozinku.')
        return redirect('resetiraj_lozinku')
    else:
        messages.error(request, 'Link je istekao!')
        return redirect('mojRacun')

def resetiraj_lozinku(request):
    if request.method == 'POST':
        lozinka = request.POST['lozinka']
        potvrdi_lozinku = request.POST['potvrdi_lozinku']

        if lozinka == potvrdi_lozinku:
            pk = request.session.get('uid')
            korisnik = User.objects.get(pk=pk)
            korisnik.set_password(lozinka)
            korisnik.is_active = True
            korisnik.save()
            messages.success(request, 'Lozinka je uspješno promijenjena.')
            return redirect('prijava')
        else:
            messages.error(request, 'Lozinke se ne podudaraju!')
            return redirect('resetiraj_lozinku')
        
    return render(request, 'korisnicki_racuni/resetiraj_lozinku.html')