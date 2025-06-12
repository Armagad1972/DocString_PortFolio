"""
URL configuration for DocString_PortFolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import detail

from accounts.views import SocieteListView, MagasinListView, ProduitsListView, MagasinUpdateView, ProduitUpdateView
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('societes/', SocieteListView.as_view(), name="societes"),
    path('magasins/', MagasinListView.as_view(), name="magasins"),
    path('magasin/<int:pk>/edit', MagasinUpdateView.as_view(model=views.Magasin), name="magasin_edit"),
    path('produits/', ProduitsListView.as_view(), name="produits"),
    path('produits/<int:pk>/edit', ProduitUpdateView.as_view(model=views.Produit), name="produit_edit"),
]
