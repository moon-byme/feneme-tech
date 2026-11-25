from django.contrib import admin

from catalog.models import CargoType


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "limit_c", "source_type", "is_derived")
    list_filter = ("category", "is_derived")
