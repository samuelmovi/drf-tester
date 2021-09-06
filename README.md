# DRF Tester

This module aims to help developers with testing `DjangoRestFramework` API endpoints:

- Minimize the time (and lines of code) required
- Mantain consistent testing coverage
- Increase productivity!

## Table of Contents

- [Requirements](#requirements)
- [How to Use](#how-to-use)
- [Viewset Tests](#viewset-tests)
- [Installing locally](#installing-locally)

## Requirements

- Python >= 3.7
- DjagnoRESTFramework >= 3.12.2


## How To Use


To create a `TestCase` class to test a DRF endpoint:

- Extend `APITestCase`
- Import and the add `drf_tester` classes that your class requires
- Fillup the `setUp()` method with all the required variables


### Example

Included in the repository, there's an example illustrating how to implement in your project.

To test a fully open endpoint:

```python
class ThingViewSetTest(APITestCase, AnonNoAccess, AuthFullAccess, AdminFullAccess):
    """
    Thing viewset tests
    Permission level: IsAuthenticated
    """

    def setUp(self):
        """Tests setup"""
        self.requests = APIRequestFactory()
        self.endpoint = "/api/v1/things/"
        self.factory = factories.ThingFactory
        self.model = models.Thing
        self.view = views.ThingViewSet.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy"})
        self.instance_data = {...}
        self.user_data = {...}
        self.admin_data = {...}
```

## Viewset Tests

The code is separated depending on the user making the request:

```
drf_tester/viewsets/
                utils.py
                /admin.py
                /auth_user.py
                /anon_user.py

```

Within each file, there are classes that test the effects of every single action on the endpoint

These single-action classes are grouped in major classes meant to be inherited by the final test case.

For `AnonymousUser`:

- `AnonNoAccess`
- `AnonReadOnly`
- `AnonFullAccess`

For authenticate users:

- `AuthFullAccess`
- `AuthNoAccess`
- `AuthReadOnly`
- `AuthOwner`

For admin users:

- `AdminNoAccess`
- `AdminReadOnly`
- `AdminFullAccess`

You need to mix and match classes according with the level of access expected from each endpoint.

## Installing

Globally:

```bash
pip install drf-tester
```

Locally:

```bash
pip install -e .
```

