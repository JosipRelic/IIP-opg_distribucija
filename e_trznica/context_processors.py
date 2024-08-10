from .models import Kosarica, Porez
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
    pdv_dict = {}
    if request.user.is_authenticated:
        proizvodi_u_kosarici = Kosarica.objects.filter(korisnik=request.user)
        for proizvod_u_kosarici in proizvodi_u_kosarici:
            proizvod = Proizvodi.objects.get(pk=proizvod_u_kosarici.proizvod.pk)
            ukupna_cijena_proizvoda +=(proizvod.cijena_proizvoda * proizvod_u_kosarici.kolicina)
        
        dohvati_porez = Porez.objects.filter(aktivno=True)
        for i in dohvati_porez:
            vrsta_poreza = i.vrsta_poreza
            postotak_poreza = i.postotak_poreza
            iznos_poreza = round((ukupna_cijena_proizvoda * postotak_poreza)/100, 2)
            pdv_dict.update({vrsta_poreza : {str(postotak_poreza) : iznos_poreza}})
            
        #PDV {'PDV': {'25.00':'0.65'}}
        pdv = 0
        pdv = sum(x for key in pdv_dict.values() for x in key.values())

        ukupan_iznos = ukupna_cijena_proizvoda + pdv
    return dict(ukupna_cijena_proizvoda=ukupna_cijena_proizvoda, pdv=pdv, ukupan_iznos=ukupan_iznos, pdv_dict=pdv_dict)