"""
Collection of classes to be used in the testing of access to a Viewset by a SUPER user (Admin)

"""
from rest_framework import status
from rest_framework.test import force_authenticate

from ..utils import BaseDrfTest


class NoList(BaseDrfTest):
    def test_admin_user_cannot_list_existing_instances(self):
        """Admin user cannot list existing instances"""
        # get admin user
        admin_user = self.get_admin_user(self.admin_data)
        # Create instances
        instances = self.get_model_instances()
        # Query endpoint
        request = self.requests.get(self.endpoint, data={})
        force_authenticate(request, user=admin_user)
        response = self.view(request)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoRetrieve(BaseDrfTest):
    def test_admin_user_cannot_get_existing_instance(self):
        """Admin user cannot get details on existing instance"""
        # get admin user
        admin_user = self.get_admin_user(self.admin_data)
        # Create instance
        instance = self.factory()
        # Query endpoint
        request = self.requests.get(self.endpoint, data={})
        force_authenticate(request, user=admin_user)
        response = self.view(request, pk=instance.id)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoCreate(BaseDrfTest):
    def test_admin_user_cannot_create_instance(self):
        """Admin user cannot create new instance"""
        # get admin user
        admin_user = self.get_admin_user(self.admin_data)
        # Query endpoint
        request = self.requests.post(self.endpoint, data={})
        force_authenticate(request, user=admin_user)
        response = self.view(request)
        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoUpdate(BaseDrfTest):
    def test_admin_user_cannot_modify_existing_instance(self):
        """Admin user cannot modify existing instance"""
        # get admin user
        admin_user = self.get_admin_user(self.admin_data)
        # Create instance
        instance = self.factory()
        # Query endpoint
        request = self.requests.put(self.endpoint, data={})
        force_authenticate(request, user=admin_user)
        response = self.view(request, pk=instance.id)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoDestroy(BaseDrfTest):
    def test_admin_user_cannot_delete_existing_instance(self):
        """Admin user cannot delete existing instance"""
        # get admin user
        admin_user = self.get_admin_user(self.admin_data)
        # Create instances
        instance = self.factory()
        # Query endpoint
        request = self.requests.delete(self.endpoint)
        force_authenticate(request, user=admin_user)
        response = self.view(request, pk=instance.id)
        # Assert access forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Assert instance still exists on db
        self.assertTrue(self.model.objects.filter(id=instance.pk).exists())


class CanList(BaseDrfTest):
    def test_admin_user_can_list_instances(self):
        """Admin user can list instances"""
        # get admin user
        admin_user = self.get_admin_user(self.admin_data)
        # Create instances
        instances = self.get_model_instances()
        # Request list
        request = self.requests.get(self.endpoint)
        force_authenticate(request, user=admin_user)
        response = self.view(request)
        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert all instances are returned
        self.assertEqual(len(instances), len(response.data))


class CanRetrieve(BaseDrfTest):
    def test_admin_user_can_get_instance(self):
        """Admin user can get instance"""
        # get admin user
        admin_user = self.get_admin_user(self.admin_data)
        # Create instances
        instance = self.factory()
        # Request list
        request = self.requests.get(self.endpoint)
        force_authenticate(request, user=admin_user)
        response = self.view(request, pk=instance.id)
        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CanCreate(BaseDrfTest):
    def test_admin_user_can_create_instance(self):
        """Admin user can create new instance"""
        # get admin user
        admin_user = self.get_admin_user(self.admin_data)
        # Query endpoint
        request = self.requests.post(self.endpoint, data=self.instance_data)
        force_authenticate(request, user=admin_user)
        response = self.view(request)
        # Assert endpoint returns created status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assert instance exists on db
        self.assertTrue(self.model.objects.filter(id=response.data["id"]).exists())
        self.check_equal_data(self.instance_data, response.data)


class CanUpdate(BaseDrfTest):
    def test_admin_user_can_modify_instance(self):
        """Admin user can modify existing instance"""
        # get admin user
        admin_user = self.get_admin_user(self.admin_data)
        # Create instances
        instance = self.factory()
        # Query endpoint
        request = self.requests.put(self.endpoint, self.instance_data)
        force_authenticate(request, user=admin_user)
        response = self.view(request, pk=instance.id)
        # Assert endpoint returns OK code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_equal_data(self.instance_data, response.data)


class CanDestroy(BaseDrfTest):
    def test_admin_user_can_delete_instance(self):
        """Admin user can delete existing instance"""
        # get admin user
        admin_user = self.get_admin_user(self.admin_data)
        # Create instances
        instance = self.factory()
        # Query endpoint
        request = self.requests.delete(self.endpoint)
        force_authenticate(request, user=admin_user)
        response = self.view(request, pk=instance.id)
        # assert 204 no content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Assert instance doesn't exists anymore on db
        self.assertFalse(self.model.objects.filter(id=instance.pk).exists())


class CanPaginate(BaseDrfTest):
    def test_admin_user_can_paginate_instances(self):
        """Admin user can paginate instances"""
        # get admin user
        admin_user = self.get_admin_user(self.admin_data)
        limit = 5
        offset = 10
        # create instances
        instances = self.get_model_instances()
        # Request list
        url = f"{self.endpoint}?limit={limit}&offset={offset}"
        request = self.requests.get(url)
        force_authenticate(request, user=admin_user)
        response = self.view(request)
        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert only 2 instances in response
        payload = response.json()
        self.assertTrue(len(payload["results"]) <= 5)


# Extended classes


class AdminNoAccess(NoList, NoRetrieve, NoCreate, NoUpdate, NoDestroy):
    """
    Admin user has no access to endopint
    """

    pass


class AdminReadOnly(CanList, CanRetrieve, NoCreate, NoUpdate, NoDestroy):
    """
    Admin user has only read access to endopint
    """

    pass


class AdminFullAccess(CanList, CanRetrieve, CanCreate, CanUpdate, CanDestroy):
    """
    Admin user has full access to endopint
    """

    pass
