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

def dohvati_iznose_u_kosarici(request):
    ukupna_cijena_proizvoda = 0
    pdv = 0
    ukupan_iznos = 0
    if request.user.is_authenticated:
        proizvodi_u_kosarici = Kosarica.objects.filter(korisnik=request.user)
        for proizvod_u_kosarici in proizvodi_u_kosarici:
            proizvod = Proizvodi.objects.get(pk=proizvod_u_kosarici.proizvod.pk)
            ukupna_cijena_proizvoda +=(proizvod.cijena_proizvoda * proizvod_u_kosarici.kolicina)

        ukupan_iznos = ukupna_cijena_proizvoda + pdv
    return dict(ukupna_cijena_proizvoda=ukupna_cijena_proizvoda, pdv=pdv, ukupan_iznos=ukupan_iznos)