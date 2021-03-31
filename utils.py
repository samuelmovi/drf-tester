from django.contrib.auth import get_user_model

User = get_user_model()


def get_active_user(instance_data):
    return User.objects.createuser(is_active=True, **instance_data)


def get_active_admin(instance_data):
    return User.objects.createsuperuser(is_active=True, is_staff=True, **instance_data)
