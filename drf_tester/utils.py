import random

from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory


User = get_user_model()


def get_active_user(instance_data):
    return User.objects.create(is_active=True, **instance_data)


def get_active_admin(instance_data):
    return User.objects.create(is_active=True, is_staff=True, is_superuser=True, **instance_data)


class BaseDrfTest:
    """
    All classes must extend from BaseDrfTest

    setup() must be overwritten
    get_alt_data() must be customized as well
    """

    def get_admin_user(self, data:dict) -> User:
        return get_active_admin(data)
    
    def get_active_user(self, data:dict) -> User:
        return get_active_user(data)
    
    def get_model_instances(self) -> list:
        """
        Use provided factory to create a random amount of instances
        Return list of those instances
        """
        return [self.factory() for i in range(random.randint(1,10))]        

    def setUp(self):
        """
        Create the required variables
        
        TO be overwritten in final Test class:

        self.requests = APIRequestFactory()
        self.endpoint = None
        self.factory = None
        self.model = None
        self.instance_data = {}
        self.alt_data = {}
        self.view = None
        self.user_data = {}
        self.admin_data = {}
        """
        pass

