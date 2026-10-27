import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="Delivery",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("origin", models.CharField(max_length=180, verbose_name="Origem")),
                ("destination", models.CharField(max_length=180, verbose_name="Destino")),
                ("cargo_description", models.CharField(max_length=500, verbose_name="Descrição da carga")),
                ("status", models.CharField(choices=[("PENDENTE", "Pendente")], default="PENDENTE", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("assigned_driver", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="assigned_deliveries", to=settings.AUTH_USER_MODEL, verbose_name="Motorista atribuído")),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="created_deliveries", to=settings.AUTH_USER_MODEL, verbose_name="Criado por")),
            ],
            options={
                "verbose_name": "Entrega",
                "verbose_name_plural": "Entregas",
                "ordering": ["-created_at", "-id"],
            },
        ),
    ]
