from django import forms
from .models import KategorijeProizvoda

class FormaKategorije(forms.ModelForm):
    class Meta:
        model = KategorijeProizvoda
        fields = ['naziv_kategorije', 'opis_kategorije']