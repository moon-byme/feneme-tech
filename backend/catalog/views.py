from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsGestorOrMotorista
from catalog.models import CargoType, City
from catalog.serializers import CargoTypeSerializer, CitySerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista única de cidades (US-14 / FT-113). Somente leitura."""

    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated, IsGestorOrMotorista]
    pagination_class = None


class CargoTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Catálogo de tipos de carga (US-15 / FT-114). Somente leitura para todos os perfis."""

    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    permission_classes = [IsAuthenticated, IsGestorOrMotorista]
    pagination_class = None
