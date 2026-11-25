"""Fontes únicas do Feneme: cidades (US-14 / FT-113) e tipos de carga (US-15 / FT-114)."""
from django.db import models


class City(models.Model):
    """Cidade da lista fechada. A mesma lista serve ao cadastro de entregas e ao clima."""

    name = models.CharField("Nome", max_length=80)
    uf = models.CharField("UF", max_length=2)
    slug = models.SlugField(unique=True, max_length=90)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        ordering = ["name", "uf"]
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
        constraints = [
            models.UniqueConstraint(fields=["name", "uf"], name="city_name_uf_unique"),
        ]

    def __str__(self):
        return self.label

    @property
    def label(self) -> str:
        return f"{self.name} - {self.uf}"


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
