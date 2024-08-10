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
    adresa = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Počnite pisati...', 'required': 'required'}))
    slika_profila = forms.FileField(widget=forms.FileInput(attrs={'class': 'gumb-ucitavanje-slike'}), validators=[dozvoli_samo_slike_validator])
    naslovna_slika = forms.FileField(widget=forms.FileInput(attrs={'class': 'gumb-ucitavanje-slike'}), validators=[dozvoli_samo_slike_validator])

    class Meta: 
        model = KorisnickiProfil
        fields = ['slika_profila', 'naslovna_slika', 'adresa', 'drzava', 'zupanija', 'grad', 'postanski_broj', 'latituda', 'longituda']
 
    def __init__(self, *args, **kwargs):
        super(KorisnickiProfilForma, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latituda' or field == 'longituda':
                self.fields[field].widget.attrs['readonly'] = 'readonly'

class FormaInfoKorisnik(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']