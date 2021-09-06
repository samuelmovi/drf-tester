
import datetime
from decimal import Decimal

from rest_framework.test import APIRequestFactory, APITestCase

from drf_tester.viewsets.admin import AdminFullAccess
from drf_tester.viewsets.anon_user import AnonNoAccess, AnonReadOnly, AnonFullAccess
from drf_tester.viewsets.auth_user import AuthFullAccess

from . import factories, models, views

# Create your tests here.


USER_DATA = {
    "username": "test_user",
    "password": "jioqwehjnr890qweufno8we",
}

ADMIN_DATA = {
    "username": "admin_user",
    "password": "jioqwehjnr890qweufnrereo8we",
}

INSTANCE_DATA = {
    "name": "test thing name",
    "number": 5,
    "decimal_number": '1234.56',
    "timestamp": datetime.datetime.now().isoformat()
}


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
        self.endpoint = "/api/v1/things/"
        self.model = models.Thing
        # instance data
        self.instance_data = INSTANCE_DATA
        self.user_data = USER_DATA
        self.admin_data = ADMIN_DATA


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
        self.endpoint = "/api/v1/things/"
        self.model = models.Thing
        # instance data
        self.instance_data = INSTANCE_DATA
        self.user_data = USER_DATA
        self.admin_data = ADMIN_DATA


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
        self.endpoint = "/api/v1/things/"
        self.model = models.Thing
        # instance data
        self.instance_data = INSTANCE_DATA
        self.user_data = USER_DATA
        self.admin_data = ADMIN_DATA

