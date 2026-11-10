from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import UserProfile
from accounts.permissions import IsGestor, IsGestorOrMotorista
from deliveries.models import Delivery, RouteAlternative
from deliveries.serializers import (
    AssignDriverSerializer,
    DeliverySerializer,
    RouteAlternativeSerializer,
)

ROUTE_LIMIT_MESSAGE = (
    f"O limite é de {RouteAlternative.MAX_PER_DELIVERY} alternativas de trajeto por entrega."
)

class DeliveryViewSet(viewsets.ModelViewSet):
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, IsGestor]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        queryset = Delivery.objects.select_related(
            "assigned_driver", "created_by"
        ).prefetch_related("route_alternatives")
        try:
            role = self.request.user.profile.role
        except UserProfile.DoesNotExist:
            return queryset.none()
        if role == UserProfile.Role.GESTOR:
            return queryset
        if role == UserProfile.Role.MOTORISTA:
            return queryset.filter(assigned_driver=self.request.user)
        return queryset.none()

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated(), IsGestorOrMotorista()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="assign-driver")
    def assign_driver(self, request, pk=None):
        delivery = self.get_object()
        serializer = AssignDriverSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        driver = serializer.validated_data["driver_id"]
        delivery.assigned_driver = driver
        delivery.save(update_fields=["assigned_driver", "updated_at"])
        return Response(
            DeliverySerializer(delivery, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get", "post"], url_path="route-alternatives")
    def route_alternatives(self, request, pk=None):
        """US-06 (FT-46): lista ou cadastra até duas alternativas de trajeto."""
        delivery = self.get_object()
        if request.method == "GET":
            serializer = RouteAlternativeSerializer(
                delivery.route_alternatives.all(), many=True
            )
            return Response(serializer.data)

        serializer = RouteAlternativeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            # Trava a entrega para que duas requisições simultâneas não
            # ultrapassem o limite de alternativas.
            locked = Delivery.objects.select_for_update().get(pk=delivery.pk)
            if locked.route_alternatives.count() >= RouteAlternative.MAX_PER_DELIVERY:
                return Response(
                    {"detail": ROUTE_LIMIT_MESSAGE},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(delivery=locked, created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
