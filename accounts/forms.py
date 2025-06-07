from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import JadUser, Societe


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
