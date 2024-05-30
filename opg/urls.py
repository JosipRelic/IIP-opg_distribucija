from . import views
from django.urls import path, include
from korisnicki_racuni import views as KorisnickiRacuniViews

urlpatterns = [
    path('', KorisnickiRacuniViews.opg_nadzorna_ploca, name='opg'),
    path('profil/', views.opg_profil, name='opg_profil'),
    path('kreiranje-ponude/', views.kreiranje_ponude, name='kreiranje_ponude'),
    path('kreiranje-ponude/kategorija_proizvoda/<int:pk>/', views.proizvodi_po_kategoriji, name='proizvodi_po_kategoriji'),

    path('kreiranje-ponude/kategorija_proizvoda/dodaj_kategoriju/', views.dodaj_kategoriju, name='dodaj_kategoriju'),
    path('kreiranje-ponude/kategorija_proizvoda/uredi_kategoriju/<int:pk>/', views.uredi_kategoriju, name='uredi_kategoriju'),
    path('kreiranje-ponude/kategorija_proizvoda/obrisi_kategoriju/<int:pk>/', views.obrisi_kategoriju, name='obrisi_kategoriju'),

    path('kreiranje-ponude/proizvod/dodaj_proizvod/', views.dodaj_proizvod, name='dodaj_proizvod'),
    path('kreiranje-ponude/proizvod/uredi_proizvod/<int:pk>/', views.uredi_proizvod, name='uredi_proizvod'),
    path('kreiranje-ponude/proizvod/obrisi_proizvod/<int:pk>/', views.obrisi_proizvod, name='obrisi_proizvod'),
]
