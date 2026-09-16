from django.contrib.auth.models import User
from store.models import Collection
from rest_framework import status
from model_bakery import baker
import pytest

@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post('/store/collections/', {'title': 'a'})

        # assert checks to see if the behavior i expect happens, in this case the 401 response
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client):
        api_client.force_authenticate(user={}) # to authenticate the user i call and set user to an empty dictionary
        response = api_client.post('/store/collections/', {'title': 'a'})

        # assert checks to see if the behavior i expect happens, in this case the 403 response
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, api_client, authenticate):
        authenticate()

        response = api_client.post('/store/collections/', {'title': ''})

        # assert checks to see if the behavior i expect happens, in this case the 400 response
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_201(self, api_client, authenticate):
        authenticate(is_staff=True)
        
        response = api_client.post('/store/collections/', {'title': 'a'})

        # assert checks to see if the behavior i expect happens, in this case the 201 response
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)

        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }

