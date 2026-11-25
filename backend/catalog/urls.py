from rest_framework.routers import DefaultRouter

from catalog.views import CargoTypeViewSet, CityViewSet

router = DefaultRouter()
router.register("cidades", CityViewSet, basename="city")
router.register("tipos-carga", CargoTypeViewSet, basename="cargo-type")
urlpatterns = router.urls
