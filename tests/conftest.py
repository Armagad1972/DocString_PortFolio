import os
import sys
import django
from django.conf import settings

import pytest
from django.contrib.auth.handlers.modwsgi import groups_for_user
from django.contrib.auth.models import Group

from accounts.models import JadUser, Societe, Magasin, Produit, Stock, Mouvements

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DocString_PortFolio.settings')
django.setup()


@pytest.fixture
def user_1(group_1):
    user_1 = JadUser.objects.create_user(email='<valdo@gmail.com>', fname='joe', lname='doe', password='Password123!')
    user_1.save()
    group_1.user_set.add(user_1)
    return user_1


@pytest.fixture
def group_1():
    group_1 = Group.objects.create(name='Magasinier')
    return group_1
