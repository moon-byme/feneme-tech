from rest_framework import serializers

from catalog.models import CargoType


class CargoTypeSerializer(serializers.ModelSerializer):
    limit_c = serializers.DecimalField(max_digits=4, decimal_places=1, coerce_to_string=False)

    class Meta:
        model = CargoType
        fields = [
            "id", "name", "category", "limit_c", "reference",
            "source_name", "source_url", "source_type", "is_derived",
        ]
