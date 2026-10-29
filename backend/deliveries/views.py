from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import UserProfile
from accounts.permissions import IsGestor, IsGestorOrMotorista
from deliveries.models import Delivery
from deliveries.serializers import DeliverySerializer, AssignDriverSerializer

class DeliveryViewSet(viewsets.ModelViewSet):
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, IsGestor]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        queryset = Delivery.objects.select_related(
            "assigned_driver", "created_by"
        )
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
