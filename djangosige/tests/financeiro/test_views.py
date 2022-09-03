# -*- coding: utf-8 -*-

from djangosige.tests.test_case import BaseTestCase, replace_none_values_in_dictionary
from djangosige.apps.financeiro.models import MovimentoCaixa, Entrada, Saida, PlanoContasGrupo, PlanoContasSubgrupo
from djangosige.apps.estoque.models import SaidaEstoque

from django.urls import reverse
from django.db.models import Q

from datetime import datetime, timedelta
from decimal import Decimal
import json
import locale
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')


SUBGRUPO_PLANO_CONTAS_FORMSET_DATA = {
    'subgrupo_form-0-descricao': 'Subgrupo1',
    'subgrupo_form-1-descricao': 'Subgrupo2',
    'subgrupo_form-TOTAL_FORMS': 2,
    'subgrupo_form-INITIAL_FORMS': 0,
}


class FinanceiroFluxoCaixaViewTestCase(BaseTestCase):
    url = reverse('djangosige.apps.financeiro:fluxodecaixaview')

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
        url = reverse('djangosige.apps.financeiro:addgrupoview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_conta_pagar_view_get_request(self):
        url = reverse('djangosige.apps.financeiro:addcontapagarview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_conta_receber_view_get_request(self):
        url = reverse('djangosige.apps.financeiro:addcontareceberview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_recebimento_view_get_request(self):
        url = reverse('djangosige.apps.financeiro:addrecebimentoview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_pagamento_view_get_request(self):
        url = reverse('djangosige.apps.financeiro:addpagamentoview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_grupo_view_post_request(self):
        url = reverse('djangosige.apps.financeiro:addgrupoview')

        data = {
            'grupo_form-tipo_grupo': '0',
            'grupo_form-descricao': 'Entrada1',
        }

        data.update(SUBGRUPO_PLANO_CONTAS_FORMSET_DATA)

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
        url = reverse('djangosige.apps.financeiro:addcontapagarview')
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
        url = reverse('djangosige.apps.financeiro:addcontareceberview')
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
        url = reverse('djangosige.apps.financeiro:addrecebimentoview')
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
        url = reverse('djangosige.apps.financeiro:addpagamentoview')
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
    url = reverse('djangosige.apps.financeiro:planocontasview')

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

    def test_list_todos_lancamentos_view_deletar_objetos(self):
        url = reverse('djangosige.apps.financeiro:listalancamentoview')
        obj = Entrada.objects.create()
        self.check_list_view_delete(url=url, deleted_object=obj)
        obj = Saida.objects.create()
        self.check_list_view_delete(url=url, deleted_object=obj)

    def test_list_conta_pagar_view_deletar_objeto(self):
        obj = Saida.objects.create(status='1')
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.financeiro:listacontapagarview'), deleted_object=obj)

    def test_list_conta_pagar_atrasada_view_deletar_objeto(self):
        obj = Saida.objects.create(
            status='1', data_vencimento=datetime.today() - timedelta(days=1))
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.financeiro:listacontapagaratrasadasview'), deleted_object=obj)

    def test_list_conta_pagar_hoje_view_deletar_objeto(self):
        obj = Saida.objects.create(
            status='1', data_vencimento=datetime.today())
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.financeiro:listacontapagarhojeview'), deleted_object=obj)

    def test_list_conta_receber_view_deletar_objeto(self):
        obj = Entrada.objects.create(status='1')
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.financeiro:listacontareceberview'), deleted_object=obj)

    def test_list_conta_receber_atrasada_view_deletar_objeto(self):
        obj = Entrada.objects.create(
            status='1', data_vencimento=datetime.today() - timedelta(days=1))
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.financeiro:listacontareceberatrasadasview'), deleted_object=obj)

    def test_list_conta_receber_hoje_view_deletar_objeto(self):
        obj = Entrada.objects.create(
            status='1', data_vencimento=datetime.today())
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.financeiro:listacontareceberhojeview'), deleted_object=obj)

    def test_list_recebimento_view_deletar_objeto(self):
        novo_movimento = MovimentoCaixa(
            data_movimento=datetime.today(), entradas=Decimal('120.00'))
        try:
            ultimo_mvmt = MovimentoCaixa.objects.filter(
                data_movimento__lt=novo_movimento.data_movimento).latest('data_movimento')
            novo_movimento.saldo_inicial = ultimo_mvmt.saldo_final
            novo_movimento.saldo_final = novo_movimento.saldo_inicial + \
                Decimal('120.00')
        except MovimentoCaixa.DoesNotExist:
            novo_movimento.saldo_inicial = Decimal('0.00')
            novo_movimento.saldo_final = Decimal('120.00')

        novo_movimento.save()
        obj = Entrada.objects.create(descricao='Nova Entrada Teste', status='0', valor_total=Decimal(
            '120.00'), valor_liquido=Decimal('120.00'), movimentar_caixa=True, movimento_caixa=novo_movimento)
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.financeiro:listarecebimentosview'), deleted_object=obj)

        # Verificar movimento deletado
        self.assertFalse(MovimentoCaixa.objects.filter(
            pk=novo_movimento.pk).exists())

    def test_list_pagamento_view_deletar_objeto(self):
        novo_movimento = MovimentoCaixa(
            data_movimento=datetime.today(), saidas=Decimal('120.00'))
        try:
            ultimo_mvmt = MovimentoCaixa.objects.filter(
                data_movimento__lt=novo_movimento.data_movimento).latest('data_movimento')
            novo_movimento.saldo_inicial = ultimo_mvmt.saldo_final
            novo_movimento.saldo_final = novo_movimento.saldo_inicial - \
                Decimal('120.00')
        except MovimentoCaixa.DoesNotExist:
            novo_movimento.saldo_inicial = Decimal('0.00')
            novo_movimento.saldo_final = Decimal('-120.00')

        novo_movimento.save()
        obj = Saida.objects.create(descricao='Nova Saida Teste', status='0', valor_total=Decimal(
            '120.00'), valor_liquido=Decimal('120.00'), movimentar_caixa=True, movimento_caixa=novo_movimento)
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.financeiro:listapagamentosview'), deleted_object=obj)

        # Verificar movimento deletado
        self.assertFalse(MovimentoCaixa.objects.filter(
            pk=novo_movimento.pk).exists())


class FinanceiroEditarViewsTestCase(BaseTestCase):

    def test_edit_grupo_get_post_request(self):
        # Buscar objeto qualquer
        obj = PlanoContasGrupo.objects.order_by('pk').last()
        url = reverse('djangosige.apps.financeiro:editargrupoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        data.update(SUBGRUPO_PLANO_CONTAS_FORMSET_DATA)
        data['descricao'] = 'Grupo Editado editado.'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/plano/plano.html')

    def test_edit_conta_pagar_get_post_request(self):
        # Buscar objeto qualquer
        obj = Saida.objects.filter(status='1').order_by('pk').last()
        url = reverse('djangosige.apps.financeiro:editarcontapagarview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Conta Pagar editada'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Assert form invalido
        data['descricao'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'descricao', 'Este campo é obrigatório.')

    def test_edit_conta_receber_get_post_request(self):
        # Buscar objeto qualquer
        obj = Entrada.objects.filter(status='1').order_by('pk').last()
        url = reverse('djangosige.apps.financeiro:editarcontareceberview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Conta Receber editada'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

    def test_edit_recebimento_com_data_pagamento_igual_get_post_request(self):
        # Buscar entrada com movimento de caixa e data_pagamento
        # Nao modificar a data_pagamento atual, para buscar o mesmo movimento
        obj = Entrada.objects.filter(status='0', movimentar_caixa=True).exclude(
            Q(movimento_caixa__isnull=True) | Q(data_pagamento__isnull=True)).order_by('pk').last()
        valor_saldo_final_antigo = obj.movimento_caixa.saldo_final
        data_movimento = obj.movimento_caixa.data_movimento
        url = reverse('djangosige.apps.financeiro:editarrecebimentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Recebimento editado'
        data['valor_total'] = locale.format(u'%.2f', Decimal(
            data['valor_total']) + Decimal('20.00'), 1)
        data['valor_liquido'] = locale.format(u'%.2f', Decimal(
            data['valor_liquido']) + Decimal('20.00'), 1)
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento de caixa foi atualizado
        movimento_editado = MovimentoCaixa.objects.get(
            data_movimento=data_movimento)
        self.assertEqual(
            valor_saldo_final_antigo + Decimal('20.00'),
            movimento_editado.saldo_final
        )

    def test_edit_recebimento_com_data_pagamento_diferente_e_movimento_criado_get_post_request(self):
        # Buscar entrada com movimento de caixa e data_pagamento
        # Modificar a data_pagamento atual, para buscar outro movimento ou
        # criar um novo
        obj = Entrada.objects.filter(status='0', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | Q(
            data_pagamento__isnull=True) | Q(data_pagamento=datetime.strptime('06/07/2017', "%d/%m/%Y").date())).order_by('pk').last()
        # Data aleatoria, que nao possui movimentos de caixa
        nova_data_pagamento = datetime.strptime(
            '01/01/2020', "%d/%m/%Y").date()
        url = reverse('djangosige.apps.financeiro:editarrecebimentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        novo_valor_entradas = Decimal(data['valor_liquido']) + Decimal('20.00')
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Recebimento editado'
        data['valor_total'] = locale.format(u'%.2f', Decimal(
            data['valor_total']) + Decimal('20.00'), 1)
        data['valor_liquido'] = locale.format(u'%.2f', Decimal(
            data['valor_liquido']) + Decimal('20.00'), 1)
        data['data_pagamento'] = nova_data_pagamento.strftime('%d/%m/%Y')
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento foi criado corretamente
        movimento_editado = MovimentoCaixa.objects.get(
            data_movimento=nova_data_pagamento)
        self.assertEqual(movimento_editado.entradas, novo_valor_entradas)

    def test_edit_recebimento_com_data_pagamento_diferente_e_movimento_existe_get_post_request(self):
        # Buscar entrada com movimento de caixa e data_pagamento
        # Modificar a data_pagamento atual, para buscar outro movimento ou
        # criar um novo
        obj = Entrada.objects.filter(status='0', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | Q(
            data_pagamento__isnull=True) | Q(data_pagamento=datetime.strptime('06/07/2017', "%d/%m/%Y").date())).order_by('pk').last()
        # Data que possui movimento de caixa
        nova_data_pagamento = datetime.strptime(
            '06/07/2017', "%d/%m/%Y").date()
        url = reverse('djangosige.apps.financeiro:editarrecebimentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        novo_valor_entradas = MovimentoCaixa.objects.get(
            data_movimento=nova_data_pagamento).entradas + Decimal(data['valor_liquido']) + Decimal('20.00')
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Recebimento editado'
        data['valor_total'] = locale.format(u'%.2f', Decimal(
            data['valor_total']) + Decimal('20.00'), 1)
        data['valor_liquido'] = locale.format(u'%.2f', Decimal(
            data['valor_liquido']) + Decimal('20.00'), 1)
        data['data_pagamento'] = nova_data_pagamento.strftime('%d/%m/%Y')
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento foi editado corretamente
        movimento_editado = MovimentoCaixa.objects.get(
            data_movimento=nova_data_pagamento)
        self.assertEqual(movimento_editado.entradas, novo_valor_entradas)

    def test_edit_recebimento_sem_data_pagamento_vencimento_get_post_request(self):
        # Buscar entrada com movimento de caixa e data_pagamento
        obj = Entrada.objects.filter(status='0', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | Q(
            data_pagamento__isnull=True) | Q(data_pagamento=datetime.strptime('06/07/2017', "%d/%m/%Y").date())).order_by('pk').last()
        url = reverse('djangosige.apps.financeiro:editarrecebimentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Recebimento editado'
        data['data_pagamento'] = ''
        data['data_vencimento'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento foi removido do lancamento
        obj.refresh_from_db()
        self.assertIsNone(obj.movimento_caixa)

    def test_edit_recebimento_movimentar_caixa_false_get_post_request(self):
        # Buscar entrada com movimento de caixa e data_pagamento
        obj = Entrada.objects.filter(status='0', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | Q(
            data_pagamento__isnull=True) | Q(data_pagamento=datetime.strptime('06/07/2017', "%d/%m/%Y").date())).order_by('pk').last()
        url = reverse('djangosige.apps.financeiro:editarrecebimentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Recebimento editado'
        data['valor_total'] = locale.format(
            u'%.2f', Decimal(data['valor_total']), 1)
        data['valor_liquido'] = locale.format(
            u'%.2f', Decimal(data['valor_liquido']), 1)
        data['movimentar_caixa'] = False
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento foi removido do lancamento
        obj.refresh_from_db()
        self.assertIsNone(obj.movimento_caixa)

    def test_edit_recebimento_movimentar_caixa_true_get_post_request(self):
        # Criar lancamento com data futura (sem movimentos)
        data_pagamento_futura = datetime.strptime(
            '01/01/2099', "%d/%m/%Y").date()
        obj = Entrada.objects.create(status='0', movimentar_caixa=False, valor_total='120.00',
                                     valor_liquido='120.00', data_pagamento=data_pagamento_futura)
        url = reverse('djangosige.apps.financeiro:editarrecebimentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Recebimento editado'
        data['valor_total'] = locale.format(
            u'%.2f', Decimal(data['valor_total']), 1)
        data['valor_liquido'] = locale.format(
            u'%.2f', Decimal(data['valor_liquido']), 1)
        data['movimentar_caixa'] = True
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento foi criado corretamente
        movimento_editado = MovimentoCaixa.objects.get(
            data_movimento=data_pagamento_futura)
        self.assertEqual(movimento_editado.entradas, Decimal('120.00'))

    def test_edit_pagamento_com_data_pagamento_igual_get_post_request(self):
        # Buscar saida com movimento de caixa e data_pagamento
        # Nao modificar a data_pagamento atual, para buscar o mesmo movimento
        obj = Saida.objects.filter(status='0', movimentar_caixa=True).exclude(
            Q(movimento_caixa__isnull=True) | Q(data_pagamento__isnull=True)).order_by('pk').last()
        valor_saldo_final_antigo = obj.movimento_caixa.saldo_final
        data_movimento = obj.movimento_caixa.data_movimento
        url = reverse('djangosige.apps.financeiro:editarpagamentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Pagamento editado'
        data['valor_total'] = locale.format(u'%.2f', Decimal(
            data['valor_total']) + Decimal('20.00'), 1)
        data['valor_liquido'] = locale.format(u'%.2f', Decimal(
            data['valor_liquido']) + Decimal('20.00'), 1)
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento de caixa foi atualizado
        movimento_editado = MovimentoCaixa.objects.get(
            data_movimento=data_movimento)
        self.assertEqual(
            valor_saldo_final_antigo - Decimal('20.00'),
            movimento_editado.saldo_final
        )

    def test_edit_pagamento_com_data_pagamento_diferente_e_movimento_criado_get_post_request(self):
        # Buscar saida com movimento de caixa e data_pagamento
        # Modificar a data_pagamento atual, para buscar outro movimento ou
        # criar um novo
        obj = Saida.objects.filter(status='0', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | Q(
            data_pagamento__isnull=True) | Q(data_pagamento=datetime.strptime('06/07/2017', "%d/%m/%Y").date())).order_by('pk').last()
        # Data aleatoria, que nao possui movimentos de caixa
        nova_data_pagamento = datetime.strptime(
            '01/01/2030', "%d/%m/%Y").date()
        url = reverse('djangosige.apps.financeiro:editarpagamentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        novo_valor_saidas = Decimal(data['valor_liquido']) + Decimal('20.00')
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Pagamento editado'
        data['valor_total'] = locale.format(u'%.2f', Decimal(
            data['valor_total']) + Decimal('20.00'), 1)
        data['valor_liquido'] = locale.format(u'%.2f', Decimal(
            data['valor_liquido']) + Decimal('20.00'), 1)
        data['data_pagamento'] = nova_data_pagamento.strftime('%d/%m/%Y')
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento foi criado corretamente
        movimento_editado = MovimentoCaixa.objects.get(
            data_movimento=nova_data_pagamento)
        self.assertEqual(movimento_editado.saidas, novo_valor_saidas)

    def test_edit_pagamento_com_data_pagamento_diferente_e_movimento_existe_get_post_request(self):
        # Buscar saida com movimento de caixa e data_pagamento
        # Modificar a data_pagamento atual, para buscar outro movimento ou
        # criar um novo
        obj = Saida.objects.filter(status='0', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | Q(
            data_pagamento__isnull=True) | Q(data_pagamento=datetime.strptime('06/07/2017', "%d/%m/%Y").date())).order_by('pk').last()
        # Data que possui movimento de caixa
        nova_data_pagamento = datetime.strptime(
            '06/07/2017', "%d/%m/%Y").date()
        url = reverse('djangosige.apps.financeiro:editarpagamentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        novo_valor_saidas = MovimentoCaixa.objects.get(
            data_movimento=nova_data_pagamento).saidas + Decimal(data['valor_liquido']) + Decimal('20.00')
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Pagamento editado'
        data['valor_total'] = locale.format(u'%.2f', Decimal(
            data['valor_total']) + Decimal('20.00'), 1)
        data['valor_liquido'] = locale.format(u'%.2f', Decimal(
            data['valor_liquido']) + Decimal('20.00'), 1)
        data['data_pagamento'] = nova_data_pagamento.strftime('%d/%m/%Y')
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento foi editado corretamente
        movimento_editado = MovimentoCaixa.objects.get(
            data_movimento=nova_data_pagamento)
        self.assertEqual(movimento_editado.saidas, novo_valor_saidas)

    def test_edit_pagamento_sem_data_pagamento_vencimento_get_post_request(self):
        # Buscar saida com movimento de caixa e data_pagamento
        obj = Saida.objects.filter(status='0', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | Q(
            data_pagamento__isnull=True) | Q(data_pagamento=datetime.strptime('06/07/2017', "%d/%m/%Y").date())).order_by('pk').last()
        url = reverse('djangosige.apps.financeiro:editarpagamentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Pagamento editado'
        data['data_pagamento'] = ''
        data['data_vencimento'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento foi removido do lancamento
        obj.refresh_from_db()
        self.assertIsNone(obj.movimento_caixa)

    def test_edit_pagamento_movimentar_caixa_false_get_post_request(self):
        # Buscar saida com movimento de caixa e data_pagamento
        obj = Saida.objects.filter(status='0', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | Q(
            data_pagamento__isnull=True) | Q(data_pagamento=datetime.strptime('06/07/2017', "%d/%m/%Y").date())).order_by('pk').last()
        url = reverse('djangosige.apps.financeiro:editarpagamentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Pagamento editado'
        data['valor_total'] = locale.format(
            u'%.2f', Decimal(data['valor_total']), 1)
        data['valor_liquido'] = locale.format(
            u'%.2f', Decimal(data['valor_liquido']), 1)
        data['movimentar_caixa'] = False
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento foi removido do lancamento
        obj.refresh_from_db()
        self.assertIsNone(obj.movimento_caixa)

    def test_edit_pagamento_movimentar_caixa_true_get_post_request(self):
        # Criar lancamento com data futura (sem movimentos)
        data_pagamento_futura = datetime.strptime(
            '01/01/2020', "%d/%m/%Y").date()
        obj = Saida.objects.create(status='0', movimentar_caixa=False, valor_total='120.00',
                                   valor_liquido='120.00', data_pagamento=data_pagamento_futura)
        url = reverse('djangosige.apps.financeiro:editarpagamentoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Pagamento editado'
        data['valor_total'] = locale.format(
            u'%.2f', Decimal(data['valor_total']), 1)
        data['valor_liquido'] = locale.format(
            u'%.2f', Decimal(data['valor_liquido']), 1)
        data['movimentar_caixa'] = True
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'financeiro/lancamento/lancamento_list.html')

        # Verificar se movimento foi criado corretamente
        movimento_editado = MovimentoCaixa.objects.get(
            data_movimento=data_pagamento_futura)
        self.assertEqual(movimento_editado.saidas, Decimal('120.00'))


class FinanceiroGerarLancamentoViewTestCase(BaseTestCase):
    url = reverse('djangosige.apps.financeiro:gerarlancamento')

    def test_gerar_recebimento_a_partir_de_conta_receber_mesma_data_pagamento(self):
        # Buscar objeto qualquer
        obj = Entrada.objects.filter(status='1', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | (
            Q(data_pagamento__isnull=True) & Q(data_vencimento__isnull=True))).order_by('pk').last()
        if obj.data_pagamento:
            data_pagamento = obj.data_pagamento
        else:
            data_pagamento = obj.data_vencimento
        data = {'contaId': obj.pk, 'tipoConta': '0',
                'dataPagamento': data_pagamento.strftime('%d/%m/%Y')}
        response = self.client.post(self.url, data, follow=True)
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['url'], reverse(
            'djangosige.apps.financeiro:editarrecebimentoview', kwargs={'pk': obj.id}))

    def test_gerar_recebimento_a_partir_de_conta_receber_muda_data_pagamento(self):
        # Buscar objeto qualquer
        obj = Entrada.objects.filter(status='1', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | (
            Q(data_pagamento__isnull=True) & Q(data_vencimento__isnull=True))).order_by('pk').last()
        data_pagamento = datetime.strptime('01/01/2040', "%d/%m/%Y").date()
        data = {'contaId': obj.pk, 'tipoConta': '0',
                'dataPagamento': data_pagamento.strftime('%d/%m/%Y')}
        response = self.client.post(self.url, data, follow=True)
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['url'], reverse(
            'djangosige.apps.financeiro:editarrecebimentoview', kwargs={'pk': obj.id}))

        # Verficar que movimento foi criado
        movimento_criado = MovimentoCaixa.objects.get(
            data_movimento=data_pagamento)
        self.assertEqual(movimento_criado.entradas, obj.valor_liquido)

    def test_gerar_pagamento_a_partir_de_conta_pagar_mesma_data_pagamento(self):
        # Buscar objeto qualquer
        obj = Saida.objects.filter(status='1', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | (
            Q(data_pagamento__isnull=True) & Q(data_vencimento__isnull=True))).order_by('pk').last()
        if obj.data_pagamento:
            data_pagamento = obj.data_pagamento
        else:
            data_pagamento = obj.data_vencimento
        data = {'contaId': obj.pk, 'tipoConta': '1',
                'dataPagamento': data_pagamento.strftime('%d/%m/%Y')}
        response = self.client.post(self.url, data, follow=True)
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['url'], reverse(
            'djangosige.apps.financeiro:editarpagamentoview', kwargs={'pk': obj.id}))

    def test_gerar_pagamento_a_partir_de_conta_pagar_muda_data_pagamento(self):
        # Buscar objeto qualquer
        obj = Saida.objects.filter(status='1', movimentar_caixa=True).exclude(Q(movimento_caixa__isnull=True) | (
            Q(data_pagamento__isnull=True) & Q(data_vencimento__isnull=True))).order_by('pk').last()
        data_pagamento = datetime.strptime('01/01/2050', "%d/%m/%Y").date()
        data = {'contaId': obj.pk, 'tipoConta': '1',
                'dataPagamento': data_pagamento.strftime('%d/%m/%Y')}
        response = self.client.post(self.url, data, follow=True)
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['url'], reverse(
            'djangosige.apps.financeiro:editarpagamentoview', kwargs={'pk': obj.id}))

        # Verficar que movimento foi criado
        movimento_criado = MovimentoCaixa.objects.get(
            data_movimento=data_pagamento)
        self.assertEqual(movimento_criado.saidas, obj.valor_liquido)


class FinanceiroFaturarPedidoViewsTestCase(BaseTestCase):

    def test_faturar_pedido_venda(self):
        # Faturar pedido de venda aberto com produtos com estoque normal (id=4)
        # (adicionado por fixture)
        url = reverse('djangosige.apps.financeiro:faturarpedidovenda', kwargs={'pk': 4})
        response = self.client.get(url, follow=True, HTTP_REFERER=reverse(
            'djangosige.apps.financeiro:listalancamentoview'))
        self.assertEqual(response.status_code, 200)

        # Verificar se estoque dos produtos foi movimentado
        self.assertTrue(SaidaEstoque.objects.filter(
            observacoes='Saída de estoque pelo pedido de venda nº4').exists())

    def test_faturar_pedido_venda_com_produto_estoque_baixo(self):
        # Faturar pedido de venda aberto com produto com estoque baixo (id=5)
        # (adicionado por fixture)
        url = reverse('djangosige.apps.financeiro:faturarpedidovenda', kwargs={'pk': 5})
        response = self.client.get(url, follow=True, HTTP_REFERER=reverse(
            'djangosige.apps.financeiro:listalancamentoview'))
        self.assertEqual(response.status_code, 200)
        msgs = list(response.context['messages'])
        self.assertIn('Aviso: A venda não pode ser faturada', str(msgs[0]))

    def test_faturar_pedido_venda_com_produto_estoque_padrao_baixo(self):
        # Faturar pedido de venda aberto com produto com estoque baixo no local
        # Estoque Padrao (id=6) (adicionado por fixture)
        url = reverse('djangosige.apps.financeiro:faturarpedidovenda', kwargs={'pk': 6})
        response = self.client.get(url, follow=True, HTTP_REFERER=reverse(
            'djangosige.apps.financeiro:listalancamentoview'))
        self.assertEqual(response.status_code, 200)
        msgs = list(response.context['messages'])
        self.assertIn('Aviso: A venda não pode ser faturada', str(msgs[0]))

    def test_faturar_pedido_compra(self):
        # Faturar pedido de compra (id=5) (adicionado por fixture)
        url = reverse('djangosige.apps.financeiro:faturarpedidocompra', kwargs={'pk': 5})
        response = self.client.get(url, follow=True, HTTP_REFERER=reverse(
            'djangosige.apps.financeiro:listalancamentoview'))
        self.assertEqual(response.status_code, 200)
        msgs = list(response.context['messages'])
        self.assertIn('realizado com sucesso', str(msgs[0]))
