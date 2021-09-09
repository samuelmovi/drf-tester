# DRF Tester

This module aims to help developers with testing `DjangoRestFramework` API endpoints:

- Minimize the time (and lines of code) required
- Mantain consistent testing
- Increase productivity!

The philosophy behind the design of this module, is that a developer should only need to:

1. Prepare the `setUp` method of a Test class
2. Choose the correct classes to inheritb for each type of access
3. Smile!!

This saves us developers lots of time writing repetitive, boiler-plate code, while reassuring that our tests are, at the very least, consistent.

For more details, [read the docs](https://drf-tester.readthedocs.io/en/latest/)

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [BaseDrfTest](#basedrftest)
- [Viewset Tests](#viewset-tests)
- [Example](#example)
- [Contributions](#contributions)

## Requirements

- Python 3.7
- Django 2.2
- DjagnoRESTFramework 3.12.2
- factory-boy 3.1.0

## Installation

To install `drf-tester` in your systems, use pip:

```bash

pip install drf-tester

```


## BaseDrfTest

Located in `drf_tester.utils` this class is the glue that makes it all work.

It contains the `setUp` method to be run before every test, as well as some helper functions and Object variables.

Check out the code for more details.

### Built-in Functions

Some generic methods are created for DRYer single-action test classes.

- `get_admin_user(self, data: dict) -> User`
- `get_active_user(self, data: dict) -> User`
- `get_active_staff(self, data: dict) -> User`
- `get_model_instances(self) -> list`

### Object Variables

Some Object-level variables are declared outside of `setUp` for convenience.

- `EXACT_AMOUNT`: if is set to an integer value, `get_model_instances` will return a list of instances of exactly that size.
- `MIN` and `MAX`: used as limits when using `random.randint` to create a list of instances of random size. Default: `5` and `10`.

### setUp()

The variables required for correct operation:

```python
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
```

### Access Level

Once you know what level of access each kind of user should have, just add those classes to your tests, after `APITestCase`.

Example:

```python

from drf_tester.viewsets import anon, admin, auth

class YourViewSetTest(APITestCase, anon.AnonNoAccess, auth.AuthFullAccess, admin.AdminFullAccess):
    """To test a ModelViewSet with IsAuthenticated as the only Permission
    """

    def setUp(self):
        ...

```

## Viewset Tests

All the classes to assist with the development of tests for `ViewSets` are located under `drf_tester.viewsets`, and separated by user type:

- `anon.py`: Anonymous users
- `auth.py`: Authenticated users
- `admin.py`: Admin user (superusers)
- `staff.py`: Staff users

Within each file, there are classes that test the effects of different actions on the endpoint. For example:

```python
# drf_tester/viewsets/anon.py

class NoCreate(BaseDrfTest):
    def test_anon_user_cannot_create_instance(self):
        """Anonymous user cannot create new instance"""
        ...

```

These single-action classes are grouped in bigger classes meant to be inherited by the final test cases. For example:

```python

class AnonReadOnly(CanList, CanRetrieve, NoCreate, NoUpdate, NoDestroy):
    """
    Anonymous user has only read access to endopint
    """

    pass

```

A few different combinations are provided for your convenience:

- For anonymous users:
    - `AnonNoAccess`
    - `AnonReadOnly`
    - `AnonFullAccess`
- For authenticated users:
    - `AuthFullAccess`
    - `AuthNoAccess`
    - `AuthReadOnly`
    - `AuthOwner`: only controls instances linked to user
- For admin users:
    - `AdminNoAccess`
    - `AdminReadOnly`
    - `AdminFullAccess`
- For staff users:
    - `StaffNoAccess`
    - `StaffReadOnly`
    - `StaffFullAccess`


Custom groups can be made mixing and matching classes according with the level of access expected by each user-type from each endpoint.



## Example

Included in the repository, there's an example illustrating how to implement in your project.

From `example_one`:

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


## Contributions

I would love for the project to cover as many use-cases as possible, and for that I need your help.

There will always be some customized endpoint functionality that will never be covered by this module, but I'd like to make it as extensive as reasonably possible.

If you know of any situations for which the current solution won't work, please let me know and I'll try to make allowances for it.

Check out [CONTRIBUTING.md](contributing.md) for more details.
