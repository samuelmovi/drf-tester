from django.shortcuts import get_object_or_404

from example_one.permissions import CreatorPermission
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Property, Thing
from .serializers import PropertySerializer, ThingSerializer

# Create your views here.


class ThingViewSet(viewsets.ModelViewSet):
    """Thing Viewset for Authenticated Users only."""

    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class ThingViewSet2(viewsets.ModelViewSet):
    """Thing Viewset for Authenticated Users, read only for anonymous users."""

    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


class ThingViewSet3(viewsets.ModelViewSet):
    """Thing Viewset completely unrestricted."""

    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [
        AllowAny,
    ]


# PROPERTY VIEWSETS


class PropertyViewSet(viewsets.ModelViewSet):

    model = Property
    serializer_class = PropertySerializer
    permission_classes = [
        CreatorPermission,
    ]

    def get_queryset(self):
        if self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.is_staff):
            qs = self.model.objects.all()
        else:
            qs = self.model.objects.filter(creator=self.request.user)
        return qs

    def get_object(self):
        obj = get_object_or_404(self.model.objects.all(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
