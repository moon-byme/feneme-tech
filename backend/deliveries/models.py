from django.conf import settings
from django.db import models

class Delivery(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"

    origin = models.CharField("Origem", max_length=180)
    destination = models.CharField("Destino", max_length=180)
    cargo_description = models.CharField("Descrição da carga", max_length=500)
    assigned_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_deliveries",
        verbose_name="Motorista atribuído",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_deliveries",
        verbose_name="Criado por",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        verbose_name = "Entrega"
        verbose_name_plural = "Entregas"

    def __str__(self):
        return f"Entrega #{self.pk}: {self.origin} → {self.destination}"
