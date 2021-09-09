BaseDrfTest
===========

Located in ``drf_tester.utils`` this class is the glue that makes it all work.

It contains the ``setUp`` method to be run before every test, as well as some helper functions and Object variables.

Check out the code for more details.

Built-in Functions
------------------

Some generic methods are created for DRYer single-action test classes.

- ``get_admin_user(self, data: dict) -> User``
- ``get_active_user(self, data: dict) -> User``
- ``get_active_staff(self, data: dict) -> User``
- ``get_model_instances(self) -> list``

Object Variables
----------------

Some Object-level variables are declared outside of ``setUp`` for convenience.

- ``EXACT_AMOUNT``: if is set to an integer value, ``get_model_instances`` will return a list of instances of exactly that size.
- ``MIN`` and ``MAX``: used as limits when using ``random.randint`` to create a list of instances of random size. Default: ``5`` and ``10``.

setUp()
-------

The variables required for correct operation:

.. code-block:: python

    self.requests = APIRequestFactory()
    self.endpoint = None    # string with the url of the endpoint
    self.factory = None     # factory-boy class to create model instances
    self.model = None       # the model accessed through the endpoint
    self.instance_data = {}     # dict of valid SERIALIZED data for instance creation
    self.view = viewsets.YourViewSet.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy"})
    self.user_data = {}     # Required for authenticated user testing
    self.admin_data = {}    # Required for super user testing
    self.staff_data = {}    # Required for staff user testing
    self.USER_FIELD_NAME = 'creator'    # Required for testing user object access


Access Level
------------

Once you know what level of access each kind of user should have, just add those classes to your tests, after ``APITestCase``.

Example:

.. code-block:: python

    from drf_tester.viewsets import anon, admin, auth

    class YourViewSetTest(APITestCase, anon.AnonNoAccess, auth.AuthFullAccess, admin.AdminFullAccess):
        """To test a ModelViewSet with IsAuthenticated as the only Permission
        """

        def setUp(self):
            ...

