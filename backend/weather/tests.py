"""Testes da US-08 (FT-47) — previsão de temperatura via Open-Meteo.

A Open-Meteo é sempre simulada (``urlopen`` substituído): nenhum teste faz
chamada externa. Os cenários de falha cobrem CT-09 e alimentam o driver
DA-CON-JA-01 (FT-32): tempo esgotado, erro de conexão, HTTP 5xx/4xx,
resposta inválida, previsão ausente e valores inconsistentes.
"""
import io
import json
import socket
from unittest import mock
from urllib.error import HTTPError, URLError

from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import UserProfile
from deliveries.models import Delivery

PASSWORD = "SenhaSegura123!"
FORECAST_URL = "/api/weather/forecast/"
URLOPEN = "weather.client.urlopen"
UNAVAILABLE = "Previsão indisponível no momento. O cadastro e a comparação manual continuam disponíveis."


def open_meteo_payload(max_value=31.24, min_value=23.46, day="2026-11-10"):
    return {
        "latitude": -7.12,
        "longitude": -34.84,
        "timezone": "America/Fortaleza",
        "daily_units": {"temperature_2m_max": "°C", "temperature_2m_min": "°C"},
        "daily": {
            "time": [day],
            "temperature_2m_max": [max_value],
            "temperature_2m_min": [min_value],
        },
    }


class FakeResponse(io.BytesIO):
    def __init__(self, body, status_code=200):
        super().__init__(body if isinstance(body, bytes) else json.dumps(body).encode())
        self.status = status_code

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


