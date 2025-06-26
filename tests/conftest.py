import pytest
from django.contrib.auth.models import Group
from accounts.models import JadUser


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
