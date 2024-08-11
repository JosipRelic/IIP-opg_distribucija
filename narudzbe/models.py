from django.db import models
from korisnicki_racuni.models import User
from opg_ponuda.models import Proizvodi


# Create your models here.

class Placanje(models.Model):
    OPCIJE_PLACANJA = (
        ('PayPal', 'PayPal'),
    )
    korisnik = models.ForeignKey(User, on_delete=models.CASCADE)
    id_transakcije = models.CharField(max_length=100)
    nacin_placanja = models.CharField(choices=OPCIJE_PLACANJA, max_length=100)
    iznos = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    kreirano = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_transakcije
    
    class Meta:
        verbose_name = 'Placanje'
        verbose_name_plural = 'Placanja'
    
class Narudzba(models.Model):
    STATUS_NARUDZBE = (
        ('U tijeku', 'U tijeku'),
        ('Prihvaćena', 'Prihvaćena'),
        ('Završena', 'Završena'),
        ('Otkazana', 'Otkazana'),
    )

    korisnik = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    placanje = models.ForeignKey(Placanje, on_delete=models.SET_NULL, blank=True, null=True)
    broj_narudzbe = models.CharField(max_length=20)
    ime = models.CharField(max_length=50)
    prezime = models.CharField(max_length=50)
    broj_telefona = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    adresa = models.CharField(max_length=200)
    drzava = models.CharField(max_length=50, blank=True)
    zupanija = models.CharField(max_length=50, blank=True)
    grad = models.CharField(max_length=50)
    postanski_broj = models.CharField(max_length=10)
    ukupno = models.FloatField()
    porezni_podaci = models.JSONField(blank=True, help_text= "Format podataka: {'vrsta_poreza':{'postotak_poreza':'iznos_poreza'}}")
    ukupno_poreza = models.FloatField()
    nacin_placanja = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS_NARUDZBE, default='U tijeku')
    naruceno = models.BooleanField(default=False)
    kreirano = models.DateTimeField(auto_now_add=True)
    izmijenjeno = models.DateTimeField(auto_now=True)

    @property
    def ime_i_prezime(self):
        return f'{self.ime} {self.prezime}'
    
    def __str__(self):
        return self.broj_narudzbe
    
    class Meta:
        verbose_name = 'Narudzba'
        verbose_name_plural = 'Narudzbe'


class NaruceniProizvodi(models.Model):
    narudzba = models.ForeignKey(Narudzba, on_delete=models.CASCADE)
    placanje = models.ForeignKey(Placanje, on_delete=models.SET_NULL, blank=True, null=True)
    korisnik = models.ForeignKey(User, on_delete=models.CASCADE)
    proizvod = models.ForeignKey(Proizvodi, on_delete=models.CASCADE)
    kolicina = models.IntegerField()
    cijena = models.FloatField()
    iznos = models.FloatField()
    kreirano = models.DateTimeField(auto_now_add=True)
    izmijenjeno = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.proizvod.naziv_proizvoda
    
    class Meta:
        verbose_name = 'Naruceni proizvod'
        verbose_name_plural = 'Naruceni proizvodi'