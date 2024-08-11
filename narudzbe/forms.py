from django import forms
from .models import Narudzba


class FormaNarudzbe(forms.ModelForm):
    class Meta:
        model = Narudzba
        fields = ['ime', 'prezime', 'broj_telefona', 'email', 'adresa', 'drzava', 'zupanija', 'grad', 'postanski_broj']
        widgets = {
            'adresa': forms.TextInput(attrs={'placeholder': ''})
        }