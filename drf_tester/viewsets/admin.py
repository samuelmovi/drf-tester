from rest_framework.test import APIRequestFactory

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
        self.user = utils.get_active_admin(**self.user_data)

    def test_admin_user_can_list(self):

        # Authenticate
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # create instances
        expected_instances = [self.factory() for i in range(random.randint(1,5))]
        # query endpoint
        request = self.requests.get(self.endpoint)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.get(self.endpoint)

        # assertions
        self.assertEquals(response.status_code, 200)
        payload = response.json()
        self.assertEquals(len(expected_instances), len(payload))

    def test_admin_user_can_get_details(self):
        # make user site amdin
        # self.user.role = 'SITE_ADMIN'
        # self.user.save()

        # Authenticate
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # create instances
        instance = self.factory()
        url = f"{self.endpoint}{instance.id}/"
        # query endpoint
        request = self.requests.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.get(url)

        # assertions
        self.assertEquals(response.status_code, 200)
        payload = response.json()
        self.assertEquals(instance.id, payload['id'])

    def test_admin_can_create_instance(self):
        # make user site amdin
        # self.user.role = 'SITE_ADMIN'
        # self.user.save()

        # Authenticate
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # query endpoint
        request = self.requests.post(self.endpoint, data=self.instance_data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.post(self.endpoint, data=data)

        # assertions
        self.assertEquals(response.status_code, 201)
        payload = response.json()
        # TODO: check response values
        self.assertEquals(data['name'], payload['name'])

    def test_admin_can_update_instance(self):
        # make user site amdin
        # self.user.role = 'SITE_ADMIN'
        # self.user.save()

        # Authenticate
        # token = get_tokens_for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")

        # create instance
        instance = self.factory()
        url = f"{self.endpoint}{instance.id}/"

        # query endpoint
        request = self.requests.put(url, data=self.alt_data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.put(url, data=data)

        # assertions
        self.assertEquals(response.status_code, 200)
        payload = response.json()
        # TODO: check response values
        self.assertEquals(data['name'], payload['name'])

    def test_admin_can_delete_instance(self):
        # create instance
        instance = self.factory()
        url = f"{self.endpoint}{instance.id}/"

        # query endpoint
        request = self.requests.delete(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # response = self.client.delete(url)

        # assertions
        self.assertEquals(response.status_code, 204)

