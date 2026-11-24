"""US-13 / FT-59 — histórico real de status, autorização e persistência."""
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import UserProfile
from deliveries.models import Delivery, DeliveryStatusHistory

User = get_user_model()


class DeliveryStatusHistoryTests(APITestCase):
    def setUp(self):
        self.manager = self.make_user("gestor_ft59", UserProfile.Role.GESTOR)
        self.driver = self.make_user("motorista_ft59", UserProfile.Role.MOTORISTA)
        self.other = self.make_user("outro_ft59", UserProfile.Role.MOTORISTA)
        self.delivery = Delivery.objects.create(
            origin="Campina Grande",
            destination="João Pessoa",
            cargo_description="Carga fictícia FT-59",
            created_by=self.manager,
            assigned_driver=self.driver,
        )
        self.url = f"/api/deliveries/{self.delivery.pk}/status-history/"

    def make_user(self, username, role):
        user = User.objects.create_user(username=username, password="SenhaFT59Ficticia!")
        user.profile.role = role
        user.profile.save(update_fields=["role"])
        return user

    def client_as(self, user):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {AccessToken.for_user(user)}")
        return client

    def transition(self, status):
        response = self.client_as(self.driver).post(
            f"/api/deliveries/{self.delivery.pk}/update-status/",
            {"status": status}, format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_manager_sees_only_real_events_in_chronological_order(self):
        self.transition("EM_TRANSPORTE")
        self.transition("ENTREGUE")
        response = self.client_as(self.manager).get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["delivery_id"], self.delivery.pk)
        self.assertEqual(response.data["current_status"], "ENTREGUE")

        history = response.data["history"]
        self.assertEqual(len(history), 2)
        self.assertEqual(
            [(event["previous_status"], event["new_status"]) for event in history],
            [("PENDENTE", "EM_TRANSPORTE"), ("EM_TRANSPORTE", "ENTREGUE")],
        )
        self.assertEqual(
            [event["id"] for event in history],
            list(DeliveryStatusHistory.objects.filter(delivery=self.delivery)
                 .order_by("changed_at", "id").values_list("id", flat=True)),
        )
        for event in history:
            self.assertEqual(event["changed_by_username"], self.driver.username)
            self.assertIsNotNone(event["changed_at"])
            self.assertEqual(
                set(event), {"id", "previous_status", "new_status", "changed_by_username", "changed_at"},
            )

    def test_delivery_without_changes_returns_empty_history_and_current_status(self):
        response = self.client_as(self.manager).get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["current_status"], "PENDENTE")
        self.assertEqual(response.data["history"], [])
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_history_is_preserved_after_new_authentication(self):
        self.transition("EM_TRANSPORTE")
        self.transition("ENTREGUE")
        first = self.client_as(self.manager).get(self.url)
        self.assertEqual(first.status_code, 200)

        fresh_client = APIClient()
        login = fresh_client.post("/api/auth/login/", {
            "username": self.manager.username,
            "password": "SenhaFT59Ficticia!",
        }, format="json")
        self.assertEqual(login.status_code, 200, login.data)
        fresh_client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        second = fresh_client.get(self.url)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(second.data["history"], first.data["history"])
        self.assertEqual(second.data["current_status"], "ENTREGUE")
        self.assertEqual(DeliveryStatusHistory.objects.filter(delivery=self.delivery).count(), 2)

    def test_driver_and_anonymous_cannot_read_history(self):
        self.transition("EM_TRANSPORTE")
        self.assertEqual(self.client_as(self.driver).get(self.url).status_code, 403)
        self.assertEqual(self.client_as(self.other).get(self.url).status_code, 403)
        self.assertEqual(APIClient().get(self.url).status_code, 401)

    def test_nonexistent_delivery_returns_404_without_leaking_other_record(self):
        response = self.client_as(self.manager).get(
            "/api/deliveries/999999999/status-history/"
        )
        self.assertEqual(response.status_code, 404)
        self.assertNotIn(self.delivery.cargo_description, response.content.decode())

    def test_history_is_read_only_and_failed_transition_creates_no_event(self):
        client = self.client_as(self.manager)
        self.assertEqual(client.post(self.url, {}, format="json").status_code, 405)
        refused = self.client_as(self.driver).post(
            f"/api/deliveries/{self.delivery.pk}/update-status/",
            {"status": "ENTREGUE"}, format="json",
        )
        self.assertEqual(refused.status_code, 400)
        self.assertEqual(client.get(self.url).data["history"], [])
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.status, "PENDENTE")
