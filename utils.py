from django.contrib.auth import get_user_model

User = get_user_model()


def get_active_user(instance_data):
    return User.objects.create_user(is_active=True, **instance_data)