@override_settings(OPEN_METEO_FORECAST_URL="https://open-meteo.test/v1/forecast", OPEN_METEO_TIMEOUT_SECONDS=5)
class ForecastApiTests(APITestCase):
    def setUp(self):
        self.manager = self.make_user("gestor_ft47", UserProfile.Role.GESTOR)
        self.driver = self.make_user("motorista_ft47", UserProfile.Role.MOTORISTA)

    @staticmethod
    def make_user(username, role):
        user = User.objects.create_user(username=username, password=PASSWORD)
        user.profile.role = role
        user.profile.save(update_fields=["role"])
        return user

    def login_as(self, username):
        response = self.client.post(
            "/api/auth/login/", {"username": username, "password": PASSWORD}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def get_forecast(self, location="joao-pessoa"):
        return self.client.get(FORECAST_URL, {"location": location})

    # CT-20: previsão disponível
    def test_returns_daily_max_and_min_for_reference_location(self):
        self.login_as("gestor_ft47")
        with mock.patch(URLOPEN, return_value=FakeResponse(open_meteo_payload())) as fake:
            response = self.get_forecast()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "location": {"slug": "joao-pessoa", "name": "João Pessoa - PB"},
                "date": "2026-11-10",
                "temperature_max": 31.2,
                "temperature_min": 23.5,
                "unit": "°C",
                "source": "Open-Meteo",
                "notice": "Previsão de temperatura ambiente; não é a temperatura medida da carga.",
            },
        )
        request = fake.call_args.args[0]
        self.assertIn("latitude=-7.1195", request.full_url)
        self.assertIn("longitude=-34.845", request.full_url)
        self.assertIn("daily=temperature_2m_max%2Ctemperature_2m_min", request.full_url)
        self.assertIn("forecast_days=1", request.full_url)
        self.assertIn("timezone=America%2FFortaleza", request.full_url)
        self.assertEqual(fake.call_args.kwargs["timeout"], 5)

    def test_lists_reference_locations(self):
        self.login_as("gestor_ft47")
        response = self.client.get("/api/weather/locations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [item["slug"] for item in response.data],
            ["joao-pessoa", "campina-grande", "patos", "sousa", "recife"],
        )

    def test_unknown_or_missing_location_is_rejected_without_calling_api(self):
        self.login_as("gestor_ft47")
        with mock.patch(URLOPEN) as fake:
            for location in ("", "sao-paulo", "../../etc", "https://evil.test"):
                with self.subTest(location=location):
                    response = self.get_forecast(location)
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                    self.assertIn("location", response.data)
        fake.assert_not_called()

    # CT-09 / FT-32: falhas da Open-Meteo
    def test_external_failures_return_503_with_generic_message(self):
        failures = {
            "timeout": socket.timeout("timed out"),
            "timeout_error": TimeoutError(),
            "url_timeout": URLError(socket.timeout("timed out")),
            "conexao": URLError(ConnectionRefusedError("refused")),
            "dns": URLError(socket.gaierror("Name or service not known")),
            "http_500": HTTPError("https://open-meteo.test/v1/forecast?secret", 500, "Server Error", {}, None),
            "http_503": HTTPError("https://open-meteo.test/v1/forecast", 503, "Unavailable", {}, None),
            "http_429": HTTPError("https://open-meteo.test/v1/forecast", 429, "Too Many", {}, None),
            "status_204": FakeResponse(b"", status_code=204),
            "json_invalido": FakeResponse(b"<html>erro</html>"),
            "sem_daily": FakeResponse({"error": True, "reason": "Latitude must be in range"}),
            "lista_vazia": FakeResponse({"daily": {"time": [], "temperature_2m_max": [], "temperature_2m_min": []}}),
            "valor_nulo": FakeResponse(open_meteo_payload(max_value=None)),
            "valor_texto": FakeResponse(open_meteo_payload(min_value="23")),
            "valor_nan": FakeResponse(b'{"daily": {"time": ["2026-11-10"], "temperature_2m_max": [NaN], "temperature_2m_min": [20]}}'),
            "data_invalida": FakeResponse(open_meteo_payload(day="10/11/2026")),
            "min_maior_que_max": FakeResponse(open_meteo_payload(max_value=20, min_value=25)),
            "resposta_grande": FakeResponse(b"{" + b" " * (70 * 1024) + b"}"),
        }
        self.login_as("gestor_ft47")
        for name, outcome in failures.items():
            with self.subTest(failure=name):
                side_effect = outcome if isinstance(outcome, BaseException) else None
                return_value = None if side_effect else outcome
                with mock.patch(URLOPEN, side_effect=side_effect, return_value=return_value), \
                        self.assertLogs("feneme.weather", level="WARNING") as logs:
                    response = self.get_forecast()

                self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
                self.assertEqual(response.data, {"detail": UNAVAILABLE})
                body = response.content.decode()
                log_text = "\n".join(logs.output)
                for leaked in ("open-meteo.test", "Traceback", "secret", "refused", "Latitude", "<html>"):
                    self.assertNotIn(leaked, body)
                    self.assertNotIn(leaked, log_text)

    def test_failure_keeps_delivery_and_route_flows_available(self):
        self.login_as("gestor_ft47")
        with mock.patch(URLOPEN, side_effect=socket.timeout("timed out")):
            self.assertEqual(self.get_forecast().status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

        created = self.client.post(
            "/api/deliveries/",
            {"origin": "Patos - PB", "destination": "Sousa - PB", "cargo_description": "Frutas"},
            format="json",
        )
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        route = self.client.post(
            f"/api/deliveries/{created.data['id']}/route-alternatives/",
            {"distance_km": 64, "duration_minutes": 55},
            format="json",
        )
        self.assertEqual(route.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Delivery.objects.count(), 1)

    # Permissões
    def test_motorista_cannot_query_forecast_or_locations(self):
        self.login_as("motorista_ft47")
        with mock.patch(URLOPEN) as fake:
            self.assertEqual(self.get_forecast().status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.get("/api/weather/locations/").status_code, status.HTTP_403_FORBIDDEN)
        fake.assert_not_called()

    def test_anonymous_request_is_rejected(self):
        with mock.patch(URLOPEN) as fake:
            self.assertEqual(self.get_forecast().status_code, status.HTTP_401_UNAUTHORIZED)
        fake.assert_not_called()
