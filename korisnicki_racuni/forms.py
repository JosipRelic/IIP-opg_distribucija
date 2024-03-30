from django import forms
from .models import User

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
        