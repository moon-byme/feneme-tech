from django.contrib import admin
from deliveries.models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "assigned_driver", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("origin", "destination", "cargo_description", "assigned_driver__username")
    readonly_fields = ("created_at", "updated_at")
