import pytest
from accounts.models import JadUser,Societe,Magasin,Produit,Stock,Mouvements

@pytest.fixture
def user_1():
    return JadUser.objects.create_user(username='valdo',email='<valdo@gmail.com>',password='123456789')
