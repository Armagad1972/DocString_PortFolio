from django.contrib import admin

from accounts.models import Societe, Magasin, Produit

# Register your models here.
admin.site.register(Societe)
admin.site.register(Magasin)
admin.site.register(Produit)