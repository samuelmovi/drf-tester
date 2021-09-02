from rest_framework.test import APITestCase
from rest_framework import status

from ..utils import BaseDrfTest


class NoList(BaseDrfTest):
    
    def test_anon_user_cannot_list_existing_instance(self):
        """Anonymous user cannot get details on existing instance
        """
        # Create instance
        instances = self.get_model_instances()

        # Query endpoint
        url = f'{self.endpoint}'
        request = self.requests.get(url, data={})
        response = self.view(request)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoDetails(BaseDrfTest):
    
    def test_anon_user_cannot_get_existing_instance(self):
        """Anonymous user cannot get details on existing instance
        """
        # Create instance
        instance = self.factory()

        # Query endpoint
        url = f'{self.endpoint}{instance.pk}/'
        request = self.requests.get(url, data={})
        response = self.view(request)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoCreate(BaseDrfTest):

    def test_anon_user_cannot_create_instance(self):
        """Anonymous user cannot create new instance
        """
        # Query endpoint
        request = self.requests.post(self.endpoint, data={})
        response = self.view(request)
        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoUpdate(BaseDrfTest):

    def test_anon_user_cannot_modify_existing_instance(self):
        """Anonymous user cannot modify existing instance
        """
        # Create instance
        instance = self.factory()

        # Query endpoint
        url = f'{self.endpoint}{instance.pk}/'
        request = self.requests.put(url, data={})
        response = self.view(request)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoDestroy(BaseDrfTest):

    def test_anon_user_cannot_delete_existing_instance(self):
        """Anonymous user cannot delete existing instance
        """
        # Create instances
        instance = self.factory()

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        request = self.requests.delete(url)
        response = self.view(request)

        # Assert access forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Assert instance still exists on db
        self.assertTrue(self.model.objects.get(id=instance.pk))


class CanList(BaseDrfTest):
    def test_anon_user_can_list_instances(self):
        """Anonymous user can list instances
        """
        # create instances
        expected_instances = self.get_model_instances()
        # Request list
        request = self.requests.get(self.endpoint)
        response = self.view(request)

        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()
        # Assert number of instances in response
        self.assertEquals(len(expected_instances), len(payload))


class CanDetail(BaseDrfTest):
    def test_anon_user_can_get_instances(self):
        """Anonymous user can list instances
        """
        # create instances
        instance = self.factory()
        # Request list
        url = f'{self.endpoint}{instance.pk}/'
        request = self.requests.get(url)
        response = self.view(request)

        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CanCreate(BaseDrfTest):
    def test_anon_user_can_create_instance(self):
        """Anonymous user can create new instance
        """
        # Query endpoint
        request = self.requests.post(self.endpoint, data=self.instance_data)
        response = self.view(request)
        # Assert instance is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.model.objects.get(id=response.data.instance.pk))


class CanUpdate(BaseDrfTest):
    def test_anon_user_can_modify_existing_instance(self):
        """Anonymous user can modify existing instance
        """
        # Create instance
        instance = self.factory()

        # Query endpoint
        url = f'{self.endpoint}{instance.pk}/'
        request = self.requests.put(url, data=self.instance_data)
        response = self.view(request)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CanDestroy(BaseDrfTest):
    def test_anon_user_can_delete_existing_instance(self):
        """Anonymous user can delete existing instance
        """
        # Create instances
        instance = self.factory()

        # Query endpoint
        url = f'{self.endpoint}{instance.pk}/'
        request = self.requests.delete(url)
        response = self.view(request)

        # Assert access forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Assert instance still exists on db
        self.assertTrue(self.model.objects.filter(id=instance.pk).exists())


# Extended classes

class AnonNoAccess(APITestCase, NoList, NoDetails, NoCreate, NoUpdate, NoDestroy):
    """
    Anonymous user has no access to endopint
    """
    ...



class AnonReadOnly(APITestCase, CanList, CanDetail, NoCreate, NoUpdate, NoDestroy):
    """
    Anonymous user has only read access to endopint
    """
    ...



class AnonFullAccess(APITestCase, CanList, CanDetail, CanCreate, CanUpdate, CanDestroy):
    """
    Anonymous user has full access to endopint
    """
    ...


