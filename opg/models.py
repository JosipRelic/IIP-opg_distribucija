from django.db import models
from korisnicki_racuni.models import User, KorisnickiProfil

# Create your models here.

class Opg(models.Model):
    korisnik = models.OneToOneField(User, related_name='korisnik', on_delete=models.CASCADE)
    korisnicki_profil = models.OneToOneField(KorisnickiProfil, related_name='korisnicki_profil', on_delete=models.CASCADE)
    naziv_opga = models.CharField(max_length=100)
    potvrda_opga = models.ImageField(upload_to='opg/potvrda')
    opg_verificiran = models.BooleanField(default=False) 
    kreirano = models.DateTimeField(auto_now_add=True)
    izmijenjeno = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.naziv_opga
    
    class Meta:
        verbose_name_plural = 'Opg-ovi'