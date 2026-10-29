"""FT-78 / Q-10: 20 cenários negativos de autenticação e sessão.

Arquivo: backend/accounts/test_autentificacao.py.
Executar: python manage.py test accounts.test_autentificacao -v 2

Atenção: os resultados somente podem ser registrados no Jira após execução real.
"""
import base64
import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import UserProfile
from deliveries.models import Delivery


User = get_user_model()
TEST_PASSWORD = "SenhaFicticiaDeTeste123!"


class Q10InvalidAccessTests(APITestCase):
    """20 métodos independentes = 20 casos negativos mensuráveis."""

    def setUp(self):
        self.gestor = self.make_user("gestor_q10", "GESTOR")
        self.motorista = self.make_user("motorista_q10", "MOTORISTA")
        self.gestor_inativo = self.make_user("gestor_inativo_q10", "GESTOR", is_active=False)
        self.motorista_inativo = self.make_user("motorista_inativo_q10", "MOTORISTA", is_active=False)
        self.entrega = Delivery.objects.create(
            origin="Campina Grande - PB",
            destination="João Pessoa - PB",
            cargo_description="Carga fictícia para testes",
            created_by=self.gestor,
            assigned_driver=self.motorista,
        )

    def make_user(self, username, role, **kwargs):
        user = User.objects.create_user(username=username, password=TEST_PASSWORD, **kwargs)
        user.profile.role = getattr(UserProfile.Role, role)
        user.profile.save()
        return user

    @property
    def detail_url(self):
        return f"/api/deliveries/{self.entrega.id}/"

    def login(self, username, password=TEST_PASSWORD):
        return self.client.post(
            "/api/auth/login/",
            {"username": username, "password": password},
            format="json",
        )

    def assert_login_rejected(self, username, password, http_status):
        response = self.login(username, password)
        self.assertEqual(response.status_code, http_status, response.data)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def assert_api_rejected(self, method, endpoint, http_status=status.HTTP_401_UNAUTHORIZED, token=None, payload=None):
        self.client.credentials(**({"HTTP_AUTHORIZATION": f"Bearer {token}"} if token is not None else {}))
        response = getattr(self.client, method)(endpoint, payload, format="json") if method == "post" else getattr(self.client, method)(endpoint)
        self.assertEqual(response.status_code, http_status, response.data)
        return response

    # Grupo A — Oito casos de credenciais inválidas.
    def test_q10_01_senha_errada_gestor(self):
        self.assert_login_rejected("gestor_q10", "senha-errada", 401)

    def test_q10_02_senha_errada_motorista(self):
        self.assert_login_rejected("motorista_q10", "senha-errada", 401)

    def test_q10_03_usuario_inexistente(self):
        self.assert_login_rejected("nao_existe_q10", TEST_PASSWORD, 401)

    def test_q10_04_gestor_inativo(self):
        self.assert_login_rejected("gestor_inativo_q10", TEST_PASSWORD, 401)

    def test_q10_05_motorista_inativo(self):
        self.assert_login_rejected("motorista_inativo_q10", TEST_PASSWORD, 401)

    def test_q10_06_usuario_vazio(self):
        self.assert_login_rejected("", TEST_PASSWORD, 400)

    def test_q10_07_senha_vazia(self):
        self.assert_login_rejected("gestor_q10", "", 400)

    def test_q10_08_ambos_vazios(self):
        self.assert_login_rejected("", "", 400)

    # Grupo B — Doze casos de sessão ausente, expirada ou inválida.
    def test_q10_09_sem_token_lista_entregas(self):
        self.assert_api_rejected("get", "/api/deliveries/")

    def test_q10_10_sem_token_criar_entrega(self):
        payload = {"origin": "A", "destination": "B", "cargo_description": "Teste"}
        self.assert_api_rejected("post", "/api/deliveries/", payload=payload)
        self.assertEqual(Delivery.objects.count(), 1)

    def test_q10_11_sem_token_lista_motoristas(self):
        self.assert_api_rejected("get", "/api/drivers/")

    def test_q10_12_sem_token_detalhe_entrega(self):
        self.assert_api_rejected("get", self.detail_url)

    def test_q10_13_token_malformado_lista_entregas(self):
        self.assert_api_rejected("get", "/api/deliveries/", token="token-invalido")

    def test_q10_14_token_malformado_lista_motoristas(self):
        self.assert_api_rejected("get", "/api/drivers/", token="token-invalido")

    def test_q10_15_token_malformado_detalhe_entrega(self):
        self.assert_api_rejected("get", self.detail_url, token="token-invalido")

    def test_q10_16_token_expirado_gestor(self):
        token = AccessToken.for_user(self.gestor)
        token.set_exp(lifetime=-timedelta(seconds=1))
        self.assert_api_rejected("get", "/api/deliveries/", token=str(token))

    def test_q10_17_token_expirado_motorista(self):
        token = AccessToken.for_user(self.motorista)
        token.set_exp(lifetime=-timedelta(seconds=1))
        self.assert_api_rejected("get", self.detail_url, token=str(token))

    def test_q10_18_token_adulterado_papel_motorista(self):
        valid = self.login("motorista_q10")
        self.assertEqual(valid.status_code, 200)
        header, payload, signature = valid.data["access"].split(".")
        claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        claims["role"] = "GESTOR"
        tampered_payload = base64.urlsafe_b64encode(
            json.dumps(claims).encode("utf-8")
        ).rstrip(b"=").decode("ascii")
        self.assert_api_rejected(
            "get", "/api/deliveries/",
            token=f"{header}.{tampered_payload}.{signature}",
        )

    def test_q10_19_refresh_usado_para_acessar_api(self):
        valid = self.login("gestor_q10")
        self.assertEqual(valid.status_code, 200)
        self.assert_api_rejected("get", "/api/deliveries/", token=valid.data["refresh"])

    def test_q10_20_access_usado_para_renovar_sessao(self):
        valid = self.login("gestor_q10")
        self.assertEqual(valid.status_code, 200)
        self.client.credentials()  # evita interferência de cabeçalho de autenticação
        response = self.client.post(
            "/api/auth/refresh/", {"refresh": valid.data["access"]}, format="json"
        )
        self.assertEqual(response.status_code, 401, response.data)
        self.assertNotIn("access", response.data)
