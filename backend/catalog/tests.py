"""US-14 (FT-113) e US-15 (FT-114): lista única de cidades e catálogo de cargas."""
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import UserProfile
from catalog.models import CargoType, City

PASSWORD = "SenhaFicticia_123!"


def make_user(username, role):
    user = get_user_model().objects.create_user(username=username, password=PASSWORD)
    user.profile.role = role
    user.profile.save(update_fields=["role"])
    return user


class CargoCatalogApiTests(APITestCase):
    url = "/api/tipos-carga/"

    def setUp(self):
        self.manager = make_user("gestor_cat", UserProfile.Role.GESTOR)
        self.driver = make_user("motorista_cat", UserProfile.Role.MOTORISTA)

    def login(self, user):
        response = self.client.post(
            "/api/auth/login/", {"username": user.username, "password": PASSWORD}, format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_seed_has_the_seven_approved_cargo_types(self):
        """Decisão D4 (FT-112): 7 cargas com limite ≥ 20 °C; defensivos fora."""
        self.assertEqual(CargoType.objects.count(), 7)
        self.assertFalse(CargoType.objects.filter(limit_c__lt=20).exists())
        self.assertFalse(CargoType.objects.filter(name__icontains="defensivo").exists())

    def test_gestor_lists_cargo_types_with_limit_and_source(self):
        """CT-31: cada tipo traz categoria, limite e fonte; cosméticos como limite derivado."""
        self.login(self.manager)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)
        for item in response.data:
            self.assertGreaterEqual(item["limit_c"], 20)
            self.assertTrue(item["category"] and item["reference"] and item["source_name"])
            self.assertTrue(item["source_url"].startswith("https://"))
        derived = [item["name"] for item in response.data if item["is_derived"]]
        self.assertEqual(derived, ["Cosméticos e produtos de higiene"])
        self.assertEqual(response.data[0]["name"], "Tomate (maduro-verde)")

    def test_motorista_can_read_but_not_change_catalog(self):
        """CT-32: catálogo protegido; alterações pela API são negadas."""
        self.login(self.driver)
        self.assertEqual(self.client.get(self.url).status_code, status.HTTP_200_OK)
        first = CargoType.objects.first()
        attempts = [
            self.client.post(self.url, {"name": "Carga indevida", "limit_c": 40}, format="json"),
            self.client.patch(f"{self.url}{first.id}/", {"limit_c": 99}, format="json"),
            self.client.delete(f"{self.url}{first.id}/"),
        ]
        for response in attempts:
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        first.refresh_from_db()
        self.assertNotEqual(float(first.limit_c), 99)
        self.assertEqual(CargoType.objects.count(), 7)

    def test_gestor_cannot_change_catalog_either(self):
        self.login(self.manager)
        response = self.client.post(self.url, {"name": "X", "limit_c": 40}, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_catalog_requires_authentication(self):
        self.assertEqual(self.client.get(self.url).status_code, status.HTTP_401_UNAUTHORIZED)


class CityListApiTests(APITestCase):
    url = "/api/cidades/"

    def setUp(self):
        self.manager = make_user("gestor_cid", UserProfile.Role.GESTOR)
        self.driver = make_user("motorista_cid", UserProfile.Role.MOTORISTA)

    def login(self, user):
        response = self.client.post(
            "/api/auth/login/", {"username": user.username, "password": PASSWORD}, format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_seed_has_26_cities_in_13_states_plus_df(self):
        """Decisão D5 (FT-112): 26 cidades, 13 estados + DF; Sousa-PB fica fora."""
        self.assertEqual(City.objects.count(), 26)
        self.assertEqual(City.objects.values("uf").distinct().count(), 14)
        self.assertFalse(City.objects.filter(name="Sousa").exists())
        self.assertEqual(City.objects.values("slug").distinct().count(), 26)

    def test_gestor_lists_cities_with_label_and_coordinates(self):
        self.login(self.manager)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 26)
        campina = next(item for item in response.data if item["name"] == "Campina Grande")
        self.assertEqual(campina["label"], "Campina Grande - PB")
        self.assertEqual(campina["slug"], "campina-grande")
        self.assertAlmostEqual(campina["latitude"], -7.2307)
        self.assertAlmostEqual(campina["longitude"], -35.8817)

    def test_city_list_is_read_only(self):
        self.login(self.manager)
        first = City.objects.first()
        attempts = [
            self.client.post(self.url, {"name": "Sousa", "uf": "PB"}, format="json"),
            self.client.patch(f"{self.url}{first.id}/", {"name": "X"}, format="json"),
            self.client.delete(f"{self.url}{first.id}/"),
        ]
        for response in attempts:
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(City.objects.count(), 26)

    def test_city_list_requires_authentication(self):
        self.assertEqual(self.client.get(self.url).status_code, status.HTTP_401_UNAUTHORIZED)
