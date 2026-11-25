from django.contrib import admin

from catalog.models import CargoType, City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "uf", "latitude", "longitude")
    list_filter = ("uf",)
    search_fields = ("name",)


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "limit_c", "source_type", "is_derived")
    list_filter = ("category", "is_derived")
