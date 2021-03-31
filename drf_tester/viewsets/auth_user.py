from rest_framework.test import APIRequestFactory, force_authenticate

from .. import utils


class FullAccess:
    """
    User has wide access to all endopints and the instances,
    irregardless of who created them
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

    # authenticated user
    def test_auth_user_can_paginate_instances(self):
        """authenticated user can paginate instances
        """
        # Authenticate
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        limit = 5
        offset = 10
        # create instances
        instances = [self.factory(creator=self.user) for n in range(12)]

        # Request list
        url = f"{self.endpoint}?limit={limit}&offset={offset}"
        request = self.requests.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.get(url)

        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert only 2 instances in response
        payload = response.json()
        self.assertEquals(2, len(payload['results']))

    def test_auth_user_can_list_instances(self):
        """Regular logged-in user can list instance
        """
        # Create instances
        instances = [self.factory() for n in range(random.randint(1,5))]

        # Authenticate user
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # Request list
        request = self.requests.get(self.endpoint)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.get(self.endpoint)

        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert all instances are returned
        self.assertEqual(len(instances), len(response.data))

    def test_auth_user_can_get_instance(self):
        """Regular logged-in user can list instance
        """
        # Create instances
        instance = self.factory()

        # Authenticate user
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # Request list
        url = f"{self.endpoint}{instance.id}/"
        request = self.requests.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.get(url)

        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEquals(instance.id, data['id'])

    def test_auth_user_can_create_instance(self):
        """Regular logged-in user can create new instance
        """

        # Authenticate user
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # Query endpoint
        request = self.requests.post(self.endpoint, data=self.instance_data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.post(self.endpoint, data=self.instance_data, format='json')
        # Assert endpoint returns created status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert instance exists on db
        self.assertTrue(self.model.objects.get(id=response.data['id']))

    def test_auth_user_can_modify_own_instance(self):
        """Regular logged-in user can modify existing instance
        """
        # Create instances
        instance = self.factory()
        # make our user the creator
        instance.creator = self.user
        instance.save()

        # Authenticate user
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        request = self.requests.put(url, self.alt_data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.put(url, data, format='json')
        # Assert endpoint returns OK code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert instance has been modified
        for key in data:
            if key == 'company':
                continue
            self.assertEqual(data[key], response.data[key])

    def test_auth_user_can_delete_own_instance(self):
        """Regular logged-in user can delete existing instance
        """
        # Create instances
        instance = self.factory()
        # make our user the creator
        instance.creator = self.user
        instance.save()

        # Authenticate user
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        request = self.requests.delete(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.delete(url)

        # assert 204 no content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Assert instance doesn't exists anymore on db
        self.assertFalse(self.model.objects.filter(id=instance.pk).exists())


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

        # Authenticate user
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        request = self.requests.put(url, data=self.alt_data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.put(url, data=data, format='json')

        # Assert endpoint returns 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_cannot_delete_other_users_instance(self):
        """Authenticated user cannot delete other user's instance
        """
        # Create instances
        instance = self.factory()

        # Authenticate user
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        request = self.requests.delete(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.delete(url, format='json')

        # Assert endpoint returns 403 code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


