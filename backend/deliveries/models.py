from django.conf import settings
from django.db import models

class Delivery(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        EM_TRANSPORTE = "EM_TRANSPORTE", "Em transporte"
        ENTREGUE = "ENTREGUE", "Entregue"

    # Texto exibido ("Cidade - UF"). Desde a US-14 (FT-113) é preenchido a partir
    # da cidade escolhida; só guarda texto livre nas entregas anteriores à lista.
    origin = models.CharField("Origem", max_length=180, blank=True)
    destination = models.CharField("Destino", max_length=180, blank=True)
    origin_city = models.ForeignKey(
        "catalog.City", on_delete=models.PROTECT, null=True, blank=True,
        related_name="deliveries_from", verbose_name="Cidade de origem",
    )
    destination_city = models.ForeignKey(
        "catalog.City", on_delete=models.PROTECT, null=True, blank=True,
        related_name="deliveries_to", verbose_name="Cidade de destino",
    )
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

    def save(self, *args, **kwargs):
        if self.origin_city_id:
            self.origin = self.origin_city.label
        if self.destination_city_id:
            self.destination = self.destination_city.label
        update_fields = kwargs.get("update_fields")
        if update_fields is not None and (self.origin_city_id or self.destination_city_id):
            kwargs["update_fields"] = set(update_fields) | {"origin", "destination"}
        super().save(*args, **kwargs)

    @property
    def needs_review(self) -> bool:
        """Entrega anterior à lista de cidades cuja origem ou destino não foi reconhecido."""
        return not (self.origin_city_id and self.destination_city_id)


class DeliveryStatusHistory(models.Model):
    """Eventos persistentes da US-11; base da consulta cronológica da FT-59."""

    delivery = models.ForeignKey(
        Delivery, on_delete=models.PROTECT, related_name="status_history",
    )
    previous_status = models.CharField(max_length=20, choices=Delivery.Status.choices)
    new_status = models.CharField(max_length=20, choices=Delivery.Status.choices)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="delivery_status_changes",
    )
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["changed_at", "id"]
        indexes = [models.Index(fields=["delivery", "changed_at", "id"], name="delivery_history_chronological")]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(previous_status="PENDENTE", new_status="EM_TRANSPORTE")
                    | models.Q(previous_status="EM_TRANSPORTE", new_status="ENTREGUE")
                ),
                name="delivery_history_valid_transition",
            ),
            models.UniqueConstraint(
                fields=["delivery", "previous_status"], name="delivery_history_unique_transition",
            ),
        ]


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
