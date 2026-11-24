"""Catálogos do Feneme. US-15 / FT-114: tipos de carga com limite de temperatura e fonte."""
from django.db import models


class CargoType(models.Model):
    """Tipo de carga com limite de temperatura de referência e a fonte do limite."""

    name = models.CharField("Carga", max_length=120, unique=True)
    category = models.CharField("Categoria", max_length=60)
    limit_c = models.DecimalField("Limite de referência (°C)", max_digits=4, decimal_places=1)
    reference = models.CharField("Referência na fonte", max_length=255)
    source_name = models.CharField("Fonte", max_length=160)
    source_url = models.URLField("Link da fonte", max_length=500)
    source_type = models.CharField("Tipo de fonte", max_length=60)
    is_derived = models.BooleanField(
        "Limite derivado",
        default=False,
        help_text="Marque quando o limite não vem direto da fonte; a interface mostra 'limite derivado'.",
    )
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position", "name"]
        verbose_name = "Tipo de carga"
        verbose_name_plural = "Tipos de carga"

    def __str__(self):
        return f"{self.name} ({self.limit_c} °C)"
