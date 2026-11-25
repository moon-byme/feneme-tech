"""US-14 / FT-113: origem e destino da entrega pela lista única de cidades."""
from importlib import import_module

from django.apps import apps as django_apps
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import UserProfile
from catalog.models import City
from deliveries.models import Delivery

PASSWORD = "SenhaFicticia_123!"


def make_user(username, role):
    user = get_user_model().objects.create_user(username=username, password=PASSWORD)
    user.profile.role = role
    user.profile.save(update_fields=["role"])
    return user


class DeliveryCityTests(APITestCase):
    url = "/api/deliveries/"

    def setUp(self):
        self.manager = make_user("gestor_ft113", UserProfile.Role.GESTOR)
        self.client.force_authenticate(self.manager)
        self.campina = City.objects.get(slug="campina-grande")
        self.recife = City.objects.get(slug="recife")

    def post(self, **overrides):
        payload = {
            "origin_city": self.campina.id,
            "destination_city": self.recife.id,
            "cargo_description": "Carga fictícia FT-113",
        }
        payload.update(overrides)
        return self.client.post(self.url, payload, format="json")

    def test_cadastro_com_cidades_da_lista(self):
        response = self.post()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["origin_city"], self.campina.id)
        self.assertEqual(response.data["destination_city"], self.recife.id)
        self.assertEqual(response.data["origin"], "Campina Grande - PB")
        self.assertEqual(response.data["destination"], "Recife - PE")
        self.assertFalse(response.data["needs_review"])

    def test_origem_igual_ao_destino_e_rejeitada(self):
        response = self.post(destination_city=self.campina.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data), {"destination_city"})
        self.assertIn("diferente da origem", str(response.data["destination_city"][0]))
        self.assertFalse(Delivery.objects.exists())

    def test_cidade_inexistente_via_api_e_rejeitada(self):
        for value in (999999, "abc"):
            with self.subTest(value=value):
                response = self.post(origin_city=value)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("origin_city", response.data)
        self.assertFalse(Delivery.objects.exists())

    def test_texto_livre_nao_substitui_a_cidade(self):
        """Não é possível informar uma cidade fora da lista digitando o texto."""
        response = self.client.post(self.url, {
            "origin": "Sousa - PB", "destination": "Cidade Inventada",
            "cargo_description": "Carga fictícia",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data), {"origin_city", "destination_city"})
        created = self.post(origin="Texto ignorado")
        self.assertEqual(created.data["origin"], "Campina Grande - PB")


class LegacyDeliveryMigrationTests(APITestCase):
    """Migração 0005: vincula entregas antigas em texto livre ou marca para revisão."""

    def test_vincula_texto_reconhecido_e_marca_o_restante(self):
        manager = make_user("gestor_legado", UserProfile.Role.GESTOR)
        matched = Delivery.objects.create(
            origin="campina grande - pb", destination="Joao Pessoa/PB",
            cargo_description="Legada reconhecida", created_by=manager,
        )
        unmatched = Delivery.objects.create(
            origin="Sousa - PB", destination="Recife - PE",
            cargo_description="Legada parcial", created_by=manager,
        )
        migration = import_module("deliveries.migrations.0005_vincular_entregas_antigas_as_cidades")
        migration.link(django_apps, None)

        matched.refresh_from_db()
        unmatched.refresh_from_db()
        self.assertEqual(matched.origin_city.slug, "campina-grande")
        self.assertEqual(matched.destination_city.slug, "joao-pessoa")
        self.assertEqual(matched.origin, "Campina Grande - PB")
        self.assertFalse(matched.needs_review)
        self.assertIsNone(unmatched.origin_city)
        self.assertEqual(unmatched.origin, "Sousa - PB")
        self.assertEqual(unmatched.destination_city.slug, "recife")
        self.assertTrue(unmatched.needs_review)
