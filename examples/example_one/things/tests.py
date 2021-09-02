import random

from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status

from drf_tester.viewsets.anon_user import AnonNoAccess
from drf_tester.viewsets.auth_user import AuthFullAccess
from drf_tester.viewsets.admin import AdminFullAccess

from . import models
from . import factories
from . import views

# Create your tests here.

class ThingViewSetTest(AnonNoAccess, AuthFullAccess, AdminFullAccess):
    """Thing viewset tests
    """

    def setUp(self):
        """Tests setup
        """
        self.endpoint = '/api/v1/things/'
        self.factory = factories.ThingFactory
        self.model = models.Thing
        self.view = views.ThingViewSet
        self.endpoint = '/api/v1/things/'
        self.model = models.Thing
        # instance data
        self.instance_data = {
            'name': 'test thing name',
        }
        self.user_data = {
            "username": "test_user",
            "password": "jioqwehjnr890qweufno8we",
        }
        self.admin_data = {
            "username": "admin_user",
            "password": "jioqwehjnr890qweufno8we",
        }

