from example_one.permissions import CreatorPermission
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Property, Thing
from .serializers import PropertySerializer, ThingSerializer

# Create your views here.


class ThingViewSet(viewsets.ModelViewSet):

    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class ThingViewSet2(viewsets.ModelViewSet):

    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


class ThingViewSet3(viewsets.ModelViewSet):

    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [
        AllowAny,
    ]


# PROPERTY VIEWSETS


class PropertyViewSet(viewsets.ModelViewSet):

    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [
        IsAuthenticated,
        CreatorPermission,
    ]
