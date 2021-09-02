# DRF Tester

This module aims to minimize the time of test development, and increase while productivity, while guaranteeing an equal thoroughness of tests when developing REST APIs with `DjangoRestFramework`


## Table of Contents

- [Viwset Tests](#viewset-tests)



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


