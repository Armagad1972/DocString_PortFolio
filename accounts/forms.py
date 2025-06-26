from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import request

from accounts.models import JadUser, Societe, Magasin, Produit


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = JadUser
        fields = ['email', 'fname', 'lname']


class SocieteForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields = ['nom', 'adresse', 'ville', 'pays']
        widgets = {
            'pays': forms.Select(attrs={'class': 'form-control'}),
        }


class MagasinForm(forms.ModelForm):
    class Meta:
        model = Magasin
        fields = ['nom', 'adresse', 'ville', 'pays', 'societe', 'users']
        widgets = {
            'pays': forms.Select(attrs={
                'class': 'form-control',
            }),
            # 'societe': forms.Select(attrs={'class': 'form-control'}),
            'users': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, societe, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["societe"].queryset = Societe.objects.filter(nom=societe)
        self.fields["societe"].disabled = True


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'slug', 'ean', 'societe']
        widgets = {
            'societe': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')  # Extract the request object
        super().__init__(*args, **kwargs)
        if self.request and self.request.user:
            currentuser = self.request.user
            if currentuser.is_superuser:
                soc = Societe.objects.all()
            else:
                soc = Societe.objects.filter(users=currentuser)
            self.fields['societe'].queryset = Societe.objects.filter(id__in=soc.values_list('id', flat=True))
        else:
            self.fields['societe'].queryset = Societe.objects.none()
