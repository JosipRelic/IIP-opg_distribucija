from django import forms
from .models import KategorijeProizvoda

class FormaKategorije(forms.ModelForm):
    class Meta:
        model = KategorijeProizvoda
        fields = ['naziv_kategorije', 'opis_kategorije']
        error_messages = {
            'naziv_kategorije': {
                'unique': ("Kategorija već postoji! Kreirajte kategoriju s drugim nazivom."),
            }
        }