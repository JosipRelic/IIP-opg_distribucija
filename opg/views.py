from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify

from narudzbe.models import NaruceniProizvodi, Narudzba

from .forms import FormaOpg
from opg_ponuda.forms import FormaKategorije, FormaProizvodi
from korisnicki_racuni.forms import KorisnickiProfilForma

from .models import Opg
from korisnicki_racuni.models import KorisnickiProfil
from opg_ponuda.models import KategorijeProizvoda, Proizvodi

from korisnicki_racuni.views import provjeri_korisnika_opg



def dohvati_opg(request):
    opg = Opg.objects.get(korisnik = request.user)
    return opg

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


@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_opg)
def kreiranje_ponude(request):
    opg = dohvati_opg(request)
    kategorije = KategorijeProizvoda.objects.filter(opg=opg).order_by('kreirano')
    context = {
        'kategorije': kategorije,
    }
    return render(request, 'opg/kreiranje_ponude.html', context)


@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_opg)
def proizvodi_po_kategoriji(request, pk=None):
    opg = dohvati_opg(request)
    kategorija = get_object_or_404(KategorijeProizvoda, pk=pk)
    proizvodi = Proizvodi.objects.filter(opg=opg, kategorija_proizvoda=kategorija)
    context = {
        'proizvodi': proizvodi,
        'kategorija': kategorija,
    }
    return render(request, 'opg/proizvodi_po_kategoriji.html', context)


@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_opg)
def dodaj_kategoriju(request):
    if request.method == 'POST':
        forma_kategorije = FormaKategorije(request.POST)
        if forma_kategorije.is_valid():
            naziv_kategorije = forma_kategorije.cleaned_data['naziv_kategorije']
            kategorija = forma_kategorije.save(commit=False)
            kategorija.opg = dohvati_opg(request)
            kategorija.save()
            kategorija.slug = slugify(naziv_kategorije)+'-'+str(kategorija.id)
            kategorija.save()
            messages.success(request, 'Nova kategorija kreirana.')
            return redirect('kreiranje_ponude')
        else:
            print(forma_kategorije.errors)
    else:
        forma_kategorije = FormaKategorije()
    
    context = {
        'forma_kategorije': forma_kategorije,
    }
    return render(request, 'opg/dodaj_kategoriju.html', context)


@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_opg)
def uredi_kategoriju(request, pk=None):
    kategorije= get_object_or_404(KategorijeProizvoda, pk=pk)
    if request.method == 'POST':
        forma_kategorije = FormaKategorije(request.POST, instance=kategorije)
        if forma_kategorije.is_valid():
            naziv_kategorije = forma_kategorije.cleaned_data['naziv_kategorije']
            kategorije = forma_kategorije.save(commit=False)
            kategorije.opg = dohvati_opg(request)
            kategorije.save()
            kategorije.slug = slugify(naziv_kategorije)+'-'+str(kategorije.id)
            kategorije.save()
            messages.success(request, 'Kategorija uspješno ažurirana.')
            return redirect('kreiranje_ponude')
        else:
            print(forma_kategorije.errors)
    else:
        forma_kategorije = FormaKategorije(instance=kategorije)
    
    context = {
        'forma_kategorije': forma_kategorije,
        'kategorija': kategorije,
    }
    return render(request, 'opg/uredi_kategoriju.html', context)


@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_opg)
def obrisi_kategoriju(request, pk=None):
    kategorija = get_object_or_404(KategorijeProizvoda, pk=pk)
    kategorija.delete()
    messages.success(request, 'Kategorija je uspješno obrisana.')
    return redirect('kreiranje_ponude')


