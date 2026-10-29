import base64
import json
from datetime import timedelta

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import UserProfile
from deliveries.models import Delivery

PASSWORD = "SenhaSegura123!"


class FenemeAuthTestMixin:
    login_url = "/api/auth/login/"
    refresh_url = "/api/auth/refresh/"
    deliveries_url = "/api/deliveries/"
    drivers_url = "/api/drivers/"

    def create_user(self, username, role, **extra):
        user = User.objects.create_user(username=username, password=PASSWORD, **extra)
        user.profile.role = role
        user.profile.save()
        return user

    def setUp(self):
        self.manager = self.create_user("gestor_teste", UserProfile.Role.GESTOR)
        self.driver = self.create_user("motorista_teste", UserProfile.Role.MOTORISTA)
        self.other_driver = self.create_user("motorista_teste_2", UserProfile.Role.MOTORISTA)
        self.delivery = Delivery.objects.create(
            origin="Campina Grande - PB",
            destination="João Pessoa - PB",
            cargo_description="Alimentos refrigerados",
            assigned_driver=self.driver,
            created_by=self.manager,
        )

    def request_login(self, username, password=PASSWORD):
        return self.client.post(self.login_url, {"username": username, "password": password}, format="json")

    def login_as(self, username, password=PASSWORD):
        response = self.request_login(username, password)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        return response.data

    def assert_no_sensitive_data(self, response, user=None, password=None):
        body = response.content.decode()
        self.assertNotIn("Traceback", body)
        if password:
            self.assertNotIn(password, body)
        if user:
            self.assertNotIn(user.password, body)


class MotoristaLoginTests(FenemeAuthTestMixin, APITestCase):
    def test_motorista_valid_login_returns_tokens_and_role(self):
        """CT-13: Motorista com credenciais válidas é autenticado e reconhecido como MOTORISTA."""
        response = self.request_login("motorista_teste")

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"], {
            "id": self.driver.id,
            "username": "motorista_teste",
            "role": "MOTORISTA",
        })
        self.assertEqual(AccessToken(response.data["access"])["role"], "MOTORISTA")

    def test_motorista_uses_same_login_endpoint_as_gestor(self):
        """CT-13 / regra 1: o login é compartilhado; o mesmo endpoint autentica os dois perfis."""
        for username, role in [("gestor_teste", "GESTOR"), ("motorista_teste", "MOTORISTA")]:
            with self.subTest(username=username):
                response = self.request_login(username)
                self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
                self.assertEqual(response.data["user"]["role"], role)

    def test_invalid_credentials_are_rejected_without_tokens(self):
        """CT-14: credenciais inválidas não geram token e usam a mesma mensagem genérica."""
        self.create_user("motorista_inativo", UserProfile.Role.MOTORISTA, is_active=False)
        self.create_user("gestor_inativo", UserProfile.Role.GESTOR, is_active=False)
        reference = self.request_login("usuario_inexistente")
        cases = [
            ("motorista_teste", "SenhaErrada123!"),
            ("gestor_teste", "SenhaErrada123!"),
            ("usuario_inexistente", PASSWORD),
            ("motorista_inativo", PASSWORD),
            ("gestor_inativo", PASSWORD),
        ]
        for username, password in cases:
            with self.subTest(username=username, password=password):
                response = self.request_login(username, password)
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                self.assertNotIn("access", response.data)
                self.assertNotIn("refresh", response.data)
                self.assertEqual(response.data, reference.data)
                user = User.objects.filter(username=username).first()
                self.assert_no_sensitive_data(response, user=user, password=password)


