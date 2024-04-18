from . import views
from django.urls import path


urlpatterns = [
    path('registrirajKorisnika/', views.registrirajKorisnika, name='registrirajKorisnika'),
    path('registrirajOpg/', views.registrirajOpg, name='registrirajOpg'),
]
