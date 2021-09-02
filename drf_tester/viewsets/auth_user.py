from rest_framework.test import force_authenticate, APITestCase
from rest_framework import status

from ..utils import BaseDrfTest



class NoList(BaseDrfTest):
    
    def test_auth_user_cannot_list_existing_instance(self):
        """Authenticated user cannot get details on existing instance
        """
        # get user
        user = self.get_active_user()
        # Create instance
        instances = self.get_model_instances()

        # Query endpoint
        url = f'{self.endpoint}'
        request = self.requests.get(url, data={})
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoDetails(BaseDrfTest):
    
    def test_auth_user_cannot_get_existing_instance(self):
        """Authenticated user cannot get details on existing instance
        """
        # get user
        user = self.get_active_user()
        # Create instance
        instance = self.factory()

        # Query endpoint
        url = f'{self.endpoint}{instance.pk}/'
        request = self.requests.get(url, data={})
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoCreate(BaseDrfTest):

    def test_auth_user_cannot_create_instance(self):
        """Authenticated user cannot create new instance
        """
        # get user
        user = self.get_active_user()
        # Query endpoint
        request = self.requests.post(self.endpoint, data={})
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoUpdate(BaseDrfTest):

    def test_auth_user_cannot_modify_existing_instance(self):
        """Authenticated user cannot modify existing instance
        """
        # get user
        user = self.get_active_user()
        # Create instance
        instance = self.factory()

        # Query endpoint
        url = f'{self.endpoint}{instance.pk}/'
        request = self.requests.put(url, data={})
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoDestroy(BaseDrfTest):

    def test_auth_user_cannot_delete_existing_instance(self):
        """Authenticated user cannot delete existing instance
        """
        # get user
        user = self.get_active_user()
        # Create instances
        instance = self.factory()

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        request = self.requests.delete(url)
        force_authenticate(request, user=user)
        response = self.view(request)

        # Assert access forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Assert instance still exists on db
        self.assertTrue(self.model.objects.get(id=instance.pk))


class CanList(BaseDrfTest):
    def test_auth_user_can_list_instances(self):
        """Authenticated user can list instances
        """
        # get user
        user = self.get_active_user()
        # Create instances
        instances = self.get_model_instances()

        # Request list
        request = self.requests.get(self.endpoint)
        force_authenticate(request, user=user)
        response = self.view(request)

        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert all instances are returned
        self.assertEqual(len(instances), len(response.data))


class CanDetail(BaseDrfTest):
    def test_auth_user_can_get_instance(self):
        """Authenticated user can list instance
        """
        # get user
        user = self.get_active_user()
        # Create instances
        instance = self.factory()

        # Request list
        url = f"{self.endpoint}{instance.id}/"
        request = self.requests.get(url)
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CanCreate(BaseDrfTest):
    def test_auth_user_can_create_instance(self):
        """Authenticated user can create new instance
        """
        # get user
        user = self.get_active_user()
        # Query endpoint
        request = self.requests.post(self.endpoint, data=self.instance_data)
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert endpoint returns created status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assert instance exists on db
        self.assertTrue(self.model.objects.filter(id=response.data['id']).exists())


class CanUpdate(BaseDrfTest):
    def test_auth_user_can_modify_instance(self):
        """Authenticated user can modify existing instance
        """
        # get user
        user = self.get_active_user()
        # Create instances
        instance = self.factory()

        # Query endpoint
        url = f'{self.endpoint}{instance.pk}/'
        request = self.requests.put(url, self.instance_data)
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert endpoint returns OK code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert instance has been modified
        for key, value in response.data.items():
            self.assertEqual(self.instance_data[key], value)


class CanDestroy(BaseDrfTest):
    def test_auth_user_can_delete_instance(self):
        """Authenticated user can delete existing instance
        """
        # get user
        user = self.get_active_user()
        # Create instances
        instance = self.factory()

        # Query endpoint
        url = f'{self.endpoint}{instance.pk}/'
        request = self.requests.delete(url)
        force_authenticate(request, user=user)
        response = self.view(request)

        # assert 204 no content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Assert instance doesn't exists anymore on db
        self.assertFalse(self.model.objects.filter(id=instance.pk).exists())


class CanPaginate(BaseDrfTest):
    def test_auth_user_can_paginate_instances(self):
        """authenticated user can paginate instances
        """
        limit = 5
        offset = 10
        # get user
        user = self.get_active_user()
        # create instances
        instances = self.get_model_instances()

        # Request list
        url = f"{self.endpoint}?limit={limit}&offset={offset}"
        request = self.requests.get(url)
        force_authenticate(request, user=user)
        response = self.view(request)

        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert only 2 instances in response
        payload = response.json()
        self.assertTrue( len(payload['results']) <= 5)


# EXTENDED CLASSES

class AuthFullAccess(APITestCase, CanList, CanDetail, CanCreate, CanUpdate, CanDestroy):
    """
    Authenticated user has full access to endopint
    """
    ...


class AuthNoAccess(APITestCase, NoList, NoDetails, NoCreate, NoUpdate, NoDestroy):
    """
    Authenticated user has no access to endopint
    """
    ...


class AuthReadOnly(APITestCase, CanList, CanDetail, NoCreate, NoUpdate, NoDestroy):
    """
    Authenticated user has only read access to endopint
    """
    ...



'''
class IndividualAccess:
    """
    User has wide access to all endopints and the instances created by that user
    """

    def setUp(self):
        self.requests = APIRequestFactory()
        self.endpoint = None
        self.factory = None
        self.model = None
        self.instance_data = {}
        self.alt_data = {}
        self.view = None
        # users
        self.user_data = {}
        self.user = utils.get_active_user(**self.user_data)
        self.other_user_data = {}
        self.user_field_name = ''   # name of table column for instance creator

    def test_auth_user_cannot_modify_other_users_instance(self):
        """Authenticated user cannot modify other user's instance
        """
        # create extra user
        other_user = utils.get_active_user(**self.other_user_data)

        # Create instance owned by other user
        instance = self.factory()
        setattr(instance, self.user_field_name, other_user)

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        request = self.requests.put(url, data=self.alt_data)
        force_authenticate(request, user=self.user)
        response = self.view(request)

        # Assert endpoint returns 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_cannot_delete_other_users_instance(self):
        """Authenticated user cannot delete other user's instance
        """
        # Create instances
        instance = self.factory()
        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        request = self.requests.delete(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.delete(url, format='json')

        # Assert endpoint returns 403 code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

'''

