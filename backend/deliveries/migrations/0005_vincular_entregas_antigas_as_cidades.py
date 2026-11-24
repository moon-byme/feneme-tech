"""US-14 (FT-113): entregas anteriores à lista de cidades tinham origem e destino
em texto livre. Quando o texto corresponde a uma cidade da lista, a entrega é
vinculada; quando não corresponde, fica marcada para revisão pelo Gestor (a
API expõe ``needs_review`` e a interface mostra o aviso).
"""
import unicodedata

from django.db import migrations


def normalize(text):
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    return " ".join(text.lower().replace("/", " - ").split())


def link(apps, schema_editor):
    City = apps.get_model("catalog", "City")
    Delivery = apps.get_model("deliveries", "Delivery")
    known = {}
    for city in City.objects.all():
        known[normalize(f"{city.name} - {city.uf}")] = city
        known[normalize(f"{city.name}-{city.uf}")] = city
        known.setdefault(normalize(city.name), city)
    for delivery in Delivery.objects.filter(origin_city__isnull=True) | Delivery.objects.filter(destination_city__isnull=True):
        origin = known.get(normalize(delivery.origin))
        destination = known.get(normalize(delivery.destination))
        changed = []
        if origin and delivery.origin_city_id is None:
            delivery.origin_city = origin
            delivery.origin = f"{origin.name} - {origin.uf}"
            changed += ["origin_city", "origin"]
        if destination and delivery.destination_city_id is None and destination != origin:
            delivery.destination_city = destination
            delivery.destination = f"{destination.name} - {destination.uf}"
            changed += ["destination_city", "destination"]
        if changed:
            delivery.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [
        ("deliveries", "0004_cidades_origem_destino"),
        ("catalog", "0004_seed_cidades"),
    ]
    operations = [migrations.RunPython(link, migrations.RunPython.noop)]
