from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Morate unijeti email adresu')
        if not username:
            raise ValueError('Morate unijeti korisnicko ime')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    OPG = 1
    KUPAC = 2

    ROLE_CHOICE = (
        (OPG, 'opg'),
        (KUPAC, 'kupac'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    #zahtjevana polja
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'opg'
        elif self.role == 2:
            user_role = 'kupac'
        return user_role        

    class Meta:
        verbose_name = 'korisnik'
        verbose_name_plural = 'korisnici'


class KorisnickiProfil(models.Model):
    korisnik = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    slika_profila = models.ImageField(upload_to='korisnici/slike_profila', blank=True, null=True)
    naslovna_slika = models.ImageField(upload_to='korisnici/naslovne_slike', blank=True, null=True)
    adresa = models.CharField(max_length=300, blank=True, null=True)
    drzava = models.CharField(max_length=100, blank=True, null=True)
    zupanija = models.CharField(max_length=100, blank=True, null=True)
    grad = models.CharField(max_length=100, blank=True, null=True)
    postanski_broj = models.CharField(max_length=8, blank=True, null=True)
    latituda = models.CharField(max_length=50, blank=True, null=True)
    longituda = models.CharField(max_length=50, blank=True, null=True)
    lokacija = gismodels.PointField(blank=True, null=True, srid=4326)
    kreirano = models.DateTimeField(auto_now_add=True)
    izmijenjeno = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.korisnik.email

    class Meta:
        verbose_name = 'korisnicki profil'
        verbose_name_plural = 'korisnicki profili'

    def save(self, *args, **kwargs):
        if self.latituda and self.longituda:
            self.lokacija = Point(float(self.longituda), float(self.latituda))
            return super(KorisnickiProfil, self).save(*args, **kwargs)
        return super(KorisnickiProfil, self).save(*args, **kwargs)




