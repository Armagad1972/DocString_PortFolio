from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView

from accounts.forms import UserRegistrationForm, MagasinForm, ProduitForm
from accounts.models import Societe, Magasin, Produit, Stock


# Create your views here.

@login_required
def home(request):
    """
    This is the home view.
    """

    return render(request, 'home.html')


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context['errors'] = form.errors
    else:
        form = UserRegistrationForm()

    return render(request, 'signup.html', context={"form": form})


class SocieteListView(LoginRequiredMixin, ListView):
    """
    View for listing 'Societe' objects with pagination.

    This class-based view lists 'Societe' objects associated with the logged-in user.
    It enforces authentication using the LoginRequiredMixin and enables customizable
    pagination functionality. Users can view a specified number of objects per page.

    Attributes:
        model: Model being queried. Represents the 'Societe' objects in the database.
        template_name: Name of the template used to render the view.
        ordering: List of fields to order the query results by.
        context_object_name: Name of the context variable that holds the queryset.
        paginate_by: Default number of objects displayed on each page.
    """
    model = Societe
    template_name = 'societe.html'
    ordering = ['nom']
    context_object_name = 'societes'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Societe.objects.all().order_by(*self.ordering)
        else:
            user_societes = Societe.objects.filter(users=self.request.user) # Optimisation une requête
            if user_societes.exists(): # Utilisation de exists() pour vérifier l'existence
                # Redis moi si c'est bien ça que tu attendais
                return user_societes.order_by(*self.ordering)
            else:
                self.request.user.user_permissions.none()
                return Societe.objects.none()

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Magasinier').exists():
            return render(request, '403.html', status=403)
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return self.template_name


class MagasinListView(LoginRequiredMixin, ListView):
    """
    MagasinListView provides a view for listing Magasin objects restricted by user access.

    This class-based view leverages Django's ListView framework to display a
    list of Magasin objects that are filtered based on the current user's
    associated Societe. It ensures that only authorized users can access this
    view and dynamically manages pagination.

    Attributes:
    model: The model associated with the view, which in this case is Magasin.
    template_name (str): The path to the HTML template used for rendering the view.
    context_object_name (str): The name of the context variable that holds the list
        of Magasin objects in the template.
    ordering (list): Specifies the default ordering of Magasin objects based on
        the `societe` attribute.

    Methods:

    get_queryset:
        Returns a filtered QuerySet of Magasin objects for the currently
        authenticated user.

    get_paginate_by:
        Returns the number of items per page for pagination, dynamically
        determined from the request (15 by default).
    """
    model = Magasin
    template_name = 'magasin.html'
    context_object_name = 'magasins'
    ordering = ['societe']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Magasin.objects.all().order_by(*self.ordering)
        elif self.request.user.groups.filter(name='Propriétaire').exists():
            soc = Societe.objects.get(users=self.request.user)
            return Magasin.objects.filter(societe=soc).order_by(*self.ordering)
        else:
            return Magasin.objects.filter(users=self.request.user).order_by(*self.ordering)

    def get_paginate_by(self, queryset):
        # Dynamically set items per page, e.g., based on a query parameter
        return self.request.GET.get('items_per_page', int(12))


class MagasinUpdateView(UpdateView):
    """
    MagasinListView provides a view for listing Magasin objects restricted by user access.
    """
    model = Magasin
    form_class = MagasinForm
    template_name = 'magasin_update.html'
    success_url = reverse_lazy('magasins') # Utilise reverse pour obtenir l'URL de succès


class ProduitsListView(LoginRequiredMixin, ListView):
    """
    MagasinListView provides a view for listing Magasin objects restricted by user access.

    This class-based view leverages Django's ListView framework to display a
    list of Magasin objects that are filtered based on the current user's
    associated Societe. It ensures that only authorized users can access this
    view and dynamically manages pagination.

    Attributes:
    model: The model associated with the view, which in this case is Magasin.
    template_name (str): The path to the HTML template used for rendering the view.
    context_object_name (str): The name of the context variable that holds the list
        of Magasin objects in the template.
    ordering (list): Specifies the default ordering of Magasin objects based on
        the `societe` attribute.

    Methods:

    get_queryset:
        Returns a filtered QuerySet of Magasin objects for the currently
        authenticated user.

    get_paginate_by:
        Returns the number of items per page for pagination, dynamically
        determined from the request (15 by default).
    """
    model = Produit
    template_name = 'produit.html'
    context_object_name = 'produits'
    ordering = ['societe']

    def get_queryset(self, *args, **kwargs):

        if self.request.user.is_superuser:
            return Produit.objects.all().order_by(*self.ordering)
        elif self.request.user.groups.filter(name='Propriétaire').exists():
            soc = Societe.objects.get(users=self.request.user)
            return Produit.objects.filter(societe=soc).order_by(*self.ordering)
        else:
            mag = Magasin.objects.filter(users=self.request.user).first()
            soc = Societe.objects.get(magasins=mag)
            return Produit.objects.filter(societe=soc).order_by(*self.ordering)

    def get_paginate_by(self, queryset):
        # Dynamically set items per page, e.g., based on a query parameter
        return self.request.GET.get('items_per_page', int(12))


class ProduitUpdateView(UpdateView):
    """
    MagasinListView provides a view for listing Magasin objects restricted by user access.
    """
    model = Produit
    form_class = ProduitForm
    template_name = 'produit_update.html'
    success_url = reverse_lazy('produits')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class StocksListView(LoginRequiredMixin, ListView):
    """
    MagasinListView provides a view for listing Magasin objects restricted by user access.

    This class-based view leverages Django's ListView framework to display a
    list of Magasin objects that are filtered based on the current user's
    associated Societe. It ensures that only authorized users can access this
    view and dynamically manages pagination.

    Attributes:
    model: The model associated with the view, which in this case is Magasin.
    template_name (str): The path to the HTML template used for rendering the view.
    context_object_name (str): The name of the context variable that holds the list
        of Magasin objects in the template.
    ordering (list): Specifies the default ordering of Magasin objects based on
        the `societe` attribute.

    Methods:

    get_queryset:
        Returns a filtered QuerySet of Magasin objects for the currently
        authenticated user.

    get_paginate_by:
        Returns the number of items per page for pagination, dynamically
        determined from the request (15 by default).
    """
    model = Stock
    template_name = 'stock.html'
    context_object_name = 'stocks'
    ordering = ['produit']

    def get_queryset(self, *args, **kwargs):

        if self.request.user.is_superuser:
            return Stock.objects.all().order_by(*self.ordering)
        elif self.request.user.groups.filter(name='Propriétaire').exists():
            soc = Societe.objects.get(users=self.request.user)
            magasins = Magasin.objects.filter(societe=soc)
            return Stock.objects.filter(magasin__in=magasins).order_by(*self.ordering)
        else:
            mag = Magasin.objects.filter(users=self.request.user)
            return Stock.objects.filter(magasin__in=mag).order_by(*self.ordering)

    def get_paginate_by(self, queryset):
        # Dynamically set items per page, e.g., based on a query parameter
        return self.request.GET.get('items_per_page', int(12))
