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


## Viewset Tests

Code:

```
drf_tester/viewsets/
                utils.py
                /admin.py
                /auth_user.py
                /anon_user.py

```

They are separated in relation to the user querying the endpoing, and the action to be performed.

On each file we have classes covering every action, and some extended classes with convenient groupings of the more basic classes



## Installing


Globally:

```bash
pip install drf-tester
```

Locally:

```bash
pip install -e .
```

