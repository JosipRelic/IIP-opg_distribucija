from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import FormaOpg
from opg_ponuda.forms import FormaKategorije
from .models import Opg
from korisnicki_racuni.forms import KorisnickiProfilForma
from korisnicki_racuni.models import KorisnickiProfil
from opg_ponuda.models import KategorijeProizvoda, Proizvodi
from korisnicki_racuni.views import provjeri_korisnika_opg
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify


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

def dodaj_kategoriju(request):
    if request.method == 'POST':
        forma_kategorije = FormaKategorije(request.POST)
        if forma_kategorije.is_valid():
            naziv_kategorije = forma_kategorije.cleaned_data['naziv_kategorije']
            kategorija = forma_kategorije.save(commit=False)
            kategorija.opg = dohvati_opg(request)
            kategorija.slug = slugify(naziv_kategorije)
            forma_kategorije.save()
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


def uredi_kategoriju(request, pk=None):
    kategorije= get_object_or_404(KategorijeProizvoda, pk=pk)
    if request.method == 'POST':
        forma_kategorije = FormaKategorije(request.POST, instance=kategorije)
        if forma_kategorije.is_valid():
            naziv_kategorije = forma_kategorije.cleaned_data['naziv_kategorije']
            kategorije = forma_kategorije.save(commit=False)
            kategorije.opg = dohvati_opg(request)
            kategorije.slug = slugify(naziv_kategorije)
            forma_kategorije.save()
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


def obrisi_kategoriju(request, pk=None):
    kategorija = get_object_or_404(KategorijeProizvoda, pk=pk)
    kategorija.delete()
    messages.success(request, 'Kategorija je uspješno obrisana.')
    return redirect('kreiranje_ponude')