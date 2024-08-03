from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from e_trznica.context_processors import dohvati_brojac_kosarice
from opg.models import Opg
from opg_ponuda.models import KategorijeProizvoda, Proizvodi
from e_trznica.models import Kosarica
from django.db.models import Prefetch

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
                        'kolicina': provjeraKosarice.kolicina
                    })
                except:
                    provjeraKosarice = Kosarica.objects.create(korisnik=request.user, proizvod=proizvod, kolicina=1)
                    return JsonResponse({
                        'status': 'Uspješno',
                        'poruka': 'Proizvod je dodan u košaricu',
                        'brojac_kosarice': dohvati_brojac_kosarice(request),
                        'kolicina': provjeraKosarice.kolicina
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
            'status': 'Neuspješno',
            'poruka': 'Molimo Vas da se prijavite za nastavak.'
        })
