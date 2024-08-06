from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from e_trznica.context_processors import dohvati_brojac_kosarice, dohvati_iznose_u_kosarici
from opg.models import Opg
from opg_ponuda.models import KategorijeProizvoda, Proizvodi
from e_trznica.models import Kosarica
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

# Create your views here.
def e_trznica(request):
    opgovi = Opg.objects.filter(opg_verificiran=True, korisnik__is_active=True)
    broj_opgova = opgovi.count()
    context = {
        'opgovi': opgovi,
        'broj_opgova': broj_opgova,
    }
    return render(request, 'e_trznica/prikaz_opgova.html', context)

def pojedinosti_opga(request, opg_slug):
    opg = get_object_or_404(Opg, opg_slug=opg_slug)
    kategorije_proizvoda = KategorijeProizvoda.objects.filter(opg=opg).prefetch_related(
        Prefetch(
            'proizvodi',
            queryset= Proizvodi.objects.filter(proizvod_dostupan=True)
        )
    )

    if request.user.is_authenticated:
        proizvodi_u_kosarici = Kosarica.objects.filter(korisnik=request.user) 
    else:
        proizvodi_u_kosarici = None
        
    context = {
        'opg': opg,
        'kategorije_proizvoda': kategorije_proizvoda,
        'proizvodi_u_kosarici': proizvodi_u_kosarici,
    }
    return render(request, 'e_trznica/pojedinosti_opga.html', context)

def dodaj_u_kosaricu(request, id_proizvoda):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #provjeravanje da li proizvod postoji
            try:
                proizvod = Proizvodi.objects.get(id=id_proizvoda)
                #provjeravanje da li je taj proizvod već u košaricu
                try:
                    provjeraKosarice = Kosarica.objects.get(korisnik=request.user, proizvod=proizvod)
                    # povećavanje količine u košarici
                    provjeraKosarice.kolicina += 1
                    provjeraKosarice.save()
                    return JsonResponse({
                        'status': 'Uspješno',
                        'poruka': 'Količina proizvoda u košarici je uvećana.',
                        'brojac_kosarice': dohvati_brojac_kosarice(request),
                        'kolicina': provjeraKosarice.kolicina,
                        'iznos_kosarice': dohvati_iznose_u_kosarici(request)
                    })
                except:
                    provjeraKosarice = Kosarica.objects.create(korisnik=request.user, proizvod=proizvod, kolicina=1)
                    return JsonResponse({
                        'status': 'Uspješno',
                        'poruka': 'Proizvod je dodan u košaricu',
                        'brojac_kosarice': dohvati_brojac_kosarice(request),
                        'kolicina': provjeraKosarice.kolicina,
                        'iznos_kosarice': dohvati_iznose_u_kosarici(request)
                    })

            except:
                return JsonResponse({
                    'status': 'Neuspješno',
                    'poruka': 'Ovaj proizvod nije na raspolaganju.'
                 })
        else:
            return JsonResponse({
                'status': 'Neuspješno',
                'poruka': 'Nevažeći zahtjev.'
            })
        
    else:
        return JsonResponse({
            'status': 'potrebna_prijava',
            'poruka': 'Molimo Vas da se prijavite za nastavak.'
        })


def ukloni_iz_kosarice(request, id_proizvoda):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #provjeravanje da li proizvod postoji
            try:
                proizvod = Proizvodi.objects.get(id=id_proizvoda)
                #provjeravanje da li je taj proizvod već u košaricu
                try:
                    provjeraKosarice = Kosarica.objects.get(korisnik=request.user, proizvod=proizvod)
                    
                    if provjeraKosarice.kolicina > 1:
                        # smanjivanje količine u košarici
                        provjeraKosarice.kolicina -= 1
                        provjeraKosarice.save()
                    else:
                        provjeraKosarice.delete()
                        provjeraKosarice.kolicina = 0
                    return JsonResponse({
                        'status': 'Uspješno',
                        'poruka': 'Količina proizvoda u košarici je umanjena.',
                        'brojac_kosarice': dohvati_brojac_kosarice(request),
                        'kolicina': provjeraKosarice.kolicina,
                        'iznos_kosarice': dohvati_iznose_u_kosarici(request)
                    })
                except:
                    return JsonResponse({
                        'status': 'Neuspješno',
                        'poruka': 'Nemate ovaj proizvod u košarici',
                    })

            except:
                return JsonResponse({
                    'status': 'Neuspješno',
                    'poruka': 'Ovaj proizvod nije na raspolaganju.'
                 })
        else:
            return JsonResponse({
                'status': 'Neuspješno',
                'poruka': 'Nevažeći zahtjev.'
            })
        
    else:
        return JsonResponse({
            'status': 'potrebna_prijava',
            'poruka': 'Molimo Vas da se prijavite za nastavak.'
        })

@login_required(login_url='prijava')
def kosarica(request):
    proizvodi_u_kosarici = Kosarica.objects.filter(korisnik=request.user).order_by('kreirano')
    context = {
        'proizvodi_u_kosarici': proizvodi_u_kosarici
    }
    return render(request, 'e_trznica/kosarica.html', context)

def obrisi_kosaricu(request, id_kosarice):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                proizvod_u_kosarici = Kosarica.objects.get(korisnik=request.user, id = id_kosarice)
                if proizvod_u_kosarici:
                    proizvod_u_kosarici.delete()
                    return JsonResponse({
                        'status': 'Uspješno',
                        'poruka': 'Proizvod je obrisan iz košarice.',
                        'brojac_kosarice': dohvati_brojac_kosarice(request),
                        'iznos_kosarice': dohvati_iznose_u_kosarici(request)
                    })                    
            except:
                return JsonResponse({
                    'status': 'Neuspješno',
                    'poruka': 'Ovaj proizvod nije na raspolaganju.'
                 })
        else:
            return JsonResponse({
                'status': 'Neuspješno',
                'poruka': 'Nevažeći zahtjev.'
            })


def pretraga(request):
    if not 'lokacija' in request.GET:
        return redirect('e_trznica')
    else:
        lokacija = request.GET['lokacija']
        lat = request.GET['lat']
        lng = request.GET['lng']
        udaljenost = request.GET['udaljenost']
        naziv_opga_proizvoda = request.GET['naziv_opga_proizvoda']

        dohvati_opgove_po_proizvodima = Proizvodi.objects.filter(naziv_proizvoda__icontains=naziv_opga_proizvoda, proizvod_dostupan=True).values_list('opg', flat=True)
        opgovi = Opg.objects.filter(Q(id__in=dohvati_opgove_po_proizvodima) | Q(naziv_opga__icontains=naziv_opga_proizvoda, opg_verificiran=True, korisnik__is_active=True))
        
        if lat and lng and udaljenost:
            pnt = GEOSGeometry("POINT({0} {1})".format(lng, lat))
            opgovi = Opg.objects.filter(Q(id__in=dohvati_opgove_po_proizvodima) | Q(naziv_opga__icontains=naziv_opga_proizvoda, opg_verificiran=True, korisnik__is_active=True), 
                                        korisnicki_profil__lokacija__distance_lte=(pnt, D(km=udaljenost))
                                        ).annotate(distance=Distance("korisnicki_profil__lokacija", pnt)).order_by("distance")

            for opg in opgovi:
                opg.udaljenost_km = round(opg.distance.km, 1) 
            
        broj_opgova = opgovi.count()

        context = {
            'opgovi': opgovi,
            'broj_opgova': broj_opgova,
            'trenutna_lokacija': lokacija
        }
    
        return render(request, 'e_trznica/prikaz_opgova.html', context)