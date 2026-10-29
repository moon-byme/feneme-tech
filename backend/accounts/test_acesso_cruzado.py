"""FT-73 / Q-05: isolamento das entregas entre Motoristas na API.

Executar em backend: python manage.py test accounts.test_acesso_cruzado -v 2
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import UserProfile
from deliveries.models import Delivery

User = get_user_model()


class Q05AcessoCruzadoTests(APITestCase):
    """Requisições com JWT; dados isolados no banco de testes do APITestCase."""

    @classmethod
    def setUpTestData(cls):
        cls.gestor = cls._criar_usuario("qa_gestor_q05", UserProfile.Role.GESTOR)
        cls.motorista_a = cls._criar_usuario("qa_motorista_a_q05", UserProfile.Role.MOTORISTA)
        cls.motorista_b = cls._criar_usuario("qa_motorista_b_q05", UserProfile.Role.MOTORISTA)
        cls.a1 = cls._criar_entrega("A1", cls.motorista_a)
        cls.a2 = cls._criar_entrega("A2", cls.motorista_a)
        cls.b1 = cls._criar_entrega("B1", cls.motorista_b)
        cls.b2 = cls._criar_entrega("B2", cls.motorista_b)
        cls.livre1 = cls._criar_entrega("Livre1", None)
        cls.livre2 = cls._criar_entrega("Livre2", None)

    @classmethod
    def _criar_usuario(cls, username, papel):
        user = User.objects.create_user(username=username, password="SenhaFicticiaQ05_123!")
        user.profile.role = papel
        user.profile.save(update_fields=["role"])
        return user

    @classmethod
    def _criar_entrega(cls, rotulo, motorista):
        return Delivery.objects.create(
            origin=f"Origem {rotulo}",
            destination=f"Destino {rotulo}",
            cargo_description=f"Carga ficticia {rotulo}",
            created_by=cls.gestor,
            assigned_driver=motorista,
        )

    @staticmethod
    def _fotografia_banco():
        """Compara todos os campos, inclusive atribuição, status e timestamps."""
        return list(Delivery.objects.order_by("id").values())

    def _autenticar(self, usuario):
        token = AccessToken.for_user(usuario)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def _tentar_acesso(self, ator, entrega, metodo):
        self._autenticar(ator)
        antes = self._fotografia_banco()
        detalhe = f"/api/deliveries/{entrega.id}/"

        if metodo == "get":
            resposta = self.client.get(detalhe)
            esperado = status.HTTP_404_NOT_FOUND
            # A API não deve expor o conteúdo protegido nem no corpo do erro.
            for valor in (entrega.origin, entrega.destination, entrega.cargo_description):
                self.assertNotIn(valor, resposta.content.decode("utf-8"))
        elif metodo == "head":
            resposta = self.client.head(detalhe)
            esperado = status.HTTP_404_NOT_FOUND
        elif metodo == "assign":
            resposta = self.client.post(
                detalhe + "assign-driver/",
                {"driver_id": ator.id},
                format="json",
            )
            esperado = status.HTTP_403_FORBIDDEN
        elif metodo in ("put", "patch", "delete"):
            resposta = getattr(self.client, metodo)(detalhe, {
                "origin": "Origem indevida",
                "destination": "Destino indevido",
                "cargo_description": "Carga alterada indevidamente",
                "assigned_driver": ator.id,
            }, format="json")
            esperado = status.HTTP_403_FORBIDDEN
        else:
            raise AssertionError(f"Método de teste inesperado: {metodo}")

        self.assertEqual(resposta.status_code, esperado, resposta.content.decode("utf-8"))
        self.assertEqual(antes, self._fotografia_banco(),
                         "Uma tentativa indevida alterou os registros de entregas.")

    def test_q05_01_a_get_b1(self):
        """Tentativa 01/20: motorista_a usa GET na entrega b1."""
        self._tentar_acesso(self.motorista_a, self.b1, "get")

    def test_q05_02_a_assign_b1(self):
        """Tentativa 02/20: motorista_a usa ASSIGN na entrega b1."""
        self._tentar_acesso(self.motorista_a, self.b1, "assign")

    def test_q05_03_a_get_b2(self):
        """Tentativa 03/20: motorista_a usa GET na entrega b2."""
        self._tentar_acesso(self.motorista_a, self.b2, "get")

    def test_q05_04_a_assign_b2(self):
        """Tentativa 04/20: motorista_a usa ASSIGN na entrega b2."""
        self._tentar_acesso(self.motorista_a, self.b2, "assign")

    def test_q05_05_a_get_livre1(self):
        """Tentativa 05/20: motorista_a usa GET na entrega livre1."""
        self._tentar_acesso(self.motorista_a, self.livre1, "get")

    def test_q05_06_a_assign_livre1(self):
        """Tentativa 06/20: motorista_a usa ASSIGN na entrega livre1."""
        self._tentar_acesso(self.motorista_a, self.livre1, "assign")

    def test_q05_07_a_get_livre2(self):
        """Tentativa 07/20: motorista_a usa GET na entrega livre2."""
        self._tentar_acesso(self.motorista_a, self.livre2, "get")

    def test_q05_08_a_assign_livre2(self):
        """Tentativa 08/20: motorista_a usa ASSIGN na entrega livre2."""
        self._tentar_acesso(self.motorista_a, self.livre2, "assign")

    def test_q05_09_a_head_b1(self):
        """Tentativa 09/20: motorista_a usa HEAD na entrega b1."""
        self._tentar_acesso(self.motorista_a, self.b1, "head")

    def test_q05_10_a_head_b2(self):
        """Tentativa 10/20: motorista_a usa HEAD na entrega b2."""
        self._tentar_acesso(self.motorista_a, self.b2, "head")

    def test_q05_11_b_get_a1(self):
        """Tentativa 11/20: motorista_b usa GET na entrega a1."""
        self._tentar_acesso(self.motorista_b, self.a1, "get")

    def test_q05_12_b_assign_a1(self):
        """Tentativa 12/20: motorista_b usa ASSIGN na entrega a1."""
        self._tentar_acesso(self.motorista_b, self.a1, "assign")

    def test_q05_13_b_get_a2(self):
        """Tentativa 13/20: motorista_b usa GET na entrega a2."""
        self._tentar_acesso(self.motorista_b, self.a2, "get")

    def test_q05_14_b_assign_a2(self):
        """Tentativa 14/20: motorista_b usa ASSIGN na entrega a2."""
        self._tentar_acesso(self.motorista_b, self.a2, "assign")

    def test_q05_15_b_get_livre1(self):
        """Tentativa 15/20: motorista_b usa GET na entrega livre1."""
        self._tentar_acesso(self.motorista_b, self.livre1, "get")

    def test_q05_16_b_assign_livre1(self):
        """Tentativa 16/20: motorista_b usa ASSIGN na entrega livre1."""
        self._tentar_acesso(self.motorista_b, self.livre1, "assign")

    def test_q05_17_b_get_livre2(self):
        """Tentativa 17/20: motorista_b usa GET na entrega livre2."""
        self._tentar_acesso(self.motorista_b, self.livre2, "get")

    def test_q05_18_b_assign_livre2(self):
        """Tentativa 18/20: motorista_b usa ASSIGN na entrega livre2."""
        self._tentar_acesso(self.motorista_b, self.livre2, "assign")

    def test_q05_19_b_head_a1(self):
        """Tentativa 19/20: motorista_b usa HEAD na entrega a1."""
        self._tentar_acesso(self.motorista_b, self.a1, "head")

    def test_q05_20_b_head_a2(self):
        """Tentativa 20/20: motorista_b usa HEAD na entrega a2."""
        self._tentar_acesso(self.motorista_b, self.a2, "head")

    def _tentar_modificar_entregas_alheias(self, metodo):
        for ator, entregas in [
            (self.motorista_a, [self.b1, self.b2, self.livre1, self.livre2]),
            (self.motorista_b, [self.a1, self.a2, self.livre1, self.livre2]),
        ]:
            for entrega in entregas:
                with self.subTest(motorista=ator.username, entrega=entrega.id, metodo=metodo):
                    self._tentar_acesso(ator, entrega, metodo)

    def test_motoristas_nao_podem_substituir_entregas_alheias(self):
        self._tentar_modificar_entregas_alheias("put")

    def test_motoristas_nao_podem_alterar_entregas_alheias(self):
        self._tentar_modificar_entregas_alheias("patch")

    def test_motoristas_nao_podem_excluir_entregas_alheias(self):
        self._tentar_modificar_entregas_alheias("delete")

    def test_controle_motoristas_leem_apenas_proprias_entregas(self):
        """Controle positivo: o sistema não está bloqueando todas as leituras."""
        for usuario, permitidas in [
            (self.motorista_a, {self.a1.id, self.a2.id}),
            (self.motorista_b, {self.b1.id, self.b2.id}),
        ]:
            with self.subTest(motorista=usuario.username):
                self._autenticar(usuario)
                resposta = self.client.get("/api/deliveries/")
                self.assertEqual(resposta.status_code, status.HTTP_200_OK)
                self.assertEqual({d["id"] for d in resposta.data}, permitidas)
                for id_entrega in permitidas:
                    detalhe = self.client.get(f"/api/deliveries/{id_entrega}/")
                    self.assertEqual(detalhe.status_code, status.HTTP_200_OK)
                    self.assertEqual(detalhe.data["id"], id_entrega)

    def test_controle_gestor_pode_atribuir_entrega(self):
        """Controle positivo: a operação de atribuição realmente funciona para Gestor."""
        self._autenticar(self.gestor)
        resposta = self.client.post(
            f"/api/deliveries/{self.livre1.id}/assign-driver/",
            {"driver_id": self.motorista_a.id}, format="json",
        )
        self.assertEqual(resposta.status_code, status.HTTP_200_OK, resposta.data)
        self.livre1.refresh_from_db()
        self.assertEqual(self.livre1.assigned_driver_id, self.motorista_a.id)

    def test_controle_motorista_nao_pode_cadastrar_entrega(self):
        """Controle complementar: Motorista não cria entregas na API."""
        self._autenticar(self.motorista_a)
        antes = self._fotografia_banco()
        resposta = self.client.post("/api/deliveries/", {
            "origin": "Indevida", "destination": "Indevida",
            "cargo_description": "Cadastro não autorizado",
        }, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(antes, self._fotografia_banco())
