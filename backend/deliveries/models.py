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


class RouteAlternative(models.Model):
    """Alternativa de trajeto informada manualmente pelo Gestor (US-06 / FT-46).

    Não há cálculo de rota: distância e duração são estimativas digitadas.
    """

    MAX_PER_DELIVERY = 2

    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        related_name="route_alternatives",
        verbose_name="Entrega",
    )
    distance_km = models.DecimalField("Distância estimada (km)", max_digits=7, decimal_places=2)
    duration_minutes = models.PositiveIntegerField("Duração estimada (min)")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_route_alternatives",
        verbose_name="Criado por",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]
        verbose_name = "Alternativa de trajeto"
        verbose_name_plural = "Alternativas de trajeto"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(distance_km__gt=0),
                name="route_alternative_distance_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(duration_minutes__gt=0),
                name="route_alternative_duration_positive",
            ),
        ]

    def __str__(self):
        return f"Alternativa de trajeto #{self.pk} da entrega #{self.delivery_id}"
