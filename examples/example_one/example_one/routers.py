from rest_framework import routers

from core import views as core_views
from things import views as thing_views

# from things import views as things_views

router = routers.DefaultRouter()


router.register('things', thing_views.ThingViewSet, basename='things')
