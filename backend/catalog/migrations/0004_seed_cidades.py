from django.db import migrations
from django.utils.text import slugify

from catalog.seed import CITIES


def seed(apps, schema_editor):
    City = apps.get_model("catalog", "City")
    for name, uf, latitude, longitude in CITIES:
        City.objects.update_or_create(
            name=name, uf=uf,
            defaults={"slug": slugify(name), "latitude": latitude, "longitude": longitude},
        )


def unseed(apps, schema_editor):
    apps.get_model("catalog", "City").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("catalog", "0003_cidades")]
    operations = [migrations.RunPython(seed, unseed)]
