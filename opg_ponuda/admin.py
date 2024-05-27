from django.contrib import admin
from .models import KategorijeProizvoda, Proizvodi

class KategorijeProizvodaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('naziv_kategorije',)}
    list_display = ('naziv_kategorije', 'opg', 'izmijenjeno',)
    search_fields = ('naziv_kategorije', 'opg__naziv_opga',)


class ProizvodiAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('naziv_proizvoda',)}
    list_display = ('naziv_proizvoda', 'kategorija_proizvoda', 'opg', 'cijena_proizvoda', 'proizvod_dostupan', 'izmijenjeno',)
    search_fields = ('naziv_proizvoda', 'kategorija_proizvoda__naziv_kategorije', 'opg__naziv_opga', 'cijena_proizvoda',)
    list_filter = ('proizvod_dostupan',)


admin.site.register(KategorijeProizvoda, KategorijeProizvodaAdmin)
admin.site.register(Proizvodi, ProizvodiAdmin)