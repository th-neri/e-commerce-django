from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest

# using fixture/reusable functions to get rid of repetitive lines. all i have to do is add it to every test as a parameter
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False): # initializing is_staff as False
        return api_client.force_authenticate(user=User(is_staff=True)) # to authenticate the user to an user object that is an admin
    return do_authenticate