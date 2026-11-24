from rest_framework.routers import DefaultRouter

from catalog.views import CargoTypeViewSet

router = DefaultRouter()
router.register("tipos-carga", CargoTypeViewSet, basename="cargo-type")
urlpatterns = router.urls
