# -*- coding: utf-8 -*-

from djangosige.tests.test_case import BaseTestCase
from djangosige.apps.cadastro.models import Cliente
from djangosige.apps.vendas.models import CondicaoPagamento, OrcamentoVenda, PedidoVenda
from djangosige.apps.estoque.models import LocalEstoque, DEFAULT_LOCAL_ID
from django.urls import reverse

from datetime import datetime, timedelta


VENDA_FORMSET_DATA = {
    'produtos_form-0-produto': 1,
    'produtos_form-0-quantidade': 2,
    'produtos_form-0-valor_unit': '100,00',
    'produtos_form-0-tipo_desconto': '0',
    'produtos_form-0-desconto': '20,00',
    'produtos_form-0-valor_rateio_frete': '0,00',
    'produtos_form-0-valor_rateio_despesas': '0,00',
    'produtos_form-0-valor_rateio_seguro': '0,00',
    'produtos_form-0-subtotal': '180,00',
    'produtos_form-1-produto': 2,
    'produtos_form-1-quantidade': 3,
    'produtos_form-1-valor_unit': '100,00',
    'produtos_form-1-tipo_desconto': '0',
    'produtos_form-1-desconto': '20,00',
    'produtos_form-1-valor_rateio_frete': '0,00',
    'produtos_form-1-valor_rateio_despesas': '0,00',
    'produtos_form-1-valor_rateio_seguro': '0,00',
    'produtos_form-1-subtotal': '280,00',
    'produtos_form-TOTAL_FORMS': 2,
    'produtos_form-INITIAL_FORMS': 0,
    'pagamento_form-1-indice_parcela': 1,
    'pagamento_form-1-vencimento': '31/07/2017',
    'pagamento_form-1-valor_parcela': '460,00',
    'pagamento_form-TOTAL_FORMS': 1,
    'pagamento_form-INITIAL_FORMS': 0,
}


