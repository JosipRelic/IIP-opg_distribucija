from django.urls import path
from . import views

urlpatterns = [
    path('', views.e_trznica, name='e_trznica'),  
 
    path('<slug:opg_slug>/', views.pojedinosti_opga, name='pojedinosti_opga'),

    path('dodaj_u_kosaricu/<int:id_proizvoda>/', views.dodaj_u_kosaricu, name='dodaj_u_kosaricu'),
    path('ukloni_iz_kosarice/<int:id_proizvoda>/', views.ukloni_iz_kosarice, name='ukloni_iz_kosarice'),

    path('obrisi_kosaricu/<int:id_kosarice>', views.obrisi_kosaricu, name='obrisi_kosaricu')

]