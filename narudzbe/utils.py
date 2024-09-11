import datetime
import simplejson as json

def generiraj_broj_narudzbe(pk):
    trenutno_vrijeme = datetime.datetime.now().strftime('%d%m%y%H%M')
    broj_narudzbe = trenutno_vrijeme + str(pk)
    return broj_narudzbe


def ukupne_narudzbe_po_opgu(narudzba, opg_id):
    ukupni_podaci = json.loads(narudzba.ukupni_podaci)
    podaci = ukupni_podaci.get(str(opg_id))
    ukupna_cijena_proizvoda = 0
    iznos_poreza = 0
    pdv_dict = {}

    for key,value in podaci.items():
        ukupna_cijena_proizvoda += float(key)
        value = value.replace("'", '"')
        value = json.loads(value)
        pdv_dict.update(value)
        for i in value:
            for j in value[i]:
                iznos_poreza += float(value[i][j])
    ukupno = float(ukupna_cijena_proizvoda) + float(iznos_poreza)
    
    context = {
        'ukupna_cijena_proizvoda': ukupna_cijena_proizvoda,
        'pdv_dict': pdv_dict,
        'ukupno': ukupno
    }
    return context

    """
    opg = Opg.objects.get(korisnik=request_object.user)
    
    ukupna_cijena_proizvoda = 0
    iznos_poreza = 0
    pdv_dict = {}
    
    if self.ukupni_podaci:
        ukupni_podaci = json.loads(self.ukupni_podaci)
        podaci = ukupni_podaci.get(str(opg.id))
        
        
        for key,value in podaci.items():
            ukupna_cijena_proizvoda += float(key)
            value = value.replace("'", '"')
            value = json.loads(value)
            pdv_dict.update(value)
            for i in value:
                for j in value[i]:
                    iznos_poreza += float(value[i][j])
    ukupno = float(ukupna_cijena_proizvoda) + float(iznos_poreza)
    
    context = {
        'ukupna_cijena_proizvoda': ukupna_cijena_proizvoda,
        'pdv_dict': pdv_dict,
        'ukupno': ukupno
    }
    return context
    """