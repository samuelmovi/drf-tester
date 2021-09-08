# DRF Tester

This module aims to help developers with testing `DjangoRestFramework` API endpoints:

- Minimize the time (and lines of code) required
- Mantain consistent testing coverage
- Increase productivity!

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [Viewset Tests](#viewset-tests)
- [Installing locally](#installing-locally)
- [Contributions](#contributions)

## Requirements

- Python >= 3.7
- DjagnoRESTFramework >= 3.12.2


## Installation

To install `drf-tester` in your systems, use pip:

```bash
pip install drf-tester
```

## How To Use

The philosophy behind the design of this module, is that a developer should only need to:

- prepare the `setUp` method of a Test class
- choose the correct classes to inherit

This saves the developer lots of time writing repetitive, boiler-plate code to thoroughly cover every possible action upon an endpoint, by different kinds of users.

From a user point-of-view, the test classes are divided in 4 groups:

- `anon.py`: Anonymous users
- `auth.py`: Authenticated users
- `admin.py`: Admin user (superusers)
- `staff.py`: Staff users

Each module contains all of the classes required to test access for that user-type.
These are like small building blocks with which to construct more comprehensive classes.
By default some of these larger classes are provided for convenience.

Example:

```python

class AnonReadOnly(CanList, CanRetrieve, NoCreate, NoUpdate, NoDestroy):
    """
    Anonymous user has only read access to endopint
    """

    pass

```

When you know what level of access each kind of user should have, just add those classes to your tests, after `APITestCase`.

Example:

```python

class YourViewSetTest(APITestCase, AnonNoAccess, AuthFullAccess, AdminFullAccess):

    def setUp(self):
        ...

```

### Example

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

## Viewset Tests

Within each file, there are classes that test the effects of every single action on the endpoint

These single-action classes are grouped in bigger classes meant to be inherited by the final test case.

Provided action-bundles test classes are:

- For `AnonymousUser`:
    - `AnonNoAccess`
    - `AnonReadOnly`
    - `AnonFullAccess`
- For authenticated users:
    - `AuthFullAccess`
    - `AuthNoAccess`
    - `AuthReadOnly`
    - `AuthOwner`
- For admin users:
    - `AdminNoAccess`
    - `AdminReadOnly`
    - `AdminFullAccess`
- For staff users:
    - `StaffNoAccess`
    - `StaffReadOnly`
    - `StaffFullAccess`

Mix and match classes according with the level of access expected by each user-type from each endpoint.


## Contributions

Contributions are welcome
