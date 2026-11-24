from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsGestorOrMotorista
from catalog.models import CargoType
from catalog.serializers import CargoTypeSerializer


class CargoTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Catálogo de tipos de carga (US-15 / FT-114). Somente leitura para todos os perfis."""

    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    permission_classes = [IsAuthenticated, IsGestorOrMotorista]
    pagination_class = None
