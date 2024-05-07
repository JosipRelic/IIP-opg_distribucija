from . import views
from django.urls import path


urlpatterns = [
    path('registrirajKorisnika/', views.registrirajKorisnika, name='registrirajKorisnika'),
    path('registrirajOpg/', views.registrirajOpg, name='registrirajOpg'),

    path('prijava/', views.prijava, name='prijava'),
    path('odjava/', views.odjava, name='odjava'),
    
    path('mojRacun/', views.mojRacun, name='mojRacun'),
    path('kupac_nadzorna_ploca/', views.kupac_nadzorna_ploca, name='kupac_nadzorna_ploca' ),
    path('opg_nadzorna_ploca/', views.opg_nadzorna_ploca, name='opg_nadzorna_ploca' ),
    
    path('aktiviraj_racun/<uidb64>/<token>/', views.aktiviraj_racun, name='aktiviraj_racun'),

    path('zaboravljena_lozinka/', views.zaboravljena_lozinka, name='zaboravljena_lozinka'),
    path('resetiraj_lozinku_validacija/<uidb64>/<token>/', views.resetiraj_lozinku_validacija, name='resetiraj_lozinku_validacija'),
    path('resetiraj_lozinku/', views.resetiraj_lozinku, name='resetiraj_lozinku')
]
