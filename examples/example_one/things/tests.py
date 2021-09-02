from rest_framework.test import APIRequestFactory, APITestCase

from drf_tester.viewsets.admin import AdminFullAccess
from drf_tester.viewsets.anon_user import AnonNoAccess
from drf_tester.viewsets.auth_user import AuthFullAccess

from . import factories, models, views

# Create your tests here.


class ThingViewSetTest(APITestCase, AnonNoAccess):
    """Thing viewset tests"""

    def setUp(self):
        """Tests setup"""
        self.requests = APIRequestFactory()
        self.endpoint = "/api/v1/things/"
        self.factory = factories.ThingFactory
        self.model = models.Thing
        self.view = views.ThingViewSet
        self.endpoint = "/api/v1/things/"
        self.model = models.Thing
        # instance data
        self.instance_data = {
            "name": "test thing name",
        }
        self.user_data = {
            "username": "test_user",
            "password": "jioqwehjnr890qweufno8we",
        }
        self.admin_data = {
            "username": "admin_user",
            "password": "jioqwehjnr890qweufno8we",
        }
