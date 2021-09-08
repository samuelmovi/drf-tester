from rest_framework import routers
from things import views as thing_views

# from things import views as things_views

router = routers.DefaultRouter()


router.register("things/is_authenticated/", thing_views.ThingViewSet, basename="things-auth-only")
router.register("things/auth_or_readonly/", thing_views.ThingViewSet3, basename="things-auth-or-readonly")
router.register("things/allow_any/", thing_views.ThingViewSet3, basename="things-allow-any")

router.register("property/", thing_views.PropertyViewSet, basename="property")
