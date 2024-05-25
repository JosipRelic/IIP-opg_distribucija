from django.core.exceptions import ValidationError
import os

def dozvoli_samo_slike_validator(value):
    ext = os.path.splitext(value.name)[1] #prikupljanje ekstenzije datoteke npr. slika.png [1] je druga vrijednost u listi
    print(ext)
    dozvoljene_ext = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in dozvoljene_ext:
        raise ValidationError('Nepodržani format slike! Učitajte neki od podržanih formata: png, jpg, jpeg')