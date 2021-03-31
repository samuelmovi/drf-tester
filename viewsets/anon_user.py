import random
import string

from rest_framework import status


class NoAccess:

    def setUp(self):
        self.endpoint = None
        self.factory = None
        self.model = None

    # anon user
    def test_anon_user_cannot_create_instance(self):
        """Anonymous user cannot create new instance
        """
        instances = [self.factory() for n in range(random.randint(1,5))]

        # Query endpoint
        response = self.client.post(self.endpoint, data={})
        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anon_user_cannot_modify_existing_instance(self):
        """Anonymous user cannot modify existing instance
        """
        # Create instance
        instance = self.factory()

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        response = self.client.put(url, {}, format='json')

        # Assert forbidden code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anon_user_cannot_delete_existing_instance(self):
        """Anonymous user cannot delete existing instance
        """
        # Create instances
        instance = self.factory()

        # Query endpoint
        url = self.endpoint + f'{instance.pk}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Assert instance still exists on db
        self.assertTrue(self.model.objects.get(id=instance.pk))


class ReadAccess:

    def setUp(self):
        self.endpoint = None
        self.factory = None
        self.model = None
        self.filters = []

    def test_anon_user_can_list_instances(self):
        """Anonymous user can list instances
        """
        # create instances
        expected_instances = [ self.factory() for x in random.randint(3, 10) ]
        # Request list
        response = self.client.get(self.endpoint)

        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()

        # Assert number of instances in response
        self.assertEquals(len(expected_instances), len(payload))

    def test_anon_user_can_filter(self):
        """Iterate over self.filters
        Assert expected functionality
        """
        for filter_name in self.filters:
            random_string = ''.join(random.choices(string.ascii_uppercase, k = 10))
            # create instances
            expected = self.factory()
            setattr(expected, filter_name, random_string)
            unexpected = self.factory()

            url = f"{self.endpoint}?{filter_name}={random_string}"

            # Request list
            response = self.client.get(url)

            # Assert access is granted
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            payload = response.json()
            # Assert number of instances in response
            self.assertEquals(1, len(payload))
            # Assert value in response
            self.assertEquals(payload[0][filter_name], random_string)

