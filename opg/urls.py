from . import views
from django.urls import path, include
from korisnicki_racuni import views as KorisnickiRacuniViews

urlpatterns = [
    path('', KorisnickiRacuniViews.opg_nadzorna_ploca, name='opg'),
    path('profil/', views.opg_profil, name='opg_profil'),
    path('kreiranje-ponude/', views.kreiranje_ponude, name='kreiranje_ponude'),
    path('kreiranje-ponude/kategorija_proizvoda/<int:pk>/', views.proizvodi_po_kategoriji, name='proizvodi_po_kategoriji')
]
