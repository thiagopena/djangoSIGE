# -*- coding: utf-8 -*-

from djangosige.tests.test_case import BaseTestCase
from django.core.urlresolvers import reverse
from djangosige.apps.financeiro.models import MovimentoCaixa, Entrada, Saida, PlanoContasGrupo, PlanoContasSubgrupo

from datetime import datetime, timedelta

GRUPO_PLANO_CONTAS_FORMSET_DATA = {
    'subgrupo_form-0-descricao': 'Subgrupo1',
    'subgrupo_form-1-descricao': 'Subgrupo2',
    'subgrupo_form-TOTAL_FORMS': 2,
    'subgrupo_form-INITIAL_FORMS': 0,
}


class FinanceiroFluxoCaixaViewTestCase(BaseTestCase):
    url = reverse('financeiro:fluxodecaixaview')

    def test_fluxo_caixa_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('movimentos' in response.context)

        # Testar permissao
        permission_codename = 'acesso_fluxodecaixa'
        self.check_user_get_permission(
            self.url, permission_codename=permission_codename)

    def test_fluxo_caixa_get_request_data_inicial(self):
        data_inicial = datetime.today()
        data = {
            'from': data_inicial.strftime('%d/%m/%Y'),
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['movimentos']), list(
            MovimentoCaixa.objects.filter(data_movimento__range=(data_inicial, data_inicial))))

    def test_fluxo_caixa_get_request_data_final(self):
        data_final = datetime.today()
        data = {
            'to': data_final.strftime('%d/%m/%Y'),
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['movimentos']), list(
            MovimentoCaixa.objects.filter(data_movimento__range=(data_final, data_final))))

    def test_fluxo_caixa_get_request_datas_inicial_final(self):
        data_inicial = datetime.today()
        data_final = datetime.today() + timedelta(days=30)
        data = {
            'from': data_inicial.strftime('%d/%m/%Y'),
            'to': data_final.strftime('%d/%m/%Y'),
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['movimentos']), list(
            MovimentoCaixa.objects.filter(data_movimento__range=(data_inicial, data_final))))

    def test_fluxo_caixa_get_request_data_formato_errado(self):
        data_inicial = datetime.today()
        data = {
            'from': data_inicial.strftime('%d-%m-%Y'),  # Formato Invalido
        }
        response = self.client.get(self.url, data)
        msgs = list(response.context['messages'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(msgs), 1)
        self.assertEqual(
            str(msgs[0]), 'Formato de data incorreto, deve ser no formato DD/MM/AAAA')


class FinanceiroAdicionarViewsTestCase(BaseTestCase):

    def test_add_grupo_view_get_request(self):
        url = reverse('financeiro:addgrupoview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_conta_pagar_view_get_request(self):
        url = reverse('financeiro:addcontapagarview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_conta_receber_view_get_request(self):
        url = reverse('financeiro:addcontareceberview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_recebimento_view_get_request(self):
        url = reverse('financeiro:addrecebimentoview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_pagamento_view_get_request(self):
        url = reverse('financeiro:addpagamentoview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_grupo_view_post_request(self):
        url = reverse('financeiro:addgrupoview')

        data = {
            'grupo_form-tipo_grupo': '0',
            'grupo_form-descricao': 'Entrada1',
        }

        data.update(GRUPO_PLANO_CONTAS_FORMSET_DATA)

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/plano/plano.html')

        # Assert form invalido
        data['grupo_form-descricao'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'descricao', 'Este campo é obrigatório.')

    def test_add_conta_pagar_view_post_request(self):
        url = reverse('financeiro:addcontapagarview')
        data_atual = datetime.today() + timedelta(days=30)

        data = {
            'status': '1',
            'descricao': 'Conta a pagar Teste1',
            'valor_total': '100,00',
            'abatimento': '0,00',
            'juros': '0,00',
            'valor_liquido': '100,00',
            'data_vencimento': data_atual.strftime('%d/%m/%Y'),
            'movimentar_caixa': True,
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento de caixa foi criado e se a saida foi
        # adicionada
        movimento_criado = MovimentoCaixa.objects.get(
            data_movimento=data_atual)
        self.assertTrue(movimento_criado.saidas >= 100)

        # Assert form invalido
        data['descricao'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'descricao', 'Este campo é obrigatório.')

    def test_add_conta_receber_view_post_request(self):
        url = reverse('financeiro:addcontareceberview')
        data_atual = datetime.today() + timedelta(days=30)

        data = {
            'status': '1',
            'descricao': 'Conta a receber Teste1',
            'valor_total': '100,00',
            'abatimento': '0,00',
            'juros': '0,00',
            'valor_liquido': '100,00',
            'data_vencimento': data_atual.strftime('%d/%m/%Y'),
            'movimentar_caixa': True,
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento de caixa foi criado e se a saida foi
        # adicionada
        movimento_criado = MovimentoCaixa.objects.get(
            data_movimento=data_atual)
        self.assertTrue(movimento_criado.entradas >= 100)

        # Assert form invalido
        data['descricao'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'descricao', 'Este campo é obrigatório.')

    def test_add_recebimento_view_post_request(self):
        url = reverse('financeiro:addrecebimentoview')
        data_atual = datetime.today()

        data = {
            'status': '0',
            'descricao': 'Recebimento Teste1',
            'valor_total': '100,00',
            'abatimento': '0,00',
            'juros': '0,00',
            'valor_liquido': '100,00',
            'data_pagamento': data_atual.strftime('%d/%m/%Y'),
            'movimentar_caixa': True,
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento de caixa foi criado e se a saida foi
        # adicionada
        movimento_criado = MovimentoCaixa.objects.get(
            data_movimento=data_atual)
        self.assertTrue(movimento_criado.entradas >= 100)

        # Assert form invalido
        data['descricao'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'descricao', 'Este campo é obrigatório.')

    def test_add_pagamento_view_post_request(self):
        url = reverse('financeiro:addpagamentoview')
        data_atual = datetime.today()

        data = {
            'status': '0',
            'descricao': 'Pagamento Teste1',
            'valor_total': '100,00',
            'abatimento': '0,00',
            'juros': '0,00',
            'valor_liquido': '100,00',
            'data_pagamento': data_atual.strftime('%d/%m/%Y'),
            'movimentar_caixa': True,
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento de caixa foi criado e se a saida foi
        # adicionada
        movimento_criado = MovimentoCaixa.objects.get(
            data_movimento=data_atual)
        self.assertTrue(movimento_criado.saidas >= 100)

        # Assert form invalido
        data['descricao'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'descricao', 'Este campo é obrigatório.')


class FinanceiroPlanoContasViewsTestCase(BaseTestCase):
    url = reverse('financeiro:planocontasview')

    def test_plano_contas_view_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Testar permissao
        permission_codename = 'view_planocontasgrupo'
        self.check_user_get_permission(
            self.url, permission_codename=permission_codename)

    def test_deletar_grupo_plano_contas(self):
        obj = PlanoContasGrupo.objects.create(
            codigo='000001', tipo_grupo='0', descricao='Grupo Entrada Teste')
        self.check_list_view_delete(
            url=self.url, deleted_object=obj, context_object_key='all_grupos_entrada')

    def test_deletar_subgrupo_plano_contas(self):
        grupo = PlanoContasGrupo.objects.filter(tipo_grupo='0')[0]
        PlanoContasSubgrupo.objects.create(
            codigo='000010', tipo_grupo='0', descricao='Subgrupo Entrada Teste', grupo=grupo)
        obj = PlanoContasGrupo.objects.get(
            codigo='000010', tipo_grupo='0', descricao='Subgrupo Entrada Teste')
        self.check_list_view_delete(
            url=self.url, deleted_object=obj, context_object_key='all_grupos_entrada')


class FinanceiroListarViewsTestCase(BaseTestCase):

    def test_list_conta_pagar_view_deletar_objeto(self):
        obj = Saida.objects.create(status='1')
        self.check_list_view_delete(url=reverse(
            'financeiro:listacontapagarview'), deleted_object=obj)

    def test_list_conta_pagar_atrasada_view_deletar_objeto(self):
        obj = Saida.objects.create(
            status='1', data_vencimento=datetime.today() - timedelta(days=1))
        self.check_list_view_delete(url=reverse(
            'financeiro:listacontapagaratrasadasview'), deleted_object=obj)

    def test_list_conta_pagar_hoje_view_deletar_objeto(self):
        obj = Saida.objects.create(
            status='1', data_vencimento=datetime.today())
        self.check_list_view_delete(url=reverse(
            'financeiro:listacontapagarhojeview'), deleted_object=obj)

    def test_list_conta_receber_view_deletar_objeto(self):
        obj = Entrada.objects.create(status='1')
        self.check_list_view_delete(url=reverse(
            'financeiro:listacontareceberview'), deleted_object=obj)

    def test_list_conta_receber_atrasada_view_deletar_objeto(self):
        obj = Entrada.objects.create(
            status='1', data_vencimento=datetime.today() - timedelta(days=1))
        self.check_list_view_delete(url=reverse(
            'financeiro:listacontareceberatrasadasview'), deleted_object=obj)

    def test_list_conta_receber_hoje_view_deletar_objeto(self):
        obj = Entrada.objects.create(
            status='1', data_vencimento=datetime.today())
        self.check_list_view_delete(url=reverse(
            'financeiro:listacontareceberhojeview'), deleted_object=obj)

    def test_list_recebimento_view_deletar_objeto(self):
        obj = Entrada.objects.create(status='0')
        self.check_list_view_delete(url=reverse(
            'financeiro:listarecebimentosview'), deleted_object=obj)

    def test_list_pagamento_view_deletar_objeto(self):
        obj = Saida.objects.create(status='0')
        self.check_list_view_delete(url=reverse(
            'financeiro:listapagamentosview'), deleted_object=obj)
