from django.db import models
from korisnicki_racuni.models import User, KorisnickiProfil
from korisnicki_racuni.utils import posalji_obavijest_opg_verifikacija

# Create your models here.

class Opg(models.Model):
    korisnik = models.OneToOneField(User, related_name='korisnik', on_delete=models.CASCADE)
    korisnicki_profil = models.OneToOneField(KorisnickiProfil, related_name='korisnicki_profil', on_delete=models.CASCADE)
    naziv_opga = models.CharField(max_length=100)
    opg_slug = models.SlugField(max_length=100, unique=True)
    potvrda_opga = models.ImageField(upload_to='opg/potvrda')
    opg_verificiran = models.BooleanField(default=False) 
    kreirano = models.DateTimeField(auto_now_add=True)
    izmijenjeno = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.naziv_opga
    
    class Meta:
        verbose_name_plural = 'Opg-ovi'

    def save(self, *args, **kwargs):
        if self.pk is not None:
            #azuriranje
            trenutno_stanje = Opg.objects.get(pk=self.pk)
            if trenutno_stanje.opg_verificiran != self.opg_verificiran:
                email_template = 'korisnicki_racuni/email/verifikacija_opga_admin.html'
                context = {
                    "korisnik": self.korisnik,
                    "opg_verificiran": self.opg_verificiran,
                }
                if self.opg_verificiran == True:
                    #posalji obavijest putem emaila
                    predmet_emaila = "Dobre vijesti! Vaš OPG je verificiran."
                    posalji_obavijest_opg_verifikacija(predmet_emaila, email_template, context)
                else:
                    #posalji obavijest putem emaila
                    predmet_emaila = "Loše vijesti! :( Nažalost, Vaš opg nije prošao verifikaciju."
                    posalji_obavijest_opg_verifikacija(predmet_emaila, email_template, context)


        return super(Opg, self).save(*args, **kwargs)
