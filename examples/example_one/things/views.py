from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

from example_one.permissions import AlwaysTrue
from .models import Thing
from .serializers import ThingSerializer

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
        AlwaysTrue,
    ]
