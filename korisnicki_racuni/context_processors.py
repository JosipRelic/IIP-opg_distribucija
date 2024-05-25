from opg.models import Opg
from django.conf import settings

def dohvati_opg(request):
    try:
        opg = Opg.objects.get(korisnik = request.user)
    except:
        opg = None
    return dict(opg=opg)

def dohvati_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}