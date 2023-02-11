# -*- coding: utf-8 -*-

from django.test import TestCase
from djangosige.apps.cadastro.models import Produto
from djangosige.apps.estoque.models import (
    LocalEstoque,
    ItensMovimento,
    EntradaEstoque,
    SaidaEstoque
)


class MovimentoEstoqueModelTestCase(TestCase):
    """
    Testa remoção de movimentos de estoque
    """

    def test_saida_estoque_delete(self):
        """
        Testa se estoque é reajustado em caso de remoção de saída de estoque
        """
        # Cria produto, local e movimentações
        produto = Produto.objects.create(
            codigo="123", descricao="produto", estoque_atual=100)
        local = LocalEstoque.objects.create(descricao="localTeste")
        # Adiciona produtos estocados
        produto_estocado = local.local_produto_estocado.create(
            produto=produto, quantidade=100)
        # Cria saída de estoque
        mov = SaidaEstoque.objects.create(
            local_orig=local, quantidade_itens=50)
        ItensMovimento.objects.create(
            produto=produto, movimento_id=mov, quantidade=50)
        # Remove a saída de estoque que acabamos de criar
        mov.delete()
        # Verifica se os valores em estoque foram modificados
        # Os valores estarão somados aos valores atuais pois as saídas não
        # foram registradas
        produto.refresh_from_db()
        produto_estocado.refresh_from_db()
        self.assertEqual(int(produto.estoque_atual), 150)
        self.assertEqual(int(produto_estocado.quantidade), 150)

    def test_entrada_estoque_delete(self):
        """
        Testa se estoque é reajustado em caso de remoção de entrada no estoque
        """
        # Cria produto, local e movimentações
        produto = Produto.objects.create(
            codigo="123", descricao="produto", estoque_atual=100)
        local = LocalEstoque.objects.create(descricao="localTeste")
        # Adiciona produtos estocados
        produto_estocado = local.local_produto_estocado.create(
            produto=produto, quantidade=100)
        # Cria entrada em estoque
        mov = EntradaEstoque.objects.create(
            local_dest=local, quantidade_itens=50)
        ItensMovimento.objects.create(
            produto=produto, movimento_id=mov, quantidade=50)
        # Remove a entrada em estoque que acabamos de criar
        mov.delete()
        # Verifica se os valores em estoque foram modificados
        # Os valores estarão subtraídos dos valores atuais pois as entradas não
        # foram registradas
        produto.refresh_from_db()
        produto_estocado.refresh_from_db()
        self.assertEqual(int(produto.estoque_atual), 50)
        self.assertEqual(int(produto_estocado.quantidade), 50)
