from django.contrib import admin
from .models import Societe, Magasin, Produit, Stock, Mouvements, JadUser
from .resources import SocieteResource, MagasinResource, ProduitResource
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(JadUser)

admin.site.register(Stock)

admin.site.register(Mouvements)


@admin.register(Societe)
class SocieteAdmin(ImportExportModelAdmin):
    resource_class = SocieteResource
    list_display = ['id', 'nom', 'adresse', 'ville', 'pays']


@admin.register(Magasin)
class MagasinAdmin(ImportExportModelAdmin):
    resource_class = MagasinResource
    list_display = ['id', 'nom', 'adresse', 'ville', 'pays', 'societe']


@admin.register(Produit)
class ProduitAdmin(ImportExportModelAdmin):
    resource_class = ProduitResource
    list_display = ['id', 'nom', 'slug', 'CreationDate', 'UpdateDate']
