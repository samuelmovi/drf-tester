from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Thing
from .serializers import ThingSerializer
# Create your views here.



class ThingViewSet(viewsets.ModelViewSet):

    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [IsAuthenticated,]

