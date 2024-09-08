from django.urls import path
from . import views

urlpatterns = [
    path('posalji_narudzbu/', views.posalji_narudzbu, name='posalji_narudzbu'),
    path('placanje/', views.placanje, name='placanje'),
    path('narudzba_poslana/', views.narudzba_poslana, name='narudzba_poslana')
]