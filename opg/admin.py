from django.contrib import admin
from opg.models import Opg

# Register your models here.

class OpgAdmin(admin.ModelAdmin):
    list_display = ('korisnik', 'naziv_opga', 'opg_verificiran', 'kreirano')
    list_display_links = ('korisnik', 'naziv_opga')
    list_editable = ('opg_verificiran',)

admin.site.register(Opg, OpgAdmin)