from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, KorisnickiProfil


#@receiver(post_save, sender=User)
#def kreiraj_profil_post_save_receiver(sender, instance, created, **kwargs):
#    print(created)
#    if created:
#        KorisnickiProfil.objects.create(korisnik=instance)
#    else:
#        try:
#            profil = KorisnickiProfil.objects.get(korisnik=instance) 
#            profil.save()
#        except:
#            # kreiraj korisnicki profil ukoliko ne postoji
#            KorisnickiProfil.objects.create(korisnik=instance)
#        print('korisnik je azuriran')


@receiver(pre_save, sender=User)
def kreiraj_profil_pre_save_receiver(sender, instance, **kwargs):
    pass

#post_save.connect(kreiraj_profil_post_save_receiver, sender=User)