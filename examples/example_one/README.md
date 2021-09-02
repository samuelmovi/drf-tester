# EXAMPLE ONE


## Table of contents

- [First Steps](#first-steps)
- [Settings](#settings)
- [core app](#core-app)

## First Steps

Steps taken in the creation of the project

- create venv: `virtualenv --python=python3.7 venv`
- activate venv: `source venv/bin/activate`
- populate and install requirements: `pip install -r requirements.txt`

## Settings

### .env variables

Add this below the `BASE_DIR` definition:

```python
import dotenv
# Get variables from .env
dotenv.read_dotenv(
    dotenv=os.path.join(BASE_DIR, '.env'),
    override=True
    )
```

### DRF config

```python
# DRF Options
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

### DRF MultiDB Tenants configutation

These is the default configuration, customizable in your settings

```python
# Multitenant config
DATABASE_ROUTERS = ["drf_multidb_tenants.dbrouters.TenantAwareRouter",]
TENANT_ONLY_APPS = ['things', 'tenantusers']
UNIVERSAL_APPS = ['contenttypes', ]     # migrated to all databases
TEST_TENANT_DB = 'test_tenant_db'
SHARED_USER_FIELD = 'email'
JWT_TENANT = False
```

#### Datbase configuration

Remember to add an extra database, like:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    },
    TEST_TENANT_DB: {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': TEST_TENANT_DB,
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    },
}
```

After this we add the following snippet to load all tenants' database upon start:
```python
from drf_multidb_tenants.dbmanager import DatabaseManager

with DatabaseManager(TEST_TENANT_DB) as dbmanager:
    """
    Load databases from tenant database
    """
    DATABASES[TEST_TENANT_DB] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': TEST_TENANT_DB,
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }


if not ('test' in sys.argv or 'makemigrations' in sys.argv or 'migrate' in sys.argv):
    with DatabaseManager() as dbmanager:
        """
        Load databases linked to by each Tenant instance
        """
        for dbname in dbmanager.load_databases():
            DATABASES[dbname[0]] = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': dbname[0],
                'USER': os.getenv('DB_USER'),
                'PASSWORD': os.getenv('DB_PASSWORD'),
                'HOST': os.getenv('DB_HOST'),
                'PORT': os.getenv('DB_PORT'),
            }
```



## core app


Create core app: `django-admin startapp core`

Register app in settings

### Create core models

2 models:

- `AuthUser`: extends `AbstractAuthUser`
    - Register in settings as `AUTH_USER_MODEL`
- `Tenant`: extends `AbstractTenant`

Migrate:

- `python manage.py makemigrations core`
- `python manage.py migrate`

OK!!

### Create Serializers

Create file `core/serializers.py`

Create serializer for Tenant.

Create read, write, and password change serializers for AuthUser


### Create Views


Extend the `UnifiedUserViewSet` and add required classes

(you can't add tenant user stuff yet because we haven't created it yet)


## tenantusers app

Stores the model for user that can be referenced within tenant's database, and link to authenticated user

Create app: `django-admin startapp tenantusers`

Register app in settings

### Create model

Only required field is `settings.SHARED_USER_FIELD`
The same as for `AuthUser`

### Create serializer

Added regular serializer and tenant-aware serializer

### Create view

Added view extending `TenantAwareViewSet`

## create routers.py



