from django import forms
from .models import KategorijeProizvoda, Proizvodi
from korisnicki_racuni.validators import dozvoli_samo_slike_validator

class FormaKategorije(forms.ModelForm):
    class Meta:
        model = KategorijeProizvoda
        fields = ['naziv_kategorije', 'opis_kategorije']
        error_messages = {
            'naziv_kategorije': {
                'unique': ("Kategorija već postoji! Kreirajte kategoriju s drugim nazivom."),
            }
        }

class FormaProizvodi(forms.ModelForm):
    slika_proizvoda= forms.FileField(widget=forms.FileInput(attrs={'class': 'gumb-ucitavanje-slike'}), validators=[dozvoli_samo_slike_validator])
    class Meta:
        model = Proizvodi
        fields = ['kategorija_proizvoda', 'naziv_proizvoda', 'opis_proizvoda', 'cijena_proizvoda', 'slika_proizvoda', 'proizvod_dostupan']