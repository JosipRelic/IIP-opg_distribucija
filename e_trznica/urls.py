from django.urls import path
from . import views

urlpatterns = [
    path('', views.e_trznica, name='e_trznica'),  
]