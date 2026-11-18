"""US-11: autorização, transições, auditoria, persistência e concorrência real."""
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from threading import Barrier, Event
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import close_old_connections, connection, transaction
from django.test import TransactionTestCase, skipUnlessDBFeature
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import UserProfile
from deliveries.models import Delivery, DeliveryStatusHistory

User = get_user_model()


class StatusFixtures:
    def make_user(self, username, role):
        user = User.objects.create_user(username=username)
        user.profile.role = role
        user.profile.save(update_fields=["role"])
        return user

    def setUp(self):
        super().setUp()
        self.manager = self.make_user("gestor_status", UserProfile.Role.GESTOR)
        self.driver = self.make_user("motorista_status", UserProfile.Role.MOTORISTA)
        self.other = self.make_user("outro_status", UserProfile.Role.MOTORISTA)
        self.delivery = self.make_delivery()
        self.url = f"/api/deliveries/{self.delivery.pk}/update-status/"

    def make_delivery(self, **kwargs):
        return Delivery.objects.create(**{
            "origin": "Campina Grande", "destination": "João Pessoa",
            "cargo_description": "Carga fictícia FT-48",
            "created_by": self.manager, "assigned_driver": self.driver, **kwargs,
        })

    def token_client(self, user):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {AccessToken.for_user(user)}")
        return client


