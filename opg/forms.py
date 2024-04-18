from django import forms
from .models import Opg

class FormaOpg(forms.ModelForm):
    class Meta:
        model = Opg
        fields = ['naziv_opga', 'potvrda_opga']
