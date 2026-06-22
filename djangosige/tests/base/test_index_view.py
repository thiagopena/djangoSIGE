from datetime import datetime, timedelta
from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from djangosige.apps.financeiro.models import MovimentoCaixa


class IndexViewAuthTestCase(TestCase):
    """Contexto: Testes de autorização e controle de acesso à IndexView."""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = reverse("base:index")
        cls.credenciais = {
            "username": "admin",
            "password": "admin@xpt0",
        }
        cls.user = get_user_model().objects.create_user(**cls.credenciais)
        return super().setUpTestData()

    def test_o_usuario_nao_esta_logado(self) -> None:
        """Garante que usuários anônimos não acessam a rota (ou recebem 404/Redirect)"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_o_usuario_esta_logado(self) -> None:
        """Garante que usuários autenticados conseguem acessar a rota com sucesso"""
        self.client.login(**self.credenciais)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class IndexViewMovimentoCaixaTestCase(TestCase):
    """Contexto: Validação da lógica de negócio de saldos e MovimentoCaixa (Issue 1)."""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.credenciais = {
            "username": "admin",
            "password": "admin@xpt0",
        }
        cls.user = get_user_model().objects.create_user(**cls.credenciais)
        return super().setUpTestData()

    def setUp(self):
        self.url = reverse("base:index")
        self.data_atual = datetime.now().date()
        self.data_ontem = self.data_atual - timedelta(days=1)
        self.client.login(**self.credenciais)

    def test_movimento_caixa_do_dia_atual(self):
        """Cenário 1: Se existir movimento hoje, ele deve ser injetado no contexto"""
        movimento_hoje = MovimentoCaixa.objects.create(
            data_movimento=self.data_atual, saldo_final=150
        )

        response = self.client.get(self.url)

        self.assertEqual(response.context["movimento_dia"], movimento_hoje)
        self.assertNotIn("saldo", response.context)

    def test_saldo_do_ultimo_movimento_quando_nao_ha_hoje(self):
        """Cenário 2: Sem movimento hoje, busca o saldo_final do último movimento realizado"""
        MovimentoCaixa.objects.create(
            data_movimento=self.data_ontem, saldo_final=350.50
        )

        response = self.client.get(self.url)

        self.assertIsNone(response.context.get("movimento_dia"))
        self.assertEqual(response.context["saldo"], 350.50)

    def test_saldo_padrao_quando_nao_ha_nenhum_movimento(self):
        """Cenário 3: Banco totalmente vazio de movimentos deve retornar '0,00'"""
        MovimentoCaixa.objects.all().delete()

        response = self.client.get(self.url)

        self.assertIsNone(response.context.get("movimento_dia"))
        self.assertEqual(response.context["saldo"], "0,00")
