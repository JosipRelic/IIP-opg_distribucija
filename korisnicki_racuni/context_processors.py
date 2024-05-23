from opg.models import Opg

def dohvati_opg(request):
    try:
        opg = Opg.objects.get(korisnik = request.user)
    except:
        opg = None
    return dict(opg=opg)