class DeliveryStatusTests(StatusFixtures, APITestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.driver)

    def update(self, new_status, delivery=None):
        url = f"/api/deliveries/{delivery.pk}/update-status/" if delivery else self.url
        return self.client.post(url, {"status": new_status}, format="json")

    def test_every_status_transition_and_history(self):
        allowed = {("PENDENTE", "EM_TRANSPORTE"), ("EM_TRANSPORTE", "ENTREGUE")}
        for previous in Delivery.Status.values:
            for new in Delivery.Status.values:
                with self.subTest(previous=previous, new=new):
                    delivery = self.make_delivery(status=previous)
                    before = timezone.now()
                    response = self.update(new, delivery)
                    delivery.refresh_from_db()
                    if (previous, new) in allowed:
                        self.assertEqual(response.status_code, 200, response.data)
                        self.assertEqual(response.data["status"], new)
                        self.assertEqual(delivery.status, new)
                        event = delivery.status_history.get()
                        self.assertEqual(event.previous_status, previous)
                        self.assertEqual(event.new_status, new)
                        self.assertEqual(event.changed_by_id, self.driver.pk)
                        self.assertEqual(event.delivery_id, delivery.pk)
                        self.assertLessEqual(before, event.changed_at)
                        self.assertLessEqual(event.changed_at, timezone.now())
                    else:
                        self.assertEqual(response.status_code, 400, response.data)
                        self.assertEqual(delivery.status, previous)
                        self.assertFalse(delivery.status_history.exists())

    def test_valid_flow_records_chronological_events(self):
        for new in ["EM_TRANSPORTE", "ENTREGUE"]:
            self.assertEqual(self.update(new).status_code, 200)
        self.assertEqual(list(self.delivery.status_history.values_list(
            "previous_status", "new_status",
        )), [("PENDENTE", "EM_TRANSPORTE"), ("EM_TRANSPORTE", "ENTREGUE")])

    def test_invalid_missing_null_and_blank_status_leave_no_changes(self):
        for payload in [{}, {"status": None}, {"status": ""}, {"status": "CANCELADA"}, {"status": []}]:
            with self.subTest(payload=payload):
                response = self.client.post(self.url, payload, format="json")
                self.assertEqual(response.status_code, 400)
                self.delivery.refresh_from_db()
                self.assertEqual(self.delivery.status, "PENDENTE")
                self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_other_driver_and_unassigned_delivery_are_hidden(self):
        for driver in [self.other, None]:
            with self.subTest(driver=driver):
                delivery = self.make_delivery(assigned_driver=driver)
                response = self.update("EM_TRANSPORTE", delivery)
                self.assertEqual(response.status_code, 404)
                self.assertNotIn(delivery.cargo_description, str(response.data))
                delivery.refresh_from_db()
                self.assertEqual(delivery.status, "PENDENTE")
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_manager_cannot_update(self):
        self.client.force_authenticate(self.manager)
        self.assertEqual(self.update("EM_TRANSPORTE").status_code, 403)
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.status, "PENDENTE")
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_unauthenticated_and_invalid_tokens_cannot_update(self):
        self.client.force_authenticate(None)
        for token in [None, "invalido"]:
            with self.subTest(token=token):
                self.client.credentials(**({"HTTP_AUTHORIZATION": f"Bearer {token}"} if token else {}))
                self.assertEqual(self.update("EM_TRANSPORTE").status_code, 401)
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.status, "PENDENTE")
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_expired_token_cannot_update(self):
        token = AccessToken.for_user(self.driver)
        token["exp"] = 0
        self.client.force_authenticate(None)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(self.update("EM_TRANSPORTE").status_code, 401)
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_inactive_driver_cannot_update(self):
        client = self.token_client(self.driver)
        self.driver.is_active = False
        self.driver.save(update_fields=["is_active"])
        self.assertEqual(client.post(self.url, {"status": "EM_TRANSPORTE"}).status_code, 401)
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_missing_or_unknown_profile_cannot_update(self):
        client = self.token_client(self.driver)
        self.driver.profile.role = "DESCONHECIDO"
        self.driver.profile.save(update_fields=["role"])
        self.assertEqual(client.post(self.url, {"status": "EM_TRANSPORTE"}).status_code, 403)
        self.driver.profile.delete()
        self.assertEqual(client.post(self.url, {"status": "EM_TRANSPORTE"}).status_code, 403)
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_current_role_overrides_stale_driver_token(self):
        client = self.token_client(self.driver)
        self.driver.profile.role = UserProfile.Role.GESTOR
        self.driver.profile.save(update_fields=["role"])
        self.assertEqual(client.post(self.url, {"status": "EM_TRANSPORTE"}).status_code, 403)
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_nonexistent_delivery(self):
        self.assertEqual(self.client.post(
            "/api/deliveries/999999/update-status/", {"status": "EM_TRANSPORTE"},
        ).status_code, 404)
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_spoofed_driver_and_history_fields_are_ignored(self):
        response = self.client.post(self.url, {
            "status": "EM_TRANSPORTE", "driver_id": self.other.pk,
            "assigned_driver": self.other.pk, "changed_by": self.other.pk,
            "previous_status": "ENTREGUE", "changed_at": "2000-01-01T00:00:00Z",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.assigned_driver_id, self.driver.pk)
        event = self.delivery.status_history.get()
        self.assertEqual(event.changed_by_id, self.driver.pk)
        self.assertEqual(event.previous_status, "PENDENTE")
        self.assertEqual(event.changed_at.date(), timezone.now().date())

    def test_generic_edit_cannot_change_status(self):
        for actor, expected in [(self.manager, 405), (self.driver, 403)]:
            self.client.force_authenticate(actor)
            for method in ["patch", "put"]:
                with self.subTest(actor=actor.username, method=method):
                    response = getattr(self.client, method)(
                        f"/api/deliveries/{self.delivery.pk}/", {"status": "ENTREGUE"},
                    )
                    self.assertEqual(response.status_code, expected)
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.status, "PENDENTE")
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_creation_cannot_override_initial_status(self):
        self.client.force_authenticate(self.manager)
        response = self.client.post("/api/deliveries/", {
            "origin": "A", "destination": "B", "cargo_description": "Teste",
            "status": "ENTREGUE",
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Delivery.objects.get(pk=response.data["id"]).status, "PENDENTE")
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_history_failure_rolls_back_status_and_timestamp(self):
        old_timestamp = self.delivery.updated_at
        with patch("deliveries.views.DeliveryStatusHistory.objects.create", side_effect=RuntimeError("falha simulada")):
            with self.assertRaisesMessage(RuntimeError, "falha simulada"):
                self.update("EM_TRANSPORTE")
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.status, "PENDENTE")
        self.assertEqual(self.delivery.updated_at, old_timestamp)
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_save_failure_creates_no_history(self):
        with patch("deliveries.views.Delivery.save", side_effect=RuntimeError("falha simulada")):
            with self.assertRaisesMessage(RuntimeError, "falha simulada"):
                self.update("EM_TRANSPORTE")
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.status, "PENDENTE")
        self.assertFalse(DeliveryStatusHistory.objects.exists())

    def test_ft34_twenty_updates_recovered_after_reauthentication(self):
        # Dez entregas x duas transições válidas = 20 alterações persistidas.
        self.driver.set_password("SenhaTesteStatus!")
        self.driver.save(update_fields=["password"])
        deliveries = [self.make_delivery() for _ in range(10)]
        recovered = 0
        for delivery in deliveries:
            for new in ["EM_TRANSPORTE", "ENTREGUE"]:
                self.assertEqual(self.update(new, delivery).status_code, 200)
                # Nova sessão/autenticação e nova instância ORM, sem cache do cliente.
                client = APIClient()
                login = client.post("/api/auth/login/", {
                    "username": self.driver.username, "password": "SenhaTesteStatus!",
                })
                self.assertEqual(login.status_code, 200)
                client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
                response = client.get(f"/api/deliveries/{delivery.pk}/")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["status"], new)
                fresh = Delivery.objects.get(pk=delivery.pk)
                self.assertEqual(fresh.status, new)
                self.assertEqual(fresh.status_history.last().new_status, new)
                self.assertEqual(fresh.status_history.last().changed_by_id, self.driver.pk)
                recovered += 1
        self.assertEqual(recovered, 20)
        self.assertEqual(DeliveryStatusHistory.objects.count(), 20)

    def test_manager_reads_latest_persisted_status_in_list_and_detail(self):
        for new in ["EM_TRANSPORTE", "ENTREGUE"]:
            self.assertEqual(self.update(new).status_code, 200)
            manager = self.token_client(self.manager)
            detail = manager.get(f"/api/deliveries/{self.delivery.pk}/")
            self.assertEqual(detail.data["status"], new)
            listed = manager.get("/api/deliveries/")
            self.assertEqual(listed.status_code, 200)
            self.assertEqual(next(item for item in listed.data if item["id"] == self.delivery.pk)["status"], new)

    def test_reassignment_revokes_previous_driver_permission(self):
        self.assertEqual(self.update("EM_TRANSPORTE").status_code, 200)
        manager = self.token_client(self.manager)
        self.assertEqual(manager.post(
            f"/api/deliveries/{self.delivery.pk}/assign-driver/", {"driver_id": self.other.pk},
        ).status_code, 200)
        self.assertEqual(self.update("ENTREGUE").status_code, 404)
        self.assertEqual(self.client.get("/api/deliveries/").data, [])
        other = self.token_client(self.other)
        self.assertEqual(other.post(self.url, {"status": "ENTREGUE"}).status_code, 200)
        self.assertEqual(list(self.delivery.status_history.values_list("changed_by_id", flat=True)), [self.driver.pk, self.other.pk])


