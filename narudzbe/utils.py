import datetime

def generiraj_broj_narudzbe(pk):
    trenutno_vrijeme = datetime.datetime.now().strftime('%d%m%y%H%M')
    broj_narudzbe = trenutno_vrijeme + str(pk)
    return broj_narudzbe
