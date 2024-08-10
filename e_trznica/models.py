from django.db import models
from korisnicki_racuni.models import User
from opg_ponuda.models import Proizvodi

# Create your models here.

class Kosarica(models.Model):
    korisnik = models.ForeignKey(User, on_delete=models.CASCADE)
    proizvod = models.ForeignKey(Proizvodi, on_delete=models.CASCADE)
    kolicina = models.PositiveIntegerField()
    kreirano = models.DateTimeField(auto_now_add=True)
    izmijenjeno = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.korisnik

    class Meta:
        verbose_name = 'kosarica'
        verbose_name_plural = 'kosarica'

class Porez(models.Model):
    vrsta_poreza = models.CharField(max_length=20, unique=True)
    postotak_poreza = models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Postotak poreza (%)')
    aktivno = models.BooleanField(default=True)

    def __str__(self):
        return self.vrsta_poreza
    
    class Meta:
        verbose_name = 'porez'
        verbose_name_plural = 'porezi'