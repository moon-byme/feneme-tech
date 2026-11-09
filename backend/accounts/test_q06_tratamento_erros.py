"""FT-33 / FT-74 — Q-06: tratamento seguro de erros e logs.

Métrica: zero exposições de credenciais, dados privados ou traceback em
20 cenários negativos. Os dados utilizados são exclusivamente fictícios.

Executar em backend:
    python manage.py test accounts.test_q06_tratamento_erros -v 2
"""
import io
import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import UserProfile
from deliveries.models import Delivery

User = get_user_model()
PASSWORD = "SenhaFicticia_Q06_123!"
SENSITIVE_MARKER = "DADO_PRIVADO_Q06_NAO_EXIBIR"


class Q06SafeErrorHandlingTests(APITestCase):
    """Vinte falhas independentes; cada teste verifica corpo HTTP e logs."""

    def setUp(self):
        self.gestor = self.make_user("gestor_q06", UserProfile.Role.GESTOR)
        self.motorista = self.make_user("motorista_q06", UserProfile.Role.MOTORISTA)
        self.entrega = Delivery.objects.create(
            origin="Origem fictícia Q06",
            destination="Destino fictício Q06",
            cargo_description="Carga fictícia Q06",
            created_by=self.gestor,
            assigned_driver=self.motorista,
        )

    def make_user(self, username, role, **kwargs):
        user = User.objects.create_user(username=username, password=PASSWORD, **kwargs)
        user.profile.role = role
        user.profile.save(update_fields=["role"])
        return user

    def request_and_assert_safe(self, method, path, expected, *, payload=None,
                                token=None, sensitive_values=()):
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        root_logger = logging.getLogger()
        django_logger = logging.getLogger("django")
        root_logger.addHandler(handler)
        django_logger.addHandler(handler)
        try:
            if token:
                self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            else:
                self.client.credentials()
            response = getattr(self.client, method)(
                path, payload, format="json"
            ) if method == "post" else getattr(self.client, method)(path)
        finally:
            root_logger.removeHandler(handler)
            django_logger.removeHandler(handler)
            handler.close()

        body = response.content.decode("utf-8", errors="replace")
        logs = stream.getvalue()
        self.assertEqual(response.status_code, expected, body)
        self.assertNotIn("Traceback", body)
        self.assertNotIn("Traceback", logs)
        self.assertNotIn(PASSWORD, body)
        self.assertNotIn(PASSWORD, logs)
        for value in sensitive_values:
            self.assertNotIn(value, body)
            self.assertNotIn(value, logs)
        return response

    # 01–05: credenciais inválidas.
    def test_q06_01_senha_incorreta_gestor(self):
        self.request_and_assert_safe("post", "/api/auth/login/", 401,
            payload={"username": "gestor_q06", "password": SENSITIVE_MARKER},
            sensitive_values=(SENSITIVE_MARKER,))

    def test_q06_02_senha_incorreta_motorista(self):
        self.request_and_assert_safe("post", "/api/auth/login/", 401,
            payload={"username": "motorista_q06", "password": SENSITIVE_MARKER},
            sensitive_values=(SENSITIVE_MARKER,))

    def test_q06_03_usuario_inexistente(self):
        self.request_and_assert_safe("post", "/api/auth/login/", 401,
            payload={"username": SENSITIVE_MARKER, "password": PASSWORD},
            sensitive_values=(SENSITIVE_MARKER,))

    def test_q06_04_usuario_inativo(self):
        inactive = self.make_user("inativo_q06", UserProfile.Role.GESTOR, is_active=False)
        self.request_and_assert_safe("post", "/api/auth/login/", 401,
            payload={"username": inactive.username, "password": PASSWORD},
            sensitive_values=(inactive.username,))

    def test_q06_05_credenciais_vazias(self):
        self.request_and_assert_safe("post", "/api/auth/login/", 400,
            payload={"username": "", "password": ""})

    # 06–10: ausência ou invalidade de autenticação.
    def test_q06_06_sem_token_lista_entregas(self):
        self.request_and_assert_safe("get", "/api/deliveries/", 401)

    def test_q06_07_sem_token_detalhe_entrega(self):
        self.request_and_assert_safe("get", f"/api/deliveries/{self.entrega.id}/", 401)

    def test_q06_08_sem_token_lista_motoristas(self):
        self.request_and_assert_safe("get", "/api/drivers/", 401)

    def test_q06_09_token_malformado(self):
        self.request_and_assert_safe("get", "/api/deliveries/", 401, token=SENSITIVE_MARKER,
            sensitive_values=(SENSITIVE_MARKER,))

    def test_q06_10_token_expirado(self):
        token = AccessToken.for_user(self.gestor)
        token.set_exp(lifetime=timedelta(seconds=-1))
        self.request_and_assert_safe("get", "/api/deliveries/", 401, token=str(token))

    # 11–15: operações proibidas ao Motorista.
    def test_q06_11_motorista_tenta_cadastrar_entrega(self):
        self.request_and_assert_safe("post", "/api/deliveries/", 403,
            token=str(AccessToken.for_user(self.motorista)),
            payload={"origin": SENSITIVE_MARKER, "destination": "B",
                     "cargo_description": "Carga"},
            sensitive_values=(SENSITIVE_MARKER,))

    def test_q06_12_motorista_tenta_listar_motoristas(self):
        self.request_and_assert_safe("get", "/api/drivers/", 403,
            token=str(AccessToken.for_user(self.motorista)))

    def test_q06_13_motorista_tenta_reatribuir_entrega(self):
        self.request_and_assert_safe("post",
            f"/api/deliveries/{self.entrega.id}/assign-driver/", 403,
            token=str(AccessToken.for_user(self.motorista)),
            payload={"driver_id": self.motorista.id})

    def test_q06_14_motorista_tenta_alterar_entrega_por_patch(self):
        self.request_and_assert_safe("patch",
            f"/api/deliveries/{self.entrega.id}/", 405,
            token=str(AccessToken.for_user(self.motorista)))

    def test_q06_15_motorista_tenta_excluir_entrega(self):
        self.request_and_assert_safe("delete",
            f"/api/deliveries/{self.entrega.id}/", 405,
            token=str(AccessToken.for_user(self.motorista)))

    # 16–20: entradas inválidas no cadastro e na atribuição.
    def test_q06_16_origem_obrigatoria_ausente(self):
        self.request_and_assert_safe("post", "/api/deliveries/", 400,
            token=str(AccessToken.for_user(self.gestor)),
            payload={"destination": "B", "cargo_description": "Carga"})

    def test_q06_17_destino_obrigatorio_ausente(self):
        self.request_and_assert_safe("post", "/api/deliveries/", 400,
            token=str(AccessToken.for_user(self.gestor)),
            payload={"origin": "A", "cargo_description": "Carga"})

    def test_q06_18_descricao_de_carga_obrigatoria_ausente(self):
        self.request_and_assert_safe("post", "/api/deliveries/", 400,
            token=str(AccessToken.for_user(self.gestor)),
            payload={"origin": "A", "destination": "B"})

    def test_q06_19_motorista_inexistente_na_atribuicao(self):
        self.request_and_assert_safe("post",
            f"/api/deliveries/{self.entrega.id}/assign-driver/", 400,
            token=str(AccessToken.for_user(self.gestor)),
            payload={"driver_id": 999999})

    def test_q06_20_gestor_nao_pode_ser_atribuido_como_motorista(self):
        self.request_and_assert_safe("post",
            f"/api/deliveries/{self.entrega.id}/assign-driver/", 400,
            token=str(AccessToken.for_user(self.gestor)),
            payload={"driver_id": self.gestor.id})
