from django.test import Client

from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_menu(user_1, group_1):
    client = Client()
    client.group = group_1
    client.force_login(user_1)
    url = reverse('societes')
    response = client.get(url)
    assert response.status_code == 403