@skipUnlessDBFeature("has_select_for_update")
class DeliveryStatusConcurrencyTests(StatusFixtures, TransactionTestCase):
    def request_in_thread(self, token, new_status, started=None, barrier=None):
        close_old_connections()
        try:
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            if started:
                started.set()
            if barrier:
                barrier.wait(timeout=10)
            return client.post(self.url, {"status": new_status}).status_code
        finally:
            connection.close()

    def test_overlapping_requests_create_only_one_event_per_transition(self):
        token = str(AccessToken.for_user(self.driver))
        for new in ["EM_TRANSPORTE", "ENTREGUE"]:
            with self.subTest(status=new):
                writing_history, release, second_started = Event(), Event(), Event()
                create = DeliveryStatusHistory.objects.create

                def delayed_create(**kwargs):
                    writing_history.set()
                    if not release.wait(timeout=10):
                        raise RuntimeError("Timeout aguardando liberação do teste")
                    return create(**kwargs)

                with patch("deliveries.views.DeliveryStatusHistory.objects.create", side_effect=delayed_create):
                    with ThreadPoolExecutor(max_workers=2) as executor:
                        first = executor.submit(self.request_in_thread, token, new)
                        try:
                            self.assertTrue(writing_history.wait(timeout=10))
                            second = executor.submit(self.request_in_thread, token, new, second_started)
                            self.assertTrue(second_started.wait(timeout=10))
                            with self.assertRaises(TimeoutError):
                                second.result(timeout=0.25)
                        finally:
                            release.set()
                        self.assertEqual(first.result(timeout=10), 200)
                        self.assertEqual(second.result(timeout=10), 400)
                self.delivery.refresh_from_db()
                self.assertEqual(self.delivery.status, new)
                self.assertEqual(self.delivery.status_history.filter(new_status=new).count(), 1)

    def test_concurrent_different_targets_preserve_valid_history_chain(self):
        token, barrier = str(AccessToken.for_user(self.driver)), Barrier(2)
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(self.request_in_thread, token, new, None, barrier)
                       for new in ["EM_TRANSPORTE", "ENTREGUE"]]
            codes = [future.result(timeout=10) for future in futures]
        self.assertEqual(codes[0], 200)
        self.assertIn(codes[1], [200, 400])
        events = list(self.delivery.status_history.all())
        self.assertEqual(events[0].previous_status, "PENDENTE")
        for previous, current in zip(events, events[1:]):
            self.assertEqual(previous.new_status, current.previous_status)
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.status, events[-1].new_status)
        self.assertEqual(len(events), codes.count(200))

    def test_concurrent_reassignment_rechecks_ownership_after_lock(self):
        token, started = str(AccessToken.for_user(self.driver)), Event()
        with ThreadPoolExecutor(max_workers=1) as executor:
            with transaction.atomic():
                locked = Delivery.objects.select_for_update().get(pk=self.delivery.pk)
                locked.assigned_driver = self.other
                locked.save(update_fields=["assigned_driver"])
                future = executor.submit(self.request_in_thread, token, "EM_TRANSPORTE", started)
                self.assertTrue(started.wait(timeout=10))
                with self.assertRaises(TimeoutError):
                    future.result(timeout=0.25)
            self.assertEqual(future.result(timeout=10), 404)
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.status, "PENDENTE")
        self.assertFalse(self.delivery.status_history.exists())

    def test_status_and_history_survive_closed_database_connection(self):
        client = self.token_client(self.driver)
        self.assertEqual(client.post(self.url, {"status": "EM_TRANSPORTE"}).status_code, 200)
        connection.close()
        fresh = Delivery.objects.get(pk=self.delivery.pk)
        self.assertEqual(fresh.status, "EM_TRANSPORTE")
        self.assertEqual(fresh.status_history.get().new_status, fresh.status)
        manager = self.token_client(self.manager)
        self.assertEqual(manager.get(f"/api/deliveries/{fresh.pk}/").data["status"], fresh.status)
