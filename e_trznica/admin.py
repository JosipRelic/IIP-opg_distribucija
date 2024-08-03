from django.contrib import admin
from e_trznica.models import Kosarica

class KosaricaAdmin(admin.ModelAdmin):
    list_display = ('korisnik', 'proizvod', 'kolicina', 'izmijenjeno')

admin.site.register(Kosarica, KosaricaAdmin)