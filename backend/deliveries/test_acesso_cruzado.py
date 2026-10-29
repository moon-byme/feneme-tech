"""FT-29 (DA-SEG-LZ-01) / FT-73 (Q-05) — verificação de acesso cruzado.

Arquivo: backend/deliveries/test_acesso_cruzado.py
Executar na raiz: python backend/manage.py test deliveries.test_acesso_cruzado -v 2

20 métodos test_ft29_*: vinte tentativas CONTRA entregas pertencentes a
outro Motorista. Quatro controles extras não entram no denominador.
A alteração de status da FT-48 ainda não existe na versão inspecionada;
precisará de regressão específica quando a US estiver implementada.

As requisições usam JWT e os dados ficam isolados no banco de testes.
Registrar resultados no Jira somente com a evidência da execução correspondente.
"""
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import UserProfile
from deliveries.models import Delivery

User = get_user_model()


class DriverCrossAccessFT29Tests(APITestCase):
    url = "/api/deliveries/"

    @classmethod
    def setUpTestData(cls):
        cls.gestor = cls.make_user("qa_ft29_gestor", UserProfile.Role.GESTOR)
        cls.a = cls.make_user("qa_ft29_a", UserProfile.Role.MOTORISTA)
        cls.b = cls.make_user("qa_ft29_b", UserProfile.Role.MOTORISTA)
        cls.a1 = cls.make_delivery("A1", cls.a)
        cls.a2 = cls.make_delivery("A2", cls.a)
        cls.b1 = cls.make_delivery("B1", cls.b)
        cls.b2 = cls.make_delivery("B2", cls.b)
        cls.sem_atribuicao = cls.make_delivery("Livre", None)

    @classmethod
    def make_user(cls, username, role):
        user = User.objects.create_user(username=username, password="SenhaFicticiaFT29_123!")
        user.profile.role = role
        user.profile.save(update_fields=["role"])
        return user

    @classmethod
    def make_delivery(cls, label, driver):
        return Delivery.objects.create(
            origin=f"Origem {label}", destination=f"Destino {label}",
            cargo_description=f"Carga fictícia {label}",
            created_by=cls.gestor, assigned_driver=driver,
        )

    def snapshot(self):
        # Os campos persistidos, inclusive data de atualização, devem ficar intactos.
        return list(Delivery.objects.order_by("pk").values())

    def authenticate(self, user):
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def attempt(self, actor, foreign_delivery, operation):
        self.authenticate(actor)
        before = self.snapshot()
        endpoint = f"{self.url}{foreign_delivery.id}/"
        if operation == "get":
            resp = self.client.get(endpoint)
            expected = status.HTTP_404_NOT_FOUND
        elif operation == "head":
            resp = self.client.head(endpoint)
            expected = status.HTTP_404_NOT_FOUND
        elif operation == "get_spoof":
            resp = self.client.get(endpoint, {"assigned_driver": actor.id, "role": "GESTOR"})
            expected = status.HTTP_404_NOT_FOUND
        elif operation == "assign_self":
            resp = self.client.post(endpoint + "assign-driver/", {"driver_id": actor.id}, format="json")
            expected = status.HTTP_403_FORBIDDEN
        elif operation == "assign_other":
            other_id = self.b.id if actor.pk == self.a.pk else self.a.id
            resp = self.client.post(endpoint + "assign-driver/", {"driver_id": other_id}, format="json")
            expected = status.HTTP_403_FORBIDDEN
        else:
            raise ValueError(operation)

        self.assertEqual(resp.status_code, expected, resp.data if hasattr(resp, "data") else resp.content)
        self.assertEqual(before, self.snapshot(), "A tentativa indevida persistiu alterações!")
        for value in (foreign_delivery.origin, foreign_delivery.destination,
                      foreign_delivery.cargo_description):
            self.assertNotIn(value, resp.content.decode("utf-8"))

    def test_ft29_01_a_get_b1(self):
        """Tentativa 01/20: a contra entrega de outro Motorista (b1)."""
        self.attempt(self.a, self.b1, "get")

    def test_ft29_02_a_head_b1(self):
        """Tentativa 02/20: a contra entrega de outro Motorista (b1)."""
        self.attempt(self.a, self.b1, "head")

    def test_ft29_03_a_get_spoof_b1(self):
        """Tentativa 03/20: a contra entrega de outro Motorista (b1)."""
        self.attempt(self.a, self.b1, "get_spoof")

    def test_ft29_04_a_assign_self_b1(self):
        """Tentativa 04/20: a contra entrega de outro Motorista (b1)."""
        self.attempt(self.a, self.b1, "assign_self")

    def test_ft29_05_a_assign_other_b1(self):
        """Tentativa 05/20: a contra entrega de outro Motorista (b1)."""
        self.attempt(self.a, self.b1, "assign_other")

    def test_ft29_06_a_get_b2(self):
        """Tentativa 06/20: a contra entrega de outro Motorista (b2)."""
        self.attempt(self.a, self.b2, "get")

    def test_ft29_07_a_head_b2(self):
        """Tentativa 07/20: a contra entrega de outro Motorista (b2)."""
        self.attempt(self.a, self.b2, "head")

    def test_ft29_08_a_get_spoof_b2(self):
        """Tentativa 08/20: a contra entrega de outro Motorista (b2)."""
        self.attempt(self.a, self.b2, "get_spoof")

    def test_ft29_09_a_assign_self_b2(self):
        """Tentativa 09/20: a contra entrega de outro Motorista (b2)."""
        self.attempt(self.a, self.b2, "assign_self")

    def test_ft29_10_a_assign_other_b2(self):
        """Tentativa 10/20: a contra entrega de outro Motorista (b2)."""
        self.attempt(self.a, self.b2, "assign_other")

    def test_ft29_11_b_get_a1(self):
        """Tentativa 11/20: b contra entrega de outro Motorista (a1)."""
        self.attempt(self.b, self.a1, "get")

    def test_ft29_12_b_head_a1(self):
        """Tentativa 12/20: b contra entrega de outro Motorista (a1)."""
        self.attempt(self.b, self.a1, "head")

    def test_ft29_13_b_get_spoof_a1(self):
        """Tentativa 13/20: b contra entrega de outro Motorista (a1)."""
        self.attempt(self.b, self.a1, "get_spoof")

    def test_ft29_14_b_assign_self_a1(self):
        """Tentativa 14/20: b contra entrega de outro Motorista (a1)."""
        self.attempt(self.b, self.a1, "assign_self")

    def test_ft29_15_b_assign_other_a1(self):
        """Tentativa 15/20: b contra entrega de outro Motorista (a1)."""
        self.attempt(self.b, self.a1, "assign_other")

    def test_ft29_16_b_get_a2(self):
        """Tentativa 16/20: b contra entrega de outro Motorista (a2)."""
        self.attempt(self.b, self.a2, "get")

    def test_ft29_17_b_head_a2(self):
        """Tentativa 17/20: b contra entrega de outro Motorista (a2)."""
        self.attempt(self.b, self.a2, "head")

    def test_ft29_18_b_get_spoof_a2(self):
        """Tentativa 18/20: b contra entrega de outro Motorista (a2)."""
        self.attempt(self.b, self.a2, "get_spoof")

    def test_ft29_19_b_assign_self_a2(self):
        """Tentativa 19/20: b contra entrega de outro Motorista (a2)."""
        self.attempt(self.b, self.a2, "assign_self")

    def test_ft29_20_b_assign_other_a2(self):
        """Tentativa 20/20: b contra entrega de outro Motorista (a2)."""
        self.attempt(self.b, self.a2, "assign_other")

    def test_controle_01_motoristas_veem_somente_entregas_proprias(self):
        for user, own_ids in [(self.a, {self.a1.id, self.a2.id}),
                              (self.b, {self.b1.id, self.b2.id})]:
            with self.subTest(motorista=user.username):
                self.authenticate(user)
                response = self.client.get(self.url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual({item["id"] for item in response.data}, own_ids)
                # O detalhe deve funcionar para o dono, além de negar acesso cruzado.
                for delivery_id in own_ids:
                    detail = self.client.get(f"{self.url}{delivery_id}/")
                    self.assertEqual(detail.status_code, 200)
                    self.assertEqual(detail.data["id"], delivery_id)
                    self.assertEqual(detail.data["assigned_driver"], user.id)

    def test_controle_02_entrega_nao_atribuida_fica_oculta(self):
        for user in [self.a, self.b]:
            with self.subTest(motorista=user.username):
                self.authenticate(user)
                response = self.client.get(f"{self.url}{self.sem_atribuicao.id}/")
                self.assertEqual(response.status_code, 404)

    def test_controle_03_motorista_nao_pode_cadastrar_entrega(self):
        self.authenticate(self.a)
        before = self.snapshot()
        response = self.client.post(self.url, {
            "origin": "X", "destination": "Y", "cargo_description": "Z",
        }, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(before, self.snapshot())

    def test_controle_04_gestor_pode_atribuir_entrega(self):
        self.authenticate(self.gestor)
        response = self.client.post(
            f"{self.url}{self.sem_atribuicao.id}/assign-driver/",
            {"driver_id": self.a.id}, format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.sem_atribuicao.refresh_from_db()
        self.assertEqual(self.sem_atribuicao.assigned_driver_id, self.a.id)
