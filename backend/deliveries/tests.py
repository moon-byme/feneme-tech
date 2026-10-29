from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import UserProfile
from deliveries.models import Delivery

class FenemeDeliveryFlowTests(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username="gestor_teste", password="SenhaSegura123!")
        self.manager.profile.role = UserProfile.Role.GESTOR
        self.manager.profile.save()
        self.driver = User.objects.create_user(username="motorista_teste", password="SenhaSegura123!")
        self.driver.profile.role = UserProfile.Role.MOTORISTA
        self.driver.profile.save()
        self.login_url = "/api/auth/login/"
        self.deliveries_url = "/api/deliveries/"

    def login_as(self, username, password="SenhaSegura123!"):
        response = self.client.post(self.login_url, {"username": username, "password": password}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        return response.data

    def test_login_returns_role(self):
        """CT-01: login válido do Gestor retorna tokens e permite consultar entregas."""
        data = self.login_as("gestor_teste")
        self.assertEqual(data["user"]["role"], "GESTOR")
        self.assertIn("refresh", data)
        self.assertEqual(self.client.get(self.deliveries_url).status_code, status.HTTP_200_OK)

    def test_delivery_endpoints_require_authentication(self):
        response = self.client.get(self.deliveries_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_driver_list_only_shows_motorista_accounts_to_gestor(self):
        self.login_as("gestor_teste")
        response = self.client.get("/api/drivers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["username"] for item in response.data], ["motorista_teste"])

    def test_motorista_cannot_create_delivery(self):
        self.login_as("motorista_teste")
        response = self.client.post(self.deliveries_url, {
            "origin": "Campina Grande - PB",
            "destination": "João Pessoa - PB",
            "cargo_description": "Alimentos",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Delivery.objects.count(), 0)

    def test_gestor_can_create_and_list_delivery(self):
        """CT-03 / CT-15: cadastro persistido e consulta dos dados pelo Gestor."""
        self.login_as("gestor_teste")
        payload = {
            "origin": " Campina Grande - PB ",
            "destination": "João Pessoa - PB",
            "cargo_description": "Alimentos refrigerados",
        }
        created = self.client.post(self.deliveries_url, payload, format="json")
        self.assertEqual(created.status_code, status.HTTP_201_CREATED, created.data)
        self.assertEqual(created.data["origin"], "Campina Grande - PB")
        self.assertEqual(created.data["created_by_username"], "gestor_teste")
        delivery = Delivery.objects.get(pk=created.data["id"])
        self.assertEqual(delivery.origin, "Campina Grande - PB")
        self.assertEqual(delivery.destination, payload["destination"])
        self.assertEqual(delivery.cargo_description, payload["cargo_description"])
        self.assertEqual(delivery.created_by, self.manager)
        self.assertEqual(delivery.status, Delivery.Status.PENDENTE)
        listed = self.client.get(self.deliveries_url)
        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listed.data), 1)
        self.assertEqual(listed.data[0], created.data)

    def test_gestor_sees_empty_delivery_list(self):
        """CT-16: Gestor autenticado consulta uma base sem entregas e recebe lista vazia."""
        self.login_as("gestor_teste")
        self.assertEqual(Delivery.objects.count(), 0)
        response = self.client.get(self.deliveries_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_missing_required_fields_are_rejected(self):
        """CT-04: campos ausentes ou em branco são identificados, sem persistir entrega."""
        self.login_as("gestor_teste")
        required = {"origin", "destination", "cargo_description"}
        valid = {"origin": "A", "destination": "B", "cargo_description": "Carga teste"}
        cases = [({}, required), ({"origin": "A"}, {"destination", "cargo_description"})]
        for field in sorted(required):
            cases.append(({key: value for key, value in valid.items() if key != field}, {field}))
            cases.append(({**valid, field: "   "}, {field}))
        for payload, expected_fields in cases:
            with self.subTest(payload=payload):
                response = self.client.post(self.deliveries_url, payload, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(set(response.data), expected_fields)
                for field in expected_fields:
                    self.assertTrue(response.data[field], response.data)
                    self.assertTrue(all(str(message).strip() for message in response.data[field]))
                self.assertEqual(Delivery.objects.count(), 0)

    def test_gestor_can_assign_existing_driver(self):
        """CT-05: atribuição persiste e libera lista e detalhe para o Motorista responsável."""
        self.login_as("gestor_teste")
        created = self.client.post(self.deliveries_url, {
            "origin": "A", "destination": "B", "cargo_description": "Carga teste",
        }, format="json")
        response = self.client.post(
            f"{self.deliveries_url}{created.data['id']}/assign-driver/",
            {"driver_id": self.driver.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data["assigned_driver"], self.driver.id)
        self.assertEqual(response.data["assigned_driver_username"], "motorista_teste")
        delivery = Delivery.objects.get(pk=created.data["id"])
        self.assertEqual(delivery.assigned_driver, self.driver)
        detail_url = f"{self.deliveries_url}{delivery.id}/"
        self.assertEqual(self.client.get(detail_url).data["assigned_driver"], self.driver.id)
        self.login_as("motorista_teste")
        listed = self.client.get(self.deliveries_url)
        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in listed.data], [delivery.id])
        detail = self.client.get(detail_url)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["assigned_driver"], self.driver.id)

    def test_cannot_assign_user_with_manager_profile(self):
        """CT-17: rejeita usuário que não é Motorista e preserva a atribuição anterior."""
        self.login_as("gestor_teste")
        created = self.client.post(self.deliveries_url, {
            "origin": "A", "destination": "B", "cargo_description": "Carga teste",
        }, format="json")
        delivery = Delivery.objects.get(pk=created.data["id"])
        delivery.assigned_driver = self.driver
        delivery.save(update_fields=["assigned_driver"])
        response = self.client.post(
            f"{self.deliveries_url}{created.data['id']}/assign-driver/",
            {"driver_id": self.manager.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("driver_id", response.data)
        self.assertIn("não possui perfil Motorista", str(response.data["driver_id"]))
        delivery.refresh_from_db()
        self.assertEqual(delivery.assigned_driver, self.driver)
