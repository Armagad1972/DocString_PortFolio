from .models import Societe, Magasin, Produit
from import_export import resources


class SocieteResource(resources.ModelResource):
    class Meta:
        model = Societe


class MagasinResource(resources.ModelResource):
    class Meta:
        model = Magasin


class ProduitResource(resources.ModelResource):
    class Meta:
        model = Produit
