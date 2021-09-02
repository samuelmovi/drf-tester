import random
import string

from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status

from drf_multidb_tenants.testing import TenantAwareTest
from drf_multidb_tenants.settings import mdb_settings

from core.models import Tenant, AuthUser
from example_one import utils

from tenantusers.models import TenantUser

from . import models

# Create your tests here.

class ThingViewSetTest(TenantAwareTest):
    """Thing viewset tests
    """

    test_tenant_name = 'Mr. Test'
    test_tenant_database = mdb_settings.TEST_TENANT_DB
    tenant_model = Tenant
    auth_user_model = AuthUser
    tenant_user_model = TenantUser
    email = 'test@email.com'
    databases = ['default', mdb_settings.TEST_TENANT_DB]

    def setUp(self):
        """Tests setup
        """
        self.endpoint = '/api/v1/things/'
        self.model = models.Thing
        # instance data
        self.instance_data = {
            'name': 'test thing name',
        }

    def tearDown(self):
        self.auth_user_model.objects.all().delete()
        self.tenant_user_model.objects.using(self.test_tenant_database).all().delete()

    def get_instance(self, data):
        return self.model.objects.using(self.test_tenant_database).create(**data)

    # anon users
    def test_anon_user_cannot_create_instance(self):
        """Anonymous user cannot create new instance
        """
        instances = [self.get_instance(self.instance_data) for n in range(random.randint(1,5))]

        # Query endpoint
        response = self.client.post(self.endpoint, data={})
        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anon_user_cannot_modify_existing_instance(self):
        """Anonymous user cannot modify existing instance
        """
        # Create instance
        instance = self.get_instance(self.instance_data)

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        response = self.client.put(url, {}, format='json')

        # Assert forbidden code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anon_user_cannot_delete_existing_instance(self):
        """Anonymous user cannot delete existing instance
        """
        # Create instances
        instance = self.get_instance(self.instance_data)

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anon_user_cannot_list_instances(self):
        """Anonymous user can't read instance
        """
        # Request list
        response = self.client.get(self.endpoint)

        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # auth users
    def test_auth_user_can_list_instances(self):
        """Authenticated user can list instances
        """
        # Create instances
        instances = [self.get_instance(self.instance_data) for n in range(random.randint(1,5))]

        # Authenticate
        token = utils.get_tokens_for_user(self.auth_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # Request list
        response = self.client.get(self.endpoint)

        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert all instances are returned
        self.assertEqual(len(instances), len(response.data))

    def test_auth_user_can_create_instance(self):
        """Authenticated user can create new instance
        """
        # Authenticate
        token = utils.get_tokens_for_user(self.auth_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # Query endpoint
        response = self.client.post(self.endpoint, data=self.instance_data, format='json')

        # Assert endpoint returns created status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auth_user_can_modify_existing_instance(self):
        """Authenticated user can modify existing instance
        """
        # Create instances
        instance = self.get_instance(self.instance_data)

        alt_data = {
            'name': 'ALT name for thing',
        }

        # Authenticate
        token = utils.get_tokens_for_user(self.auth_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        response = self.client.put(url, data=alt_data, format='json')

        # Assert endpoint returns OK code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert instance has been modified
        for key in alt_data:
            self.assertEqual(alt_data[key], response.data[key])

    def test_auth_user_can_delete_existing_instance(self):
        """Authenticated user can delete existing instance
        """
        # Create instances
        instance = self.get_instance(self.instance_data)

        # Authenticate
        token = utils.get_tokens_for_user(self.auth_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        response = self.client.delete(url)

        # assert 204 no content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Assert instance doesn't exists anymore on db
        self.assertFalse(self.model.objects.filter(id=instance.pk).exists())
