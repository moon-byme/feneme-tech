from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsGestor
from weather.client import ForecastUnavailable, fetch_daily_forecast
from weather.locations import LOCATIONS_BY_SLUG, REFERENCE_LOCATIONS

UNAVAILABLE_MESSAGE = (
    "Previsão indisponível no momento. O cadastro e a comparação manual continuam disponíveis."
)
FORECAST_NOTICE = "Previsão de temperatura ambiente; não é a temperatura medida da carga."


class ReferenceLocationListView(APIView):
    """Lista as localidades de demonstração (US-08 / FT-47)."""

    permission_classes = [IsGestor]

    def get(self, request):
        return Response(
            [{"slug": location.slug, "name": location.name} for location in REFERENCE_LOCATIONS]
        )


class DailyForecastView(APIView):
    """Máxima e mínima previstas para hoje na localidade (US-08 / FT-47)."""

    permission_classes = [IsGestor]

    def get(self, request):
        slug = request.query_params.get("location", "")
        location = LOCATIONS_BY_SLUG.get(slug)
        if location is None:
            return Response(
                {"location": ["Selecione uma localidade de referência válida."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            forecast = fetch_daily_forecast(location)
        except ForecastUnavailable:
            return Response(
                {"detail": UNAVAILABLE_MESSAGE},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {
                "location": {"slug": location.slug, "name": location.name},
                "date": forecast.date.isoformat(),
                "temperature_max": forecast.temperature_max,
                "temperature_min": forecast.temperature_min,
                "unit": "°C",
                "source": "Open-Meteo",
                "notice": FORECAST_NOTICE,
            }
        )
