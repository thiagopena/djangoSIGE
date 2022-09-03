# -*- coding: utf-8 -*-

from djangosige.tests.test_case import BaseTestCase
from djangosige.apps.cadastro.models import Produto
from djangosige.apps.estoque.models import LocalEstoque, DEFAULT_LOCAL_ID, ProdutoEstocado, EntradaEstoque, SaidaEstoque, TransferenciaEstoque
from django.urls import reverse

MOVIMENTO_ESTOQUE_FORMSET_DATA = {
    'itens_form-0-produto': 1,
    'itens_form-0-quantidade': 2,
    'itens_form-0-valor_unit': '100,00',
    'itens_form-0-subtotal': '180,00',
    'itens_form-1-produto': 2,
    'itens_form-1-quantidade': 3,
    'itens_form-1-valor_unit': '100,00',
    'itens_form-1-subtotal': '280,00',
    'itens_form-TOTAL_FORMS': 2,
    'itens_form-INITIAL_FORMS': 0,
}


class EstoqueConsultaViewTestCase(BaseTestCase):
    url = reverse('djangosige.apps.estoque:consultaestoqueview')

    def test_consulta_estoque_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_consulta_estoque_get_request_local(self):
        # Request com local definido
        local = LocalEstoque.objects.get(pk=DEFAULT_LOCAL_ID)
        data = {
            'local': local.pk,
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test_consulta_estoque_get_request_produto(self):
        # Request com produto definido
        prod = Produto.objects.filter(controlar_estoque=True).first()
        data = {
            'produto': prod.pk,
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)


class EstoqueAdicionarViewsTestCase(BaseTestCase):

    def test_add_local_estoque_view_get_request(self):
        url = reverse('djangosige.apps.estoque:addlocalview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_entrada_estoque_view_get_request(self):
        url = reverse('djangosige.apps.estoque:addentradaestoqueview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_saida_estoque_view_get_request(self):
        url = reverse('djangosige.apps.estoque:addsaidaestoqueview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_transferencia_estoque_view_get_request(self):
        url = reverse('djangosige.apps.estoque:addtransferenciaestoqueview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_local_estoque_view_post_request(self):
        url = reverse('djangosige.apps.estoque:addlocalview')

        data = {
            'descricao': 'Local Estoque Teste 1',
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Assert form invalido
        data['descricao'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'descricao', 'Este campo é obrigatório.')

    def test_add_entrada_estoque_view_post_request(self):
        url = reverse('djangosige.apps.estoque:addentradaestoqueview')
        local = LocalEstoque.objects.get(pk=DEFAULT_LOCAL_ID)

        data = {
            'quantidade_itens': 2,
            'valor_total': '460,00',
            'tipo_movimento': '0',
            'local_dest': local.pk,
        }

        data.update(MOVIMENTO_ESTOQUE_FORMSET_DATA)

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'estoque/movimento/movimento_estoque_list.html')

        # Assert form invalido
        data['tipo_movimento'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'tipo_movimento', 'Este campo é obrigatório.')

    def test_add_saida_estoque_view_post_request(self):
        url = reverse('djangosige.apps.estoque:addsaidaestoqueview')
        local = LocalEstoque.objects.get(pk=DEFAULT_LOCAL_ID)

        data = {
            'quantidade_itens': 2,
            'valor_total': '460,00',
            'tipo_movimento': '0',
            'local_orig': local.pk,
        }

        data.update(MOVIMENTO_ESTOQUE_FORMSET_DATA)

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'estoque/movimento/movimento_estoque_list.html')

        # Assert form invalido
        data['tipo_movimento'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'tipo_movimento', 'Este campo é obrigatório.')

        # Testar retirar produtos de um local sem produtos em estoque
        local = LocalEstoque.objects.create(descricao='Novo Local Estoque 1')
        data['local_orig'] = local.pk
        data['tipo_movimento'] = '0'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'estoque/movimento/movimento_estoque_list.html')

        # Testar retirar produto com estoque atual abaixo do movimentado
        prod1 = Produto.objects.create(
            descricao='Produto com estoque zero', controlar_estoque=True, estoque_atual='0.00')
        ProdutoEstocado(local=local, produto=prod1, quantidade=30).save()
        data['itens_form-2-produto'] = prod1.pk
        data['itens_form-2-quantidade'] = 10
        data['itens_form-2-valor_unit'] = '50,00'
        data['itens_form-2-subtotal'] = '500,00'
        data['itens_form-TOTAL_FORMS'] = 3
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFormsetError(
            response, 'itens_form', 2, 'quantidade', 'Quantidade retirada do estoque maior que o estoque atual (' + str(prod1.estoque_atual).replace('.', ',') + ') do produto.')

    def test_add_transferencia_estoque_view_post_request(self):
        url = reverse('djangosige.apps.estoque:addtransferenciaestoqueview')
        local1 = LocalEstoque.objects.get(pk=DEFAULT_LOCAL_ID)
        local2 = LocalEstoque.objects.create(descricao='Novo Local Estoque 2')

        data = {
            'quantidade_itens': 2,
            'valor_total': '460,00',
            'tipo_movimento': '0',
            'local_estoque_orig': local1.pk,
            'local_estoque_dest': local2.pk,
        }

        data.update(MOVIMENTO_ESTOQUE_FORMSET_DATA)

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'estoque/movimento/movimento_estoque_list.html')

        # Testar tranferencia de estoque com produto abaixo
        data['quantidade_itens'] = 2
        data['local_estoque_orig'] = local2.pk
        data['local_estoque_dest'] = local1.pk
        data['itens_form-0-quantidade'] = 10
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Assert form invalido
        data['quantidade_itens'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'quantidade_itens', 'Este campo é obrigatório.')


class EstoqueListarViewsTestCase(BaseTestCase):

    def test_list_entrada_estoque_view_deletar_objeto(self):
        obj = EntradaEstoque.objects.create()
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.estoque:listaentradasestoqueview'), deleted_object=obj)

    def test_list_saida_estoque_view_deletar_objeto(self):
        obj = SaidaEstoque.objects.create()
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.estoque:listasaidasestoqueview'), deleted_object=obj)

    def test_list_transferencia_estoque_view_deletar_objeto(self):
        obj = TransferenciaEstoque.objects.create(local_estoque_orig=LocalEstoque.objects.order_by(
            'id').first(), local_estoque_dest=LocalEstoque.objects.order_by('id').last())
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.estoque:listatransferenciasestoqueview'), deleted_object=obj)

    def test_list_todas_movimentacoes_estoque_view_deletar_objetos(self):
        obj = SaidaEstoque.objects.create()
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.estoque:listamovimentoestoqueview'), deleted_object=obj)
        obj = EntradaEstoque.objects.create()
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.estoque:listamovimentoestoqueview'), deleted_object=obj)
        obj = TransferenciaEstoque.objects.create(local_estoque_orig=LocalEstoque.objects.order_by(
            'id').first(), local_estoque_dest=LocalEstoque.objects.order_by('id').last())
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.estoque:listamovimentoestoqueview'), deleted_object=obj)

    def test_list_local_estoque_view_deletar_objeto(self):
        obj = LocalEstoque.objects.create()
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.estoque:listalocalview'), deleted_object=obj)


class EstoqueEditarViewsTestCase(BaseTestCase):

    def test_detalhar_entrada_estoque_get_request(self):
        # Buscar objeto qualquer
        obj = EntradaEstoque.objects.order_by('pk').last()
        url = reverse('djangosige.apps.estoque:detalharentradaestoqueview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'estoque/movimento/movimento_estoque_detail.html')

    def test_detalhar_saida_estoque_get_request(self):
        # Buscar objeto qualquer
        obj = SaidaEstoque.objects.order_by('pk').last()
        url = reverse('djangosige.apps.estoque:detalharsaidaestoqueview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'estoque/movimento/movimento_estoque_detail.html')

    def test_detalhar_transferencia_estoque_get_request(self):
        # Buscar objeto qualquer
        obj = TransferenciaEstoque.objects.order_by('pk').last()
        url = reverse('djangosige.apps.estoque:detalhartransferenciaestoqueview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'estoque/movimento/movimento_estoque_detail.html')

    def test_edit_local_estoque_get_post_request(self):
        # Buscar objeto qualquer
        obj = LocalEstoque.objects.order_by('pk').last()
        url = reverse('djangosige.apps.estoque:editarlocalview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        data['descricao'] = 'Local Estoque Editado'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
