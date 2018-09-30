from rest_framework import routers

from .views import CatViewSet

router = routers.SimpleRouter()
router.register(r'cat', CatViewSet)
urlpatterns = router.urls