@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_opg)
def dodaj_proizvod(request):
    if request.method == 'POST':
        forma_proizvodi = FormaProizvodi(request.POST, request.FILES)
        if forma_proizvodi.is_valid():
            naziv_proizvoda = forma_proizvodi.cleaned_data['naziv_proizvoda']
            proizvod = forma_proizvodi.save(commit=False)
            proizvod.opg = dohvati_opg(request)
            proizvod.save()
            proizvod.slug = slugify(naziv_proizvoda)+'-'+str(proizvod.id)
            proizvod.save()
            messages.success(request, 'Novi proizvod kreiran.')
            return redirect('proizvodi_po_kategoriji', proizvod.kategorija_proizvoda.pk)
        else:
            print(forma_proizvodi.errors)
    else:
        forma_proizvodi = FormaProizvodi()
        #filtriranje kategorije po specificnom opgu !!! PRONAĆI NAČIN KAKO HANDLEAT AKO KATEGORIJA POSTOJI U BAZI ALI NE ZA TAJ OPG...
        forma_proizvodi.fields['kategorija_proizvoda'].queryset = KategorijeProizvoda.objects.filter(opg = dohvati_opg(request))

    context = {
        'forma_proizvodi': forma_proizvodi,
    }
    return render(request, 'opg/dodaj_proizvod.html', context)


@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_opg)
def uredi_proizvod(request, pk=None):
    proizvodi = get_object_or_404(Proizvodi, pk=pk)
    if request.method == 'POST':
        forma_proizvodi = FormaProizvodi(request.POST, request.FILES, instance=proizvodi)
        if forma_proizvodi.is_valid():
            naziv_proizvoda = forma_proizvodi.cleaned_data['naziv_proizvoda']
            proizvodi = forma_proizvodi.save(commit=False)
            proizvodi.opg = dohvati_opg(request)
            proizvodi.save()
            proizvodi.slug = slugify(naziv_proizvoda)+'-'+str(proizvodi.id)
            proizvodi.save()
            messages.success(request, 'Proizvod je uspješno ažuriran.')
            return redirect('proizvodi_po_kategoriji', proizvodi.kategorija_proizvoda.pk)
        else:
            print(forma_proizvodi.errors)
    else:
        forma_proizvodi = FormaProizvodi(instance=proizvodi)
        forma_proizvodi.fields['kategorija_proizvoda'].queryset = KategorijeProizvoda.objects.filter(opg = dohvati_opg(request))
    
    context = {
        'forma_proizvodi': forma_proizvodi,
        'proizvodi': proizvodi,
    }
    return render(request, 'opg/uredi_proizvod.html', context)


@login_required(login_url='prijava')
@user_passes_test(provjeri_korisnika_opg)
def obrisi_proizvod(request, pk=None):
    proizvod = get_object_or_404(Proizvodi, pk=pk)
    proizvod.delete()
    messages.success(request, 'Proizvod je uspješno obrisan.')
    return redirect('proizvodi_po_kategoriji', proizvod.kategorija_proizvoda.pk)


def detalji_narudzbe_opg(request, broj_narudzbe):
    try:
        narudzba = Narudzba.objects.get(broj_narudzbe=broj_narudzbe, naruceno=True)
        naruceni_proizvodi = NaruceniProizvodi.objects.filter(narudzba=narudzba, proizvod__opg=dohvati_opg(request))

        context = {
            'narudzba': narudzba,
            'naruceni_proizvodi': naruceni_proizvodi,
            'ukupna_cijena_proizvoda': narudzba.dohvati_ukupno_po_opgu()['ukupna_cijena_proizvoda'],
            'porezni_podaci': narudzba.dohvati_ukupno_po_opgu()['pdv_dict'],
            'ukupno': narudzba.dohvati_ukupno_po_opgu()['ukupno']
        }
    except:
        redirect('opg')

    return render(request, 'opg/detalji_narudzbe_opg.html', context)


def moje_narudzbe_opg(request):
    opg = Opg.objects.get(korisnik = request.user)
    narudzbe = Narudzba.objects.filter(opgovi__in=[opg.id], naruceno=True).order_by('-kreirano')

    context = {
        'narudzbe': narudzbe
    }
    return render(request, 'opg/moje_narudzbe_opg.html', context)