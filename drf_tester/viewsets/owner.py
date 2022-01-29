"""

"""
from rest_framework import status
from rest_framework.test import force_authenticate

from ..utils import BaseDrfTest

# DISALLOWED

class NoListOwned(BaseDrfTest):
    def test_auth_user_cannot_list_owned_instance(self):
        """Authenticated user cannot list instances owned by different user."""
        # create some user
        some_user = self.user_factory()
        # Create instance
        instances = self.get_model_instances()
        for x in instances:
            setattr(x, self.USER_FIELD_NAME, some_user)
            x.save()
        # get user
        user = self.get_active_user(self.user_data)
        # Query endpoint
        request = self.requests.get(self.endpoint)
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class NoRetrieveOwned(BaseDrfTest):
    def test_auth_user_cannot_get_owned_instance(self):
        """Authenticated user cannot get details on other user's instance."""
        # create some user
        some_user = self.user_factory()
        # Create instance
        instance = self.factory(creator=some_user)
        # get user
        user = self.get_active_user(self.user_data)
        # Query endpoint
        request = self.requests.get(self.endpoint)
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # TODO: this call doesn't trigger get_object in view ?!?!?
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NoUpdateOwned(BaseDrfTest):
    def test_auth_user_cannot_modify_owned_instance(self):
        """Authenticated user cannot modify another user's instance."""
        # create some user
        some_user = self.user_factory()
        # Create instance
        instance = self.factory()
        setattr(instance, self.USER_FIELD_NAME, some_user)
        instance.save()
        # get user
        user = self.get_active_user(self.user_data)
        # Query endpoint
        request = self.requests.put(self.endpoint, data={})
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # Assert forbidden access
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NoDestroyOwned(BaseDrfTest):
    def test_auth_user_cannot_delete_owned_instance(self):
        """Authenticated user cannot delete owned instance"""
        other_user = self.user_factory()
        # Create instances
        instance = self.factory()
        setattr(instance, self.USER_FIELD_NAME, other_user)
        instance.save()
        # Query endpoint
        request = self.requests.delete(self.endpoint)
        # get user
        user = self.get_active_user(self.user_data)
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # Assert access forbidden
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Assert instance still exists on db
        self.assertTrue(self.model.objects.filter(id=instance.pk).exists())

# ALLOWED

class CanListOwned(BaseDrfTest):
    def test_auth_user_can_list_owned_instances(self):
        """Authenticated user can list owned instances"""
        # get user
        user = self.get_active_user(self.user_data)
        # Create instances
        instances = self.get_model_instances()
        for x in instances:
            setattr(x, self.USER_FIELD_NAME, user)
            x.save()
        # Request list
        request = self.requests.get(self.endpoint)
        force_authenticate(request, user=user)
        response = self.view(request)
        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert all instances are returned
        self.assertEqual(len(instances), len(response.data))


class CanRetrieveOwned(BaseDrfTest):
    def test_auth_user_can_get_owned_instance(self):
        """Authenticated user can get owned instance"""
        # get user
        user = self.get_active_user(self.user_data)
        # Create instances
        instance = self.factory()
        setattr(instance, self.USER_FIELD_NAME, user)
        instance.save()
        # Request list
        request = self.requests.get(self.endpoint)
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CanCreateOwned(BaseDrfTest):
    def test_auth_user_can_create_owned_instance(self):
        """Authenticated user can create new owned instance.

        Requires endpoint to add authenticated user to object model.
        """
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
        # assert owner properly set
        self.assertEqual(response.data[self.USER_FIELD_NAME], user.id)
        self.check_equal_data(self.instance_data, response.data)


class CanUpdateOwned(BaseDrfTest):
    def test_auth_user_can_modify_owned_instance(self):
        """Authenticated user can modify owned instance"""
        # get user
        user = self.get_active_user(self.user_data)
        # Create instances
        instance = self.factory()
        setattr(instance, self.USER_FIELD_NAME, user)
        instance.save()
        # Query endpoint
        request = self.requests.put(self.endpoint, self.instance_data)
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # Assert endpoint returns OK code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[self.USER_FIELD_NAME], user.id)
        self.check_equal_data(self.instance_data, response.data)


class CanDestroyOwned(BaseDrfTest):
    def test_auth_user_can_delete_owned_instance(self):
        """Authenticated user can delete owned instance"""
        # get user
        user = self.get_active_user(self.user_data)
        # Create instances
        instance = self.factory()
        setattr(instance, self.USER_FIELD_NAME, user)
        instance.save()
        # Query endpoint
        request = self.requests.delete(self.endpoint)
        force_authenticate(request, user=user)
        response = self.view(request, pk=instance.id)
        # assert 204 no content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Assert instance doesn't exists anymore on db
        self.assertFalse(self.model.objects.filter(id=instance.pk).exists())


# COLLECTIONS

class AuthOwner(CanListOwned, CanRetrieveOwned, CanCreateOwned, CanUpdateOwned, CanDestroyOwned):
    """
    Authenticated user can access intances owned by itself
    """

    pass


class OtherOwner(NoListOwned, NoRetrieveOwned, NoUpdateOwned, NoDestroyOwned):
    """
    Authenticated user cannot access any instances owned by other user
    """

    pass

