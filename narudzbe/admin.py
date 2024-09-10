from django.contrib import admin
from .models import Placanje, Narudzba, NaruceniProizvodi

class NaruceniProizvodiInline(admin.TabularInline):
    model = NaruceniProizvodi
    readonly_fields = ('narudzba', 'placanje', 'korisnik', 'proizvod', 'kolicina', 'cijena', 'iznos')
    extra = 0

class NarudzbaAdmin(admin.ModelAdmin):
    list_display = ['broj_narudzbe', 'ime', 'prezime', 'broj_telefona', 'email', 'nacin_placanja', 'status','narudzba_poslana_za', 'naruceno', 'ukupno' ]
    inlines = [NaruceniProizvodiInline]

admin.site.register(Placanje)
admin.site.register(Narudzba, NarudzbaAdmin)
admin.site.register(NaruceniProizvodi)

