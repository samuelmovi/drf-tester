from rest_framework.permissions import SAFE_METHODS, BasePermission


class CreatorPermission(BasePermission):
    """
    Access Control:
    - Full Access: admin, creator
    - Read access: staff
    """

    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user:
            # grant access to instance cretaor
            return True
        elif request.user.is_superuser:
            # full access to admin
            return True
        elif request.user.is_staff and request.method in SAFE_METHODS:
            # safe access to staff
            return True
        else:
            return False

    def has_permission(self, request, view):

        if request.user.is_staff and request.method in SAFE_METHODS:
            # safe access to staff
            return True
        elif request.user.is_authenticated and not request.user.is_staff:
            # staff cannot create instances
            return True
        else:
            return False
