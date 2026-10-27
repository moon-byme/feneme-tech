from rest_framework import serializers
from accounts.models import UserProfile
from deliveries.models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    assigned_driver_username = serializers.CharField(
        source="assigned_driver.username", read_only=True, default=None
    )
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )

    class Meta:
        model = Delivery
        fields = [
            "id", "origin", "destination", "cargo_description",
            "assigned_driver", "assigned_driver_username",
            "created_by_username", "status", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "assigned_driver", "assigned_driver_username",
            "created_by_username", "status", "created_at", "updated_at",
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
