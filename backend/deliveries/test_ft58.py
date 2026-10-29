from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import UserProfile
from deliveries.models import Delivery

User = get_user_model()


class DriverDeliveryListTests(APITestCase):
    url = "/api/deliveries/"

    @classmethod
    def setUpTestData(cls):
        cls.manager = cls._user("gestor_ft58", UserProfile.Role.GESTOR)
        cls.driver_a = cls._user("driver_a_ft58", UserProfile.Role.MOTORISTA)
        cls.driver_b = cls._user("driver_b_ft58", UserProfile.Role.MOTORISTA)
        cls.delivery_a = cls._delivery(cls.driver_a)
        cls.delivery_b = cls._delivery(cls.driver_b)
        cls.unassigned = cls._delivery(None)

    @classmethod
    def _user(cls, username, role):
        user = User.objects.create_user(username=username, password="SenhaSegura123!")
        user.profile.role = role
        user.profile.save(update_fields=["role"])
        return user

    @classmethod
    def _delivery(cls, driver):
        return Delivery.objects.create(
            origin="Campina Grande", destination="João Pessoa",
            cargo_description="Alimentos", assigned_driver=driver, created_by=cls.manager,
        )

    def test_driver_only_lists_own_deliveries(self):
        self.client.force_authenticate(user=self.driver_a)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.delivery_a.id])

    def test_query_parameters_cannot_change_authenticated_driver(self):
        self.client.force_authenticate(user=self.driver_a)
        response = self.client.get(self.url, {
            "assigned_driver": self.driver_b.id, "driver_id": self.driver_b.id,
            "user_id": self.driver_b.id, "role": "GESTOR",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.delivery_a.id])

    def test_driver_with_no_assignments_sees_empty_list(self):
        self.delivery_a.assigned_driver = None
        self.delivery_a.save(update_fields=["assigned_driver"])
        self.client.force_authenticate(user=self.driver_a)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_other_and_unassigned_deliveries_are_hidden_like_missing_delivery(self):
        self.client.force_authenticate(user=self.driver_a)
        missing = self.client.get(f"{self.url}{self.unassigned.id + 1}/")
        self.assertEqual(missing.status_code, status.HTTP_404_NOT_FOUND)
        for delivery in [self.delivery_b, self.unassigned]:
            with self.subTest(delivery=delivery.id):
                response = self.client.get(f"{self.url}{delivery.id}/")
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data, missing.data)
                for value in [delivery.origin, delivery.destination, delivery.cargo_description]:
                    self.assertNotIn(value, response.content.decode())

    def test_driver_can_read_own_delivery_detail(self):
        self.client.force_authenticate(user=self.driver_a)
        response = self.client.get(f"{self.url}{self.delivery_a.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.delivery_a.id)
        self.assertEqual(response.data["origin"], self.delivery_a.origin)
        self.assertEqual(response.data["destination"], self.delivery_a.destination)
        self.assertEqual(response.data["cargo_description"], self.delivery_a.cargo_description)
        self.assertEqual(response.data["status"], self.delivery_a.status)

    def test_head_respects_driver_visibility(self):
        self.client.force_authenticate(user=self.driver_a)
        self.assertEqual(self.client.head(self.url).status_code, status.HTTP_200_OK)
        for delivery, expected in [
            (self.delivery_a, status.HTTP_200_OK),
            (self.delivery_b, status.HTTP_404_NOT_FOUND),
            (self.unassigned, status.HTTP_404_NOT_FOUND),
        ]:
            with self.subTest(delivery=delivery.id):
                self.assertEqual(self.client.head(f"{self.url}{delivery.id}/").status_code, expected)

    def test_driver_cannot_create_or_reassign_any_delivery(self):
        self.client.force_authenticate(user=self.driver_a)
        response = self.client.post(self.url, {
            "origin": "X", "destination": "Y", "cargo_description": "Z",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Delivery.objects.count(), 3)
        for delivery in [self.delivery_a, self.delivery_b, self.unassigned]:
            with self.subTest(delivery=delivery.id):
                previous_driver_id = delivery.assigned_driver_id
                response = self.client.post(
                    f"{self.url}{delivery.id}/assign-driver/",
                    {"driver_id": self.driver_b.id}, format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                delivery.refresh_from_db()
                self.assertEqual(delivery.assigned_driver_id, previous_driver_id)

    def test_driver_cannot_edit_or_delete_own_delivery(self):
        self.client.force_authenticate(user=self.driver_a)
        for method in ["put", "patch", "delete"]:
            with self.subTest(method=method):
                response = getattr(self.client, method)(
                    f"{self.url}{self.delivery_a.id}/", {"origin": "Alterada"}, format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.delivery_a.refresh_from_db()
        self.assertEqual(self.delivery_a.origin, "Campina Grande")

    def test_unauthenticated_cannot_read_deliveries(self):
        for url in [self.url, f"{self.url}{self.delivery_a.id}/"]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_gestor_still_sees_all_deliveries(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {item["id"] for item in response.data},
            {self.delivery_a.id, self.delivery_b.id, self.unassigned.id},
        )
        for delivery in [self.delivery_a, self.delivery_b, self.unassigned]:
            with self.subTest(delivery=delivery.id):
                self.assertEqual(
                    self.client.get(f"{self.url}{delivery.id}/").status_code, status.HTTP_200_OK,
                )

    def test_reassignment_immediately_changes_driver_visibility(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post(
            f"{self.url}{self.delivery_a.id}/assign-driver/",
            {"driver_id": self.driver_b.id}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.driver_a)
        self.assertEqual(self.client.get(self.url).data, [])
        self.assertEqual(
            self.client.get(f"{self.url}{self.delivery_a.id}/").status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.client.force_authenticate(user=self.driver_b)
        self.assertEqual(
            {item["id"] for item in self.client.get(self.url).data},
            {self.delivery_a.id, self.delivery_b.id},
        )
        self.assertEqual(
            self.client.get(f"{self.url}{self.delivery_a.id}/").status_code,
            status.HTTP_200_OK,
        )

    def test_account_without_profile_cannot_read_deliveries(self):
        self.manager.profile.delete()
        self.manager.refresh_from_db()
        self.client.force_authenticate(user=self.manager)
        for url in [self.url, f"{self.url}{self.delivery_a.id}/"]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, status.HTTP_403_FORBIDDEN)

    def test_unknown_profile_cannot_read_deliveries(self):
        self.manager.profile.role = "DESCONHECIDO"
        self.manager.profile.save(update_fields=["role"])
        self.client.force_authenticate(user=self.manager)
        for url in [self.url, f"{self.url}{self.delivery_a.id}/"]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, status.HTTP_403_FORBIDDEN)

    def test_stale_gestor_token_uses_current_database_role(self):
        token = AccessToken.for_user(self.manager)
        token["role"] = UserProfile.Role.GESTOR
        self.manager.profile.role = UserProfile.Role.MOTORISTA
        self.manager.profile.save(update_fields=["role"])
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        self.assertEqual(
            self.client.get(f"{self.url}{self.delivery_a.id}/").status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertEqual(
            self.client.post(self.url, {
                "origin": "X", "destination": "Y", "cargo_description": "Z",
            }, format="json").status_code,
            status.HTTP_403_FORBIDDEN,
        )
