from django import forms
from .models import Opg
from korisnicki_racuni.validators import dozvoli_samo_slike_validator

class FormaOpg(forms.ModelForm):
    potvrda_opga = forms.FileField(widget=forms.FileInput(attrs={'class': 'gumb-ucitavanje-slike'}), validators=[dozvoli_samo_slike_validator])
    class Meta:
        model = Opg
        fields = ['naziv_opga', 'potvrda_opga']
