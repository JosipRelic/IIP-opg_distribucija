from .models import Kosarica
from opg_ponuda.models import Proizvodi


def dohvati_brojac_kosarice(request):
    kolicina_proizvoda_u_kosarici = 0
    if request.user.is_authenticated:
        try:
            proizvodi_u_kosarici = Kosarica.objects.filter(korisnik=request.user)
            if proizvodi_u_kosarici:
                for proizvod_u_kosarici in proizvodi_u_kosarici:
                    kolicina_proizvoda_u_kosarici += proizvod_u_kosarici.kolicina
            else:
                kolicina_proizvoda_u_kosarici = 0
        except:
            kolicina_proizvoda_u_kosarici = 0
    return dict(kolicina_proizvoda_u_kosarici=kolicina_proizvoda_u_kosarici)