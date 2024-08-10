from django.urls import path
from korisnicki_racuni import views as korisnickiRacuniViews
from . import views

urlpatterns = [
    path('', korisnickiRacuniViews.kupac_nadzorna_ploca, name = 'kupac'),
    path('profil/', views.kupac_profil, name = 'kupac_profil'),
]