from django.contrib import admin

from accounts.models import Societe, Magasin, Produit, Stock, Mouvements, JadUser

# Register your models here.
admin.site.register(JadUser)
admin.site.register(Societe)
admin.site.register(Magasin)
admin.site.register(Produit)
admin.site.register(Stock)
admin.site.register(Mouvements)