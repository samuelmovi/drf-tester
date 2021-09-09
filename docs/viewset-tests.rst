Viewset Tests
=============

All the classes to assist with the development of tests for ``ViewSets`` are located under ``drf_tester.viewsets``, and separated by user type:

- ``anon.py``: Anonymous users
- ``auth.py``: Authenticated users
- ``admin.py``: Admin user (superusers)
- ``staff.py``: Staff users

Within each file, there are classes that test the effects of different actions on the endpoint. For example:

.. code-block:: python

    # drf_tester/viewsets/anon.py

    class NoCreate(BaseDrfTest):
        def test_anon_user_cannot_create_instance(self):
            """Anonymous user cannot create new instance"""
            ...



These single-action classes are grouped in bigger classes meant to be inherited by the final test cases. For example:

.. code-block:: python

    class AnonReadOnly(CanList, CanRetrieve, NoCreate, NoUpdate, NoDestroy):
        """
        Anonymous user has only read access to endopint
        """

        pass


A few different combinations are provided for your convenience:

- For anonymous users:
    - ``AnonNoAccess``
    - ``AnonReadOnly``
    - ``AnonFullAccess``
- For authenticated users:
    - ``AuthFullAccess``
    - ``AuthNoAccess``
    - ``AuthReadOnly``
    - ``AuthOwner``: only controls instances linked to user
- For admin users:
    - ``AdminNoAccess``
    - ``AdminReadOnly``
    - ``AdminFullAccess``
- For staff users:
    - ``StaffNoAccess``
    - ``StaffReadOnly``
    - ``StaffFullAccess``


Custom groups can be made mixing and matching classes according with the level of access expected by each user-type from each endpoint.


