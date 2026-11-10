"""Localidades de demonstração da US-08 (FT-47).

Decisão do PO (10/11/2026): lista fixa com coordenadas pré-definidas,
sem geocodificação nem roteamento.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceLocation:
    slug: str
    name: str
    latitude: float
    longitude: float


REFERENCE_LOCATIONS = (
    ReferenceLocation("joao-pessoa", "João Pessoa - PB", -7.1195, -34.8450),
    ReferenceLocation("campina-grande", "Campina Grande - PB", -7.2307, -35.8817),
    ReferenceLocation("patos", "Patos - PB", -7.0244, -37.2800),
    ReferenceLocation("sousa", "Sousa - PB", -6.7597, -38.2286),
    ReferenceLocation("recife", "Recife - PE", -8.0476, -34.8770),
)

LOCATIONS_BY_SLUG = {location.slug: location for location in REFERENCE_LOCATIONS}
