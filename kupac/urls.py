from django.urls import path
from korisnicki_racuni import views as korisnickiRacuniViews
from . import views

urlpatterns = [
    path('', korisnickiRacuniViews.kupac_nadzorna_ploca, name = 'kupac'),
    path('profil/', views.kupac_profil, name = 'kupac_profil'),
    path('moje_narudzbe/', views.moje_narudzbe, name ='moje_narudzbe'),
    path('detalji_narudzbe/<str:broj_narudzbe>/', views.detalji_narudzbe, name='detalji_narudzbe')
]