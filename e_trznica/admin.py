from django.contrib import admin
from e_trznica.models import Kosarica, Porez

class KosaricaAdmin(admin.ModelAdmin):
    list_display = ('korisnik', 'proizvod', 'kolicina', 'izmijenjeno')

class PorezAdmin(admin.ModelAdmin):
    list_display = ('vrsta_poreza', 'postotak_poreza', 'aktivno')

admin.site.register(Kosarica, KosaricaAdmin)
admin.site.register(Porez, PorezAdmin)