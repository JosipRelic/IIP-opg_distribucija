from django.shortcuts import render
from django.http import HttpResponse
from opg.models import Opg
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

def dohvati_ili_postavi_trenutnu_lokaciju(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng, lat
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat'] = lat
        request.session['lng'] = lng
        return lng, lat
    else:
        return None

def pocetna_stranica(request):
    if dohvati_ili_postavi_trenutnu_lokaciju(request) is not None:

        pnt = GEOSGeometry("POINT(%s %s)" % (dohvati_ili_postavi_trenutnu_lokaciju(request)))
        opgovi = Opg.objects.filter(korisnicki_profil__lokacija__distance_lte=(pnt, D(km=50))).annotate(distance=Distance("korisnicki_profil__lokacija", pnt)).order_by("distance")

        for opg in opgovi:
            opg.udaljenost_km = round(opg.distance.km, 1) 
    else:
        opgovi = Opg.objects.filter(opg_verificiran=True, korisnik__is_active=True)[:6]
    
    context = {
        'opgovi': opgovi,
    }
    return render(request, 'pocetna_stranica.html', context)