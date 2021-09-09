"""
Collection of functions to be used by other tests in module

"""
import random

from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(instance_data: dict) -> User:
    """
    Create and return an instance of the user model
    """
    return User.objects.create(**instance_data)


def get_active_user(instance_data: dict) -> User:
    """
    Return an active instance of user
    """
    instance_data["is_active"] = True
    return create_user(instance_data)


def get_active_admin(instance_data: dict) -> User:
    """
    Return an active instance of admin user
    """
    instance_data["is_active"] = True
    instance_data["is_superuser"] = True

    return create_user(instance_data)


def get_active_staff(instance_data: dict) -> User:
    """
    Return an active instance of admin user
    """
    instance_data["is_active"] = True
    instance_data["is_staff"] = True

    return create_user(instance_data)


class BaseDrfTest:
    """
    All Test classes must extend BaseDrfTest

    - setUp() must be overridden
    """

    # Customize for desired range of random instances
    MIN = 5
    MAX = 10
    # set to integer value if random instance amounts are not desired
    EXACT_AMOUNT = None

    def check_equal_data(self, original: dict, received: dict):
        for key, value in original.items():
            self.assertEqual(value, received[key])
        return

    def get_admin_user(self, data: dict) -> User:
        return get_active_admin(data)

    def get_active_user(self, data: dict) -> User:
        return get_active_user(data)

    def get_active_staff(self, data: dict) -> User:
        return get_active_staff(data)

    def get_model_instances(self) -> list:
        """
        Return list of model instances:
        - Exact size if self.EXACT_AMOUNT is not null
        - Random size between MIN and MAX (customizable)
        """
        if self.EXACT_AMOUNT:
            return [self.factory() for i in range(self.EXACT_AMOUNT)]
        else:
            return [self.factory() for i in range(random.randint(self.MIN, self.MAX))]

    def setUp(self):
        """
        Create the required variables

        Override in implementation for correct operation:

        self.requests = APIRequestFactory()
        self.endpoint = None
        self.factory = None
        self.model = None
        self.instance_data = {}
        self.view = viewsets.YourViewSet
        self.user_data = {}     # Required for authenticated user testing
        self.admin_data = {}    # Required for super user testing
        self.staff_data = {}    # Required for staff user testing
        self.USER_FIELD_NAME = 'creator'    # Required for testing user object access
        """
        return NotImplementedError("You need to override BaseDrfTest.setUp()")
