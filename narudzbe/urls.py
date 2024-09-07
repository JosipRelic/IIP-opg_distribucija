from django.urls import path
from . import views

urlpatterns = [
    path('posalji_narudzbu/', views.posalji_narudzbu, name='posalji_narudzbu'),
    path('placanje/', views.placanje, name='placanje'),
]