class VendasAdicionarViewsTestCase(BaseTestCase):

    def test_add_orcamento_venda_view_get_request(self):
        url = reverse('djangosige.apps.vendas:addorcamentovendaview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_pedido_venda_view_get_request(self):
        url = reverse('djangosige.apps.vendas:addpedidovendaview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_condicao_pagamento_view_get_request(self):
        url = reverse('djangosige.apps.vendas:addcondicaopagamentoview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_orcamento_venda_view_post_request(self):
        url = reverse('djangosige.apps.vendas:addorcamentovendaview')
        cli = Cliente.objects.order_by('id').last()
        local_orig = LocalEstoque.objects.get(pk=DEFAULT_LOCAL_ID)

        data = {
            'data_emissao': '16/07/2017',
            'cliente': cli.pk,
            'status': '0',
            'tipo_desconto': '0',
            'desconto': '40,00',
            'frete': '0,00',
            'seguro': '0,00',
            'despesas': '0,00',
            'mod_frete': '0',
            'impostos': '0,00',
            'valor_total': '460,00',
            'local_orig': local_orig.pk,
        }

        data.update(VENDA_FORMSET_DATA)

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'vendas/orcamento_venda/orcamento_venda_list.html')

        # Assert form invalido
        data['cliente'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'cliente', 'Este campo é obrigatório.')

    def test_add_pedido_venda_view_post_request(self):
        url = reverse('djangosige.apps.vendas:addpedidovendaview')
        cli = Cliente.objects.order_by('id').last()
        local_orig = LocalEstoque.objects.get(pk=DEFAULT_LOCAL_ID)

        data = {
            'data_emissao': '16/07/2017',
            'cliente': cli.pk,
            'status': '0',
            'tipo_desconto': '0',
            'desconto': '40,00',
            'frete': '0,00',
            'seguro': '0,00',
            'despesas': '0,00',
            'mod_frete': '0',
            'impostos': '0,00',
            'valor_total': '460,00',
            'local_orig': local_orig.pk,
        }

        data.update(VENDA_FORMSET_DATA)

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'vendas/pedido_venda/pedido_venda_list.html')

        # Assert form invalido
        data['cliente'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'cliente', 'Este campo é obrigatório.')

    def test_add_condicao_pagamento_view_post_request(self):
        url = reverse('djangosige.apps.vendas:addcondicaopagamentoview')

        data = {
            'descricao': 'Condicao Pagamento Teste',
            'forma': '99',
            'n_parcelas': 6,
            'dias_recorrencia': 30,
            'parcela_inicial': 0,
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'vendas/pagamento/condicao_pagamento_list.html')

        # Assert form invalido
        data['descricao'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'descricao', 'Este campo é obrigatório.')


class VendasListarViewsTestCase(BaseTestCase):

    def test_list_orcamento_venda_view_deletar_objeto(self):
        cli = Cliente.objects.order_by('id').last()
        obj = OrcamentoVenda.objects.create(cliente=cli)
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.vendas:listaorcamentovendaview'), deleted_object=obj)

    def test_list_orcamento_venda_vencido_view_deletar_objeto(self):
        cli = Cliente.objects.order_by('id').last()
        obj = OrcamentoVenda.objects.create(
            cliente=cli, data_vencimento=datetime.now().date() - timedelta(days=1))
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.vendas:listaorcamentovendavencidoview'), deleted_object=obj)

    def test_list_orcamento_venda_vence_hoje_view_deletar_objeto(self):
        cli = Cliente.objects.order_by('id').last()
        obj = OrcamentoVenda.objects.create(
            cliente=cli, data_vencimento=datetime.now().date())
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.vendas:listaorcamentovendahojeview'), deleted_object=obj)

    def test_list_pedido_venda_view_deletar_objeto(self):
        cli = Cliente.objects.order_by('id').last()
        obj = PedidoVenda.objects.create(cliente=cli)
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.vendas:listapedidovendaview'), deleted_object=obj)

    def test_list_pedido_venda_atrasado_view_deletar_objeto(self):
        cli = Cliente.objects.order_by('id').last()
        obj = PedidoVenda.objects.create(
            cliente=cli, data_entrega=datetime.now().date() - timedelta(days=1))
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.vendas:listapedidovendaatrasadosview'), deleted_object=obj)

    def test_list_pedido_venda_entrega_hoje_view_deletar_objeto(self):
        cli = Cliente.objects.order_by('id').last()
        obj = PedidoVenda.objects.create(
            cliente=cli, data_entrega=datetime.now().date())
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.vendas:listapedidovendahojeview'), deleted_object=obj)

    def test_list_condicao_pagamento_view_deletar_objeto(self):
        obj = CondicaoPagamento.objects.create(n_parcelas=6)
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.vendas:listacondicaopagamentoview'), deleted_object=obj)


class VendasEditarViewsTestCase(BaseTestCase):

    def test_edit_orcamento_venda_get_post_request(self):
        # Buscar objeto qualquer
        obj = OrcamentoVenda.objects.order_by('pk').last()
        url = reverse('djangosige.apps.vendas:editarorcamentovendaview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        data.update(VENDA_FORMSET_DATA)
        data.update(response.context['produtos_form'].initial[0])
        data['observacoes'] = 'Orçamento editado.'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'vendas/orcamento_venda/orcamento_venda_list.html')

    def test_edit_pedido_venda_get_post_request(self):
        # Buscar objeto qualquer
        obj = PedidoVenda.objects.order_by('pk').last()
        url = reverse('djangosige.apps.vendas:editarpedidovendaview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        data.update(VENDA_FORMSET_DATA)
        data.update(response.context['produtos_form'].initial[0])
        data['observacoes'] = 'Pedido editado.'
        if data['orcamento'] is None:
            data['orcamento'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'vendas/pedido_venda/pedido_venda_list.html')

    def test_edit_condicao_pagamento_get_post_request(self):
        # Buscar objeto qualquer
        obj = CondicaoPagamento.objects.order_by('pk').last()
        url = reverse('djangosige.apps.vendas:editarcondicaopagamentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        data['descricao'] = 'Condição de pagamento editada'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)


class VendasAjaxRequestViewsTestCase(BaseTestCase):

    def test_info_condicao_pagamento_post_request(self):
        # Buscar objeto qualquer
        obj = CondicaoPagamento.objects.order_by('pk').last()
        obj_pk = obj.pk
        url = reverse('djangosige.apps.vendas:infocondpagamento')
        data = {'pagamentoId': obj_pk}
        self.check_json_response(
            url, data, obj_pk, model='vendas.condicaopagamento')

    def test_info_venda_post_request(self):
        # Buscar objeto qualquer
        obj = PedidoVenda.objects.order_by('pk').last()
        obj_pk = obj.pk
        url = reverse('djangosige.apps.vendas:infovenda')
        data = {'vendaId': obj_pk}
        self.check_json_response(url, data, obj_pk, model='vendas.pedidovenda')


class VendasAcoesUsuarioViewsTestCase(BaseTestCase):

    def test_gerar_pdf_orcamento_venda(self):
        # Buscar objeto qualquer
        obj = OrcamentoVenda.objects.order_by('pk').last()
        url = reverse('djangosige.apps.vendas:gerarpdforcamentovenda',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/pdf')

    def test_gerar_pdf_pedido_venda(self):
        # Buscar objeto qualquer
        obj = PedidoVenda.objects.order_by('pk').last()
        url = reverse('djangosige.apps.vendas:gerarpdfpedidovenda',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/pdf')

    def test_gerar_pedido_venda(self):
        # Criar novo orcamento e gerar pedido
        cli = Cliente.objects.order_by('id').last()
        obj = OrcamentoVenda.objects.create(cliente=cli)
        url = reverse('djangosige.apps.vendas:gerarpedidovenda',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'vendas/pedido_venda/pedido_venda_edit.html')
        self.assertTrue(isinstance(response.context['object'], PedidoVenda))
        self.assertEqual(response.context['object'].orcamento.pk, obj.pk)

    def test_copiar_pedido_venda(self):
        # Buscar objeto qualquer
        obj = PedidoVenda.objects.order_by('pk').last()
        url = reverse('djangosige.apps.vendas:copiarpedidovenda',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'vendas/pedido_venda/pedido_venda_edit.html')
        self.assertTrue(isinstance(response.context['object'], PedidoVenda))

    def test_copiar_orcamento_venda(self):
        # Buscar objeto qualquer
        obj = OrcamentoVenda.objects.order_by('pk').last()
        url = reverse('djangosige.apps.vendas:copiarorcamentovenda',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'vendas/orcamento_venda/orcamento_venda_edit.html')
        self.assertTrue(isinstance(response.context['object'], OrcamentoVenda))

    def test_cancelar_pedido_venda(self):
        # Buscar objeto qualquer
        obj = PedidoVenda.objects.order_by('pk').last()
        url = reverse('djangosige.apps.vendas:cancelarpedidovenda',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'vendas/pedido_venda/pedido_venda_edit.html')
        self.assertTrue(isinstance(response.context['object'], PedidoVenda))
        self.assertEqual(response.context[
                         'object'].get_status_display(), 'Cancelado')

    def test_cancelar_orcamento_venda(self):
        # Buscar objeto qualquer
        obj = OrcamentoVenda.objects.order_by('pk').last()
        url = reverse('djangosige.apps.vendas:cancelarorcamentovenda',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'vendas/orcamento_venda/orcamento_venda_edit.html')
        self.assertTrue(isinstance(response.context['object'], OrcamentoVenda))
        self.assertEqual(response.context[
                         'object'].get_status_display(), 'Cancelado')
