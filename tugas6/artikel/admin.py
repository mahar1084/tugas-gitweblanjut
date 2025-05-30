from django.contrib import admin
from artikel.models import Kategori, Artikel

class KategoriAdmin(admin.ModelAdmin):
    list_display = ['nama', 'created_at', 'created_by']
    search_fields = ['nama']

class ArtikelAdmin(admin.ModelAdmin):
    list_display = ['kategori', 'judul', 'created_at','created_by','status']
    search_fields = ['kategori__nama','judul']

admin.site.register(Kategori,KategoriAdmin)
admin.site.register(Artikel, ArtikelAdmin)
