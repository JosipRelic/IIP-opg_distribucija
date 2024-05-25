from django import forms
from .models import User, KorisnickiProfil
from .validators import dozvoli_samo_slike_validator

class FormaKorisnik(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        error_messages = {
            'username': {
                'unique': ("Korisničko ime zauzeto! Unesite drugo."),
            },
            'email':{
                'unique': ("Email zauzet! Unesite drugi."),
            }
        }
    
    def clean(self):
        cleaned_data = super(FormaKorisnik, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Lozinke se ne podudaraju!"
            )

class KorisnickiProfilForma(forms.ModelForm):
    slika_profila = forms.FileField(widget=forms.FileInput(attrs={'class': 'gumb-ucitavanje-slike'}), validators=[dozvoli_samo_slike_validator])
    naslovna_slika = forms.FileField(widget=forms.FileInput(attrs={'class': 'gumb-ucitavanje-slike'}), validators=[dozvoli_samo_slike_validator])
    class Meta: 
        model = KorisnickiProfil
        fields = ['slika_profila', 'naslovna_slika', 'adresa_1', 'adresa_2', 'drzava', 'zupanija', 'grad', 'postanski_broj', 'latituda', 'longituda']