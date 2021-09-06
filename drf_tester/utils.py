import random

from django.contrib.auth import get_user_model


User = get_user_model()


def get_active_user(instance_data):
    return User.objects.create(is_active=True, **instance_data)


def get_active_admin(instance_data):
    return User.objects.create(is_active=True, is_staff=True, is_superuser=True, **instance_data)


class BaseDrfTest:
    """
    All Test classes must extend BaseDrfTest

    - setUp() must be overridden
    """

    MIN = 5
    MAX= 10

    def check_equal_data(self, original: dict, received: dict):
        for key, value in original.items():
            self.assertEqual(value, received[key])
        return

    def get_admin_user(self, data: dict) -> User:
        return get_active_admin(data)

    def get_active_user(self, data: dict) -> User:
        return get_active_user(data)

    def get_model_instances(self, amount:int=None) -> list:
        """
        Use provided factory to create a random amount of instances, or exact amount if provided
        Return list of those instances
        """
        if amount:
            return [self.factory() for i in range(amount)]
        else:
            return [self.factory() for i in range(random.randint(self.MIN, self.MAX))]

    def setUp(self):
        """
        Create the required variables

        MUST override in implementation:

        self.requests = APIRequestFactory()
        self.endpoint = None
        self.factory = None
        self.model = None
        self.instance_data = {}
        self.view = None
        self.user_data = {}
        self.admin_data = {}
        """
        return NotImplementedError("You need to override BaseDrfTest.setUp()")
