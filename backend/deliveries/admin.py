from django.contrib import admin
from deliveries.models import Delivery, RouteAlternative

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "assigned_driver", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("origin", "destination", "cargo_description", "assigned_driver__username")
    readonly_fields = ("created_at", "updated_at")


@admin.register(RouteAlternative)
class RouteAlternativeAdmin(admin.ModelAdmin):
    list_display = ("id", "delivery", "distance_km", "duration_minutes", "created_by", "created_at")
    search_fields = ("delivery__origin", "delivery__destination")
    readonly_fields = ("created_at",)