class MotoristaPermissionTests(FenemeAuthTestMixin, APITestCase):
    def assert_motorista_is_forbidden(self, method, url, payload=None):
        response = getattr(self.client, method)(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        self.assert_no_sensitive_data(response, user=self.driver, password=PASSWORD)

    def test_motorista_cannot_access_gestor_only_endpoints(self):
        """Regra 2: Motorista autenticado recebe 403 nas operações exclusivas do Gestor."""
        self.login_as("motorista_teste")
        detail_url = f"{self.deliveries_url}{self.delivery.id}/"
        cases = [
            ("post", self.deliveries_url, {
                "origin": "Campina Grande - PB",
                "destination": "Patos - PB",
                "cargo_description": "Carga indevida",
            }),
            ("post", f"{detail_url}assign-driver/", {"driver_id": self.other_driver.id}),
            ("get", self.drivers_url, None),
        ]
        for method, url, payload in cases:
            with self.subTest(method=method, url=url):
                self.assert_motorista_is_forbidden(method, url, payload)

        own_detail = self.client.get(detail_url)
        self.assertEqual(own_detail.status_code, status.HTTP_200_OK)
        own_list = self.client.get(self.deliveries_url)
        self.assertEqual(own_list.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in own_list.data], [self.delivery.id])

        self.assertEqual(Delivery.objects.count(), 1)
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.assigned_driver, self.driver)

    def test_other_motorista_cannot_access_or_take_delivery(self):
        """Acesso cruzado (FT-29): outro Motorista não lê nem reatribui a entrega de um colega."""
        self.login_as("motorista_teste_2")
        detail_url = f"{self.deliveries_url}{self.delivery.id}/"
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assert_no_sensitive_data(response, user=self.other_driver, password=PASSWORD)
        listing = self.client.get(self.deliveries_url)
        self.assertEqual(listing.status_code, status.HTTP_200_OK)
        self.assertEqual(listing.data, [])

        response = self.client.post(
            f"{detail_url}assign-driver/", {"driver_id": self.other_driver.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_no_sensitive_data(response, user=self.other_driver, password=PASSWORD)

        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.assigned_driver, self.driver)


class InvalidSessionTests(FenemeAuthTestMixin, APITestCase):
    def assert_unauthorized(self, response):
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)
        self.assert_no_sensitive_data(response)

    def get_with_token(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return self.client.get(self.deliveries_url)

    def test_missing_or_malformed_token_is_rejected(self):
        """FT-30: requisição sem token ou com token malformado não é autenticada."""
        with self.subTest(case="sem header"):
            self.assert_unauthorized(self.client.get(self.deliveries_url))
        with self.subTest(case="token malformado"):
            self.assert_unauthorized(self.get_with_token("abc"))

    def test_expired_access_token_is_rejected(self):
        """FT-30: access token expirado é recusado para os dois perfis."""
        for user in [self.driver, self.manager]:
            with self.subTest(username=user.username):
                token = AccessToken.for_user(user)
                token.set_exp(lifetime=-timedelta(seconds=1))
                self.assert_unauthorized(self.get_with_token(str(token)))

    def test_refresh_token_cannot_be_used_as_access_token(self):
        """FT-30: o refresh token não serve como credencial de acesso para nenhum perfil."""
        for username in ["motorista_teste", "gestor_teste"]:
            with self.subTest(username=username):
                refresh = self.request_login(username).data["refresh"]
                self.assert_unauthorized(self.get_with_token(refresh))

    def test_tampered_role_claim_is_rejected(self):
        """FT-30: alterar a claim role do token do Motorista para GESTOR invalida a assinatura."""
        header, payload, signature = self.request_login("motorista_teste").data["access"].split(".")
        claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        claims["role"] = "GESTOR"
        forged_payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b"=").decode()

        self.assert_unauthorized(self.get_with_token(f"{header}.{forged_payload}.{signature}"))

    def test_access_token_cannot_be_used_to_refresh(self):
        """FT-30: o endpoint de refresh recusa um access token."""
        access = self.request_login("motorista_teste").data["access"]
        response = self.client.post(self.refresh_url, {"refresh": access}, format="json")

        self.assert_unauthorized(response)
        self.assertNotIn("access", response.data)
