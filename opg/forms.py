from django import forms
from .models import Opg

class FormaOpg(forms.ModelForm):
    potvrda_opga = forms.ImageField(widget=forms.FileInput(attrs={'class': 'gumb-ucitavanje-slike'}))
    class Meta:
        model = Opg
        fields = ['naziv_opga', 'potvrda_opga']
