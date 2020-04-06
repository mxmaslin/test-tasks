from rest_framework import routers

from .views import CarViewSet, ComponentViewSet, TripViewSet

router = routers.SimpleRouter()
router.register(r'car', CarViewSet)
router.register(r'component', ComponentViewSet)
router.register(r'trip', TripViewSet)
urlpatterns = router.urls
