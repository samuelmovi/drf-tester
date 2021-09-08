import datetime

from rest_framework.test import APIRequestFactory, APITestCase

from drf_tester.viewsets.admin import AdminFullAccess
from drf_tester.viewsets.anon import AnonFullAccess, AnonNoAccess, AnonReadOnly
from drf_tester.viewsets.auth import AuthFullAccess, AuthOwner
from drf_tester.viewsets.staff import StaffReadOnly

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

THING_INSTANCE_DATA = {
    "name": "test thing name",
    "number": 5,
    "decimal_number": "1234.56",
    "timestamp": datetime.datetime.now().isoformat(),
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
        self.view = views.ThingViewSet.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy"})
        self.instance_data = THING_INSTANCE_DATA
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
        self.instance_data = THING_INSTANCE_DATA
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
        self.instance_data = THING_INSTANCE_DATA
        self.user_data = USER_DATA
        self.admin_data = ADMIN_DATA


class PropertyViewSetTest(APITestCase, AnonNoAccess, AuthOwner, AdminFullAccess, StaffReadOnly):
    """
    Auth Only.
    Update and delete require user==instance.creator
    """

    def setUp(self):
        """Tests setup"""
        self.requests = APIRequestFactory()
        self.endpoint = "/api/v1/property/"
        self.factory = factories.PropertyFactory
        self.model = models.Property
        self.view = views.PropertyViewSet.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )
        self.instance_data = {
            "name": "TEST property name",
        }
        self.user_data = USER_DATA
        self.admin_data = ADMIN_DATA
        self.USER_FIELD_NAME = 'creator'
