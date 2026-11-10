from decimal import Decimal

from rest_framework import serializers
from accounts.models import UserProfile
from deliveries.models import Delivery, RouteAlternative

# Limites de sanidade para valores digitados manualmente (US-06 / FT-46).
MAX_DISTANCE_KM = Decimal("5000")
MAX_DURATION_MINUTES = 7 * 24 * 60


class RouteAlternativeSerializer(serializers.ModelSerializer):
    distance_km = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
        min_value=Decimal("0.01"),
        max_value=MAX_DISTANCE_KM,
        coerce_to_string=False,
        error_messages={
            "required": "Informe a distância estimada em km.",
            "null": "Informe a distância estimada em km.",
            "invalid": "Informe a distância como um número em km (ex.: 125,5).",
            "min_value": "A distância deve ser maior que zero.",
            "max_value": f"A distância deve ser de no máximo {MAX_DISTANCE_KM} km.",
            "max_decimal_places": "Use no máximo duas casas decimais na distância.",
            "max_digits": f"A distância deve ser de no máximo {MAX_DISTANCE_KM} km.",
            "max_whole_digits": f"A distância deve ser de no máximo {MAX_DISTANCE_KM} km.",
        },
    )
    duration_minutes = serializers.IntegerField(
        min_value=1,
        max_value=MAX_DURATION_MINUTES,
        error_messages={
            "required": "Informe a duração estimada em minutos.",
            "null": "Informe a duração estimada em minutos.",
            "invalid": "Informe a duração como um número inteiro de minutos.",
            "min_value": "A duração deve ser de pelo menos 1 minuto.",
            "max_value": f"A duração deve ser de no máximo {MAX_DURATION_MINUTES} minutos (7 dias).",
        },
    )

    class Meta:
        model = RouteAlternative
        fields = ["id", "delivery", "distance_km", "duration_minutes", "created_at"]
        read_only_fields = ["id", "delivery", "created_at"]


class DeliverySerializer(serializers.ModelSerializer):
    assigned_driver_username = serializers.CharField(
        source="assigned_driver.username", read_only=True, default=None
    )
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    route_alternatives = RouteAlternativeSerializer(many=True, read_only=True)

    class Meta:
        model = Delivery
        fields = [
            "id", "origin", "destination", "cargo_description",
            "assigned_driver", "assigned_driver_username",
            "created_by_username", "status", "route_alternatives",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "assigned_driver", "assigned_driver_username",
            "created_by_username", "status", "route_alternatives",
            "created_at", "updated_at",
        ]

    def validate_origin(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Informe a origem.")
        return value

    def validate_destination(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Informe o destino.")
        return value

    def validate_cargo_description(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Informe a descrição da carga.")
        return value

class AssignDriverSerializer(serializers.Serializer):
    driver_id = serializers.IntegerField(min_value=1)

    def validate_driver_id(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            driver = User.objects.select_related("profile").get(pk=value, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("O usuário informado não existe ou está inativo.")
        try:
            if driver.profile.role != UserProfile.Role.MOTORISTA:
                raise serializers.ValidationError("O usuário selecionado não possui perfil Motorista.")
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("O usuário selecionado não possui perfil Motorista.")
        return driver
