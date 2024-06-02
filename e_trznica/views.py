from django.shortcuts import render, get_object_or_404
from opg.models import Opg
from opg_ponuda.models import KategorijeProizvoda, Proizvodi
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
    context = {
        'opg': opg,
        'kategorije_proizvoda': kategorije_proizvoda,
    }
    return render(request, 'e_trznica/pojedinosti_opga.html', context)
