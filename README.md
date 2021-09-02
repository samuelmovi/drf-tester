# DRF Tester

This module aims to minimize the time of test development, and increase while productivity, while guaranteeing an equal thoroughness of tests when developing REST APIs with `DjangoRestFramework`


## Table of Contents

- [Requirements](#requirements)
- [Viewset Tests](#viewset-tests)
- [Installing locally](#installing-locally)

## Requirements

- Python >= 3.7
- DjagnoRESTFramework >= 3.12.2


## Viewset Tests

Code:

```
drf_tester/viewsets/
                /admin.py
                /auth_user.py
                /anon_user.py

```

They are separated in relation to the user querying the endpoing, and the action to be performed.

On each file we have classes covering every action, and some extended classes with convenient groupings of the more basic classes



## Installing Locally

To install the package locally: 

```bash
pip install .
```

