from django.shortcuts import render
# Create your views here.

def opg_profil(request):
    return render(request, 'opg/opg_profil.html')
