"""Testes da US-06 (FT-46) — Cadastrar alternativas de trajeto.

Cobrem os cenários Gherkin da história (CT-18 e CT-07): registro de até duas
alternativas válidas, bloqueio da terceira e rejeição de valores inválidos,
além das regras de permissão do Gestor.
"""
from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import UserProfile
from deliveries.models import Delivery, RouteAlternative

PASSWORD = "SenhaSegura123!"


class RouteAlternativeTests(APITestCase):
    def setUp(self):
        self.manager = self.make_user("gestor_ft46", UserProfile.Role.GESTOR)
        self.driver = self.make_user("motorista_ft46", UserProfile.Role.MOTORISTA)
        self.delivery = Delivery.objects.create(
            origin="Campina Grande - PB",
            destination="João Pessoa - PB",
            cargo_description="Frutas refrigeradas",
            created_by=self.manager,
            assigned_driver=self.driver,
        )
        self.other_delivery = Delivery.objects.create(
            origin="Patos - PB",
            destination="Sousa - PB",
            cargo_description="Laticínios",
            created_by=self.manager,
        )
        self.url = self.url_for(self.delivery)

    @staticmethod
    def make_user(username, role):
        user = User.objects.create_user(username=username, password=PASSWORD)
        user.profile.role = role
        user.profile.save(update_fields=["role"])
        return user

    @staticmethod
    def url_for(delivery):
        return f"/api/deliveries/{delivery.pk}/route-alternatives/"

    def login_as(self, username):
        response = self.client.post(
            "/api/auth/login/", {"username": username, "password": PASSWORD}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def post_alternative(self, distance_km, duration_minutes, url=None):
        return self.client.post(
            url or self.url,
            {"distance_km": distance_km, "duration_minutes": duration_minutes},
            format="json",
        )

    # Cenário: Registrar alternativas válidas (CT-18)
    def test_gestor_registers_two_valid_alternatives(self):
        self.login_as("gestor_ft46")

        first = self.post_alternative("125.50", 110)
        second = self.post_alternative(140, 95)

        self.assertEqual(first.status_code, status.HTTP_201_CREATED, first.data)
        self.assertEqual(second.status_code, status.HTTP_201_CREATED, second.data)
        self.assertEqual(first.data["delivery"], self.delivery.pk)
        self.assertEqual(first.data["distance_km"], Decimal("125.50"))
        self.assertEqual(first.data["duration_minutes"], 110)

        saved = list(self.delivery.route_alternatives.values_list("distance_km", "duration_minutes", "created_by"))
        self.assertEqual(
            saved,
            [(Decimal("125.50"), 110, self.manager.pk), (Decimal("140.00"), 95, self.manager.pk)],
        )
        self.assertFalse(self.other_delivery.route_alternatives.exists())

    def test_alternatives_are_returned_with_the_delivery(self):
        self.login_as("gestor_ft46")
        self.post_alternative("125.50", 110)

        listed = self.client.get(self.url)
        detail = self.client.get(f"/api/deliveries/{self.delivery.pk}/")

        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listed.data), 1)
        self.assertEqual(listed.data[0]["duration_minutes"], 110)
        self.assertEqual(len(detail.data["route_alternatives"]), 1)
        self.assertEqual(detail.data["route_alternatives"][0]["distance_km"], Decimal("125.50"))

    def test_payload_cannot_redirect_alternative_to_another_delivery(self):
        self.login_as("gestor_ft46")
        response = self.client.post(
            self.url,
            {"distance_km": 50, "duration_minutes": 40, "delivery": self.other_delivery.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["delivery"], self.delivery.pk)
        self.assertFalse(self.other_delivery.route_alternatives.exists())

    # Cenário: Terceira alternativa (CT-07)
    def test_third_alternative_is_rejected_with_limit_message(self):
        self.login_as("gestor_ft46")
        self.post_alternative(100, 90)
        self.post_alternative(120, 80)

        response = self.post_alternative(130, 70)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("limite é de 2 alternativas", response.data["detail"])
        self.assertEqual(self.delivery.route_alternatives.count(), 2)

    def test_limit_is_counted_per_delivery(self):
        self.login_as("gestor_ft46")
        self.post_alternative(100, 90)
        self.post_alternative(120, 80)

        response = self.post_alternative(30, 25, url=self.url_for(self.other_delivery))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Cenário: Dados inválidos (CT-07)
    def test_invalid_distance_is_rejected_and_identified(self):
        self.login_as("gestor_ft46")
        for distance in (0, -10, "abc", "12.345", 5000.01, None, ""):
            with self.subTest(distance=distance):
                response = self.post_alternative(distance, 60)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(set(response.data), {"distance_km"})
                self.assertTrue(response.data["distance_km"][0])
        self.assertFalse(RouteAlternative.objects.exists())

    def test_invalid_duration_is_rejected_and_identified(self):
        self.login_as("gestor_ft46")
        for duration in (0, -5, "1h", 90.5, 10081, None, ""):
            with self.subTest(duration=duration):
                response = self.post_alternative(100, duration)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(set(response.data), {"duration_minutes"})
        self.assertFalse(RouteAlternative.objects.exists())

    def test_missing_fields_are_all_identified(self):
        self.login_as("gestor_ft46")
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data), {"distance_km", "duration_minutes"})
        self.assertEqual(response.data["distance_km"][0], "Informe a distância estimada em km.")

    def test_invalid_data_does_not_consume_the_limit(self):
        self.login_as("gestor_ft46")
        self.post_alternative(100, 90)
        self.post_alternative(0, 90)
        response = self.post_alternative(120, 80)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Permissões
    def test_motorista_cannot_register_or_list_alternatives(self):
        self.login_as("motorista_ft46")
        self.assertEqual(self.post_alternative(100, 90).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get(self.url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(RouteAlternative.objects.exists())

    def test_anonymous_request_is_rejected(self):
        self.assertEqual(self.post_alternative(100, 90).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.get(self.url).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unknown_delivery_returns_404(self):
        self.login_as("gestor_ft46")
        response = self.post_alternative(100, 90, url="/api/deliveries/999999/route-alternatives/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(RouteAlternative.objects.exists())
