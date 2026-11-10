"""Cliente da Open-Meteo para a US-08 (FT-47) e o driver DA-CON-JA-01 (FT-32).

Qualquer falha externa (tempo esgotado, erro de conexão, HTTP diferente de
200 ou resposta sem os dados esperados) vira ``ForecastUnavailable``. O
motivo é registrado em log apenas por categoria, sem URL, corpo da resposta
ou traceback (DA-SEG / Q-06).
"""
import json
import logging
import math
import socket
from dataclasses import dataclass
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings

from weather.locations import ReferenceLocation

logger = logging.getLogger("feneme.weather")

FORECAST_TIMEZONE = "America/Fortaleza"
MAX_RESPONSE_BYTES = 64 * 1024


class ForecastUnavailable(Exception):
    """A previsão não pôde ser obtida; ``reason`` é uma categoria curta."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class DailyForecast:
    location: ReferenceLocation
    date: date
    temperature_max: float
    temperature_min: float


def _fail(location: ReferenceLocation, reason: str) -> ForecastUnavailable:
    logger.warning("Previsão Open-Meteo indisponível: localidade=%s motivo=%s", location.slug, reason)
    return ForecastUnavailable(reason)


def _read_temperature(daily: dict, key: str) -> float:
    values = daily.get(key)
    if not isinstance(values, list) or not values:
        raise ValueError(key)
    value = values[0]
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(key)
    return round(float(value), 1)


def fetch_daily_forecast(location: ReferenceLocation) -> DailyForecast:
    """Consulta máxima e mínima previstas para o dia atual na localidade."""
    query = urlencode(
        {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": FORECAST_TIMEZONE,
            "forecast_days": 1,
        }
    )
    request = Request(
        f"{settings.OPEN_METEO_FORECAST_URL}?{query}",
        headers={"Accept": "application/json", "User-Agent": "feneme/1.0"},
    )

    try:
        with urlopen(request, timeout=settings.OPEN_METEO_TIMEOUT_SECONDS) as response:
            if response.status != 200:
                raise _fail(location, f"http_{response.status}")
            body = response.read(MAX_RESPONSE_BYTES + 1)
    except ForecastUnavailable:
        raise
    except HTTPError as error:
        raise _fail(location, f"http_{error.code}") from None
    except (TimeoutError, socket.timeout):
        raise _fail(location, "timeout") from None
    except URLError as error:
        reason = "timeout" if isinstance(error.reason, (TimeoutError, socket.timeout)) else "conexao"
        raise _fail(location, reason) from None
    except OSError:
        raise _fail(location, "conexao") from None

    if len(body) > MAX_RESPONSE_BYTES:
        raise _fail(location, "resposta_muito_grande")

    try:
        payload = json.loads(body)
        daily = payload["daily"]
        forecast_date = date.fromisoformat(daily["time"][0])
        temperature_max = _read_temperature(daily, "temperature_2m_max")
        temperature_min = _read_temperature(daily, "temperature_2m_min")
    except (ValueError, KeyError, IndexError, TypeError):
        raise _fail(location, "dados_ausentes_ou_invalidos") from None

    if temperature_min > temperature_max:
        raise _fail(location, "dados_inconsistentes")

    return DailyForecast(location, forecast_date, temperature_max, temperature_min)
