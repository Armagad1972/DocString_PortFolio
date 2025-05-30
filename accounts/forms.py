from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import JadUser


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = JadUser
        fields = ['email', 'fname', 'lname']
