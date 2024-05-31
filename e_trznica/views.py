from django.shortcuts import render
from opg.models import Opg

# Create your views here.
def e_trznica(request):
    opgovi = Opg.objects.filter(opg_verificiran=True, korisnik__is_active=True)
    broj_opgova = opgovi.count()
    context = {
        'opgovi': opgovi,
        'broj_opgova': broj_opgova,
    }
    return render(request, 'e_trznica/prikaz_opgova.html', context)