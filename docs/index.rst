Welcome to drf-tester's documentation!
======================================

``drf-tester`` is a Python module that aims to help developers with testing `DjangoRestFramework` API endpoints.

- Minimize the time (and lines of code) required
- Mantain consistent testing coverage
- Increase productivity!

The philosophy behind the design of this module, is that a developer should only need to:

1. Prepare the ``setUp`` method of a Test class
2. Choose the correct classes to inheritb for each type of access
3. Smile!!

This saves us developers lots of time writing repetitive, boiler-plate code, while reassuring that our tests are, at the very least, consistent.


Requirements
------------

The module has been tested to work with the following software versions.

- Python 3.7
- Django 2.2
- DjagnoRESTFramework 3.12.2
- factory-boy 3.1.0

Compatibility likely greater than indicated here (let me know if something else works for you)


Installation
------------

To install `drf-tester` in your systems, use pip:

.. code-block::bash

    pip install drf-tester


.. toctree::
   :maxdepth: 2

   base-drf-test
   viewset-tests
   example

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
