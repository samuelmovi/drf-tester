Example
=======

Included in the repository, there's an example illustrating how to implement in your project.

From ``example_one``:

.. code-block:: python

    class ThingViewSetTest(APITestCase, AnonNoAccess, AuthFullAccess, AdminFullAccess):
        """
        Thing viewset tests
        Permission level: IsAuthenticated
        """

        def setUp(self):
            """Tests setup"""
            self.endpoint = "/api/v1/things/"
            self.factory = factories.ThingFactory
            self.model = models.Thing
            self.view = views.ThingViewSet.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy"})
            self.instance_data = {...}
            self.user_data = {...}
            self.admin_data = {...}

For more details, checkout the project under ``example/example_one/``

