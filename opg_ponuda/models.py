from django.db import models
from opg.models import Opg

# Create your models here.
class KategorijeProizvoda(models.Model):
    opg = models.ForeignKey(Opg, on_delete=models.CASCADE)
    naziv_kategorije = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    opis_kategorije = models.TextField(max_length=300, blank=True)
    kreirano = models.DateTimeField(auto_now_add=True)
    izmijenjeno = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.naziv_kategorije
    
    class Meta:
        verbose_name = 'Kategorije proizvoda'
        verbose_name_plural = 'Kategorije proizvoda'

    def clean(self):
        self.naziv_kategorije = self.naziv_kategorije.capitalize()


class Proizvodi(models.Model):
    opg = models.ForeignKey(Opg, on_delete=models.CASCADE)
    kategorija_proizvoda = models.ForeignKey(KategorijeProizvoda, on_delete=models.CASCADE, related_name='proizvodi')
    naziv_proizvoda = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    opis_proizvoda = models.TextField(max_length=300, blank=True)
    cijena_proizvoda = models.DecimalField(max_digits=10, decimal_places=2)
    slika_proizvoda = models.ImageField(upload_to='slike_proizvoda')
    proizvod_dostupan = models.BooleanField(default=True)
    kreirano = models.DateTimeField(auto_now_add=True)
    izmijenjeno = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.naziv_proizvoda
    
    class Meta:
        verbose_name = 'Proizvodi'
        verbose_name_plural = 'Proizvodi'