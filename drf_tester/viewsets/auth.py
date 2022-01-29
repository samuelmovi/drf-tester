"""
Collection of classes to be used in the testing of access to a Viewset by an AUTHENTICATED user

"""
from rest_framework import status
from rest_framework.test import force_authenticate

from ..utils import BaseDrfTest

# DISALLOWED BEHAVIOUR


class NoCreate(BaseDrfTest):
    def test_auth_user_cannot_create_instance(self):
        """Authenticated user cannot create new instance"""
        # get user
        user = self.get_active_user(self.user_data)
        # Query endpoint
        request = self.requests.post(self.endpoint, data={})
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NoList(BaseDrfTest):
    def test_auth_user_cannot_list_existing_instance(self):
        """Authenticated user cannot list existing instances"""
        # get user
        user = self.get_active_user(self.user_data)
        # Create instance
        instances = self.get_model_instances()
        # Query endpoint
        request = self.requests.get(self.endpoint, data={})
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NoRetrieve(BaseDrfTest):
    def test_auth_user_cannot_get_existing_instance(self):
        """Authenticated user cannot get details on existing instance.
        Receives 404 HTTP message
        """
        # get user
        user = self.get_active_user(self.user_data)
        # Create instance
        instance = self.factory()
        # Query endpoint
        request = self.requests.get(self.endpoint)
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NoUpdate(BaseDrfTest):
    def test_auth_user_cannot_modify_existing_instance(self):
        """Authenticated user cannot modify existing instance"""
        # get user
        user = self.get_active_user(self.user_data)
        # Create instance
        instance = self.factory()
        # Query endpoint
        request = self.requests.put(self.endpoint, data={})
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NoDestroy(BaseDrfTest):
    def test_auth_user_cannot_delete_existing_instance(self):
        """Authenticated user cannot delete existing instance"""
        # get user
        user = self.get_active_user(self.user_data)
        # Create instances
        instance = self.factory()
        # Query endpoint
        request = self.requests.delete(self.endpoint)
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # Assert access forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Assert instance still exists on db
        self.assertTrue(self.model.objects.filter(id=instance.pk).exists())


# ALLOWED BEHAVIOUR


class CanList(BaseDrfTest):
    def test_auth_user_can_list_instances(self):
        """Authenticated user can list instances"""
        # get user
        user = self.get_active_user(self.user_data)
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


class CanRetrieve(BaseDrfTest):
    def test_auth_user_can_get_instance(self):
        """Authenticated user can get existing instance"""
        # get user
        user = self.get_active_user(self.user_data)
        # Create instances
        instance = self.factory()
        # Request list
        request = self.requests.get(self.endpoint)
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CanCreate(BaseDrfTest):
    def test_auth_user_can_create_instance(self):
        """Authenticated user can create new instance"""
        # get user
        user = self.get_active_user(self.user_data)
        # Query endpoint
        request = self.requests.post(self.endpoint, data=self.instance_data)
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert endpoint returns created status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assert instance exists on db
        self.assertTrue(self.model.objects.filter(id=response.data["id"]).exists())
        self.check_equal_data(self.instance_data, response.data)


class CanUpdate(BaseDrfTest):
    def test_auth_user_can_modify_instance(self):
        """Authenticated user can modify existing instance"""
        # get user
        user = self.get_active_user(self.user_data)
        # Create instances
        instance = self.factory()
        # Query endpoint
        request = self.requests.put(self.endpoint, self.instance_data)
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # Assert endpoint returns OK code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_equal_data(self.instance_data, response.data)


class CanDestroy(BaseDrfTest):
    def test_auth_user_can_delete_instance(self):
        """Authenticated user can delete existing instance"""
        # get user
        user = self.get_active_user(self.user_data)
        # Create instances
        instance = self.factory()
        # Query endpoint
        request = self.requests.delete(self.endpoint)
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # assert 204 no content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Assert instance doesn't exists anymore on db
        self.assertFalse(self.model.objects.filter(id=instance.pk).exists())


class CanPaginate(BaseDrfTest):
    def test_auth_user_can_paginate_instances(self):
        """authenticated user can paginate instances"""
        limit = 5
        offset = 10
        # get user
        user = self.get_active_user(self.user_data)
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
        self.assertTrue(len(payload["results"]) <= 5)


# EXTENDED CLASSES


class AuthFullAccess(CanList, CanRetrieve, CanCreate, CanUpdate, CanDestroy):
    """
    Authenticated user has full access to endopint
    """

    pass


class AuthNoAccess(NoList, NoRetrieve, NoCreate, NoUpdate, NoDestroy):
    """
    Authenticated user has no access to endopint
    """

    pass


class AuthReadOnly(CanList, CanRetrieve, NoCreate, NoUpdate, NoDestroy):
    """
    Authenticated user has only read access to endopint
    """

    pass

