from django.db import migrations

from catalog.seed import CARGO_TYPES


def seed(apps, schema_editor):
    CargoType = apps.get_model("catalog", "CargoType")
    for position, item in enumerate(CARGO_TYPES, start=1):
        CargoType.objects.update_or_create(name=item["name"], defaults={**item, "position": position})


def unseed(apps, schema_editor):
    apps.get_model("catalog", "CargoType").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_tipos_carga")]
    operations = [migrations.RunPython(seed, unseed)]
