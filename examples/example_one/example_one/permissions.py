from rest_framework.permissions import BasePermission


class CreatorOnly(BasePermission):
    """
    Allow access if
    - user is admin
    - object creator is authenticated user
    - object creator is null
    """

    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user:
            return True
        elif obj.creator is None:
            return True
        elif request.user.is_admin:
            return True
        else:
            return False
