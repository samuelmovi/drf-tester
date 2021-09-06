from rest_framework.test import APIRequestFactory, APITestCase

from drf_tester.viewsets.admin import AdminFullAccess
from drf_tester.viewsets.anon_user import AnonNoAccess, AnonReadOnly, AnonFullAccess
from drf_tester.viewsets.auth_user import AuthFullAccess

from . import factories, models, views

# Create your tests here.


class ThingViewSetTest(APITestCase, AnonNoAccess, AuthFullAccess, AdminFullAccess):
    """
    Thing viewset tests
    Permission level: IsAuthenticated
    """

    def setUp(self):
        """Tests setup"""
        self.requests = APIRequestFactory()
        self.endpoint = "/api/v1/things/is_authenticated/"
        self.factory = factories.ThingFactory
        self.model = models.Thing
        self.view = views.ThingViewSet.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )
        # self.detail_view = views.MoistureCheckViewSet.as_view({"get": "retrieve"})
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


class ThingViewSet2Test(APITestCase, AnonReadOnly, AuthFullAccess, AdminFullAccess):
    """
    Thing viewset tests
    Permission level: IsAuthenticatedOrReadOnly
    """

    def setUp(self):
        """Tests setup"""
        self.requests = APIRequestFactory()
        self.endpoint = "/api/v1/things/auth_or_readonly/"
        self.factory = factories.ThingFactory
        self.model = models.Thing
        self.view = views.ThingViewSet2.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )
        # self.detail_view = views.MoistureCheckViewSet.as_view({"get": "retrieve"})
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


class ThingViewSet3Test(APITestCase, AnonFullAccess, AuthFullAccess, AdminFullAccess):
    """
    Thing viewset tests
    Permission level: AllowAny
    """

    def setUp(self):
        """Tests setup"""
        self.requests = APIRequestFactory()
        self.endpoint = "/api/v1/things/allow_any/"
        self.factory = factories.ThingFactory
        self.model = models.Thing
        self.view = views.ThingViewSet3.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )
        # self.detail_view = views.MoistureCheckViewSet.as_view({"get": "retrieve"})
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

