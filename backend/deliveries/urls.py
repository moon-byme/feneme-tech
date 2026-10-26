from rest_framework.routers import DefaultRouter
from deliveries.views import DeliveryViewSet

router = DefaultRouter()
router.register("deliveries", DeliveryViewSet, basename="delivery")
urlpatterns = router.urls
