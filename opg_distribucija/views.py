from django.shortcuts import render
from django.http import HttpResponse

def pocetna_stranica(request):
    return render(request, 'pocetna_stranica.html')