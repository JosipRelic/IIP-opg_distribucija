from django.shortcuts import render
from django.http import HttpResponse
from opg.models import Opg

def pocetna_stranica(request):
    opgovi = Opg.objects.filter(opg_verificiran=True, korisnik__is_active=True)[:6]
    context = {
        'opgovi': opgovi,
    }
    return render(request, 'pocetna_stranica.html', context)