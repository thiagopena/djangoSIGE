# -*- coding: utf-8 -*-

from djangosige.tests.test_case import BaseTestCase, replace_none_values_in_dictionary
from django.urls import reverse
from django.utils import timezone

from djangosige.apps.fiscal.models import NaturezaOperacao, GrupoFiscal, NotaFiscalSaida, NotaFiscalEntrada
from djangosige.apps.vendas.models import PedidoVenda


AUT_XML_FORMSET_DATA = {
    'aut_form-0-cpf_cnpj': '',
    'aut_form-TOTAL_FORMS': 1,
    'aut_form-INITIAL_FORMS': 0,
}


class FiscalAdicionarViewsTestCase(BaseTestCase):

    def test_add_natureza_operacao_view_get_request(self):
        url = reverse('djangosige.apps.fiscal:addnaturezaoperacaoview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_grupo_fiscal_view_get_request(self):
        url = reverse('djangosige.apps.fiscal:addgrupofiscalview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_nota_fiscal_saida_view_get_request(self):
        url = reverse('djangosige.apps.fiscal:addnotafiscalsaidaview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_natureza_operacao_view_post_request(self):
        url = reverse('djangosige.apps.fiscal:addnaturezaoperacaoview')

        data = {
            'cfop': '1116',
            'descricao': 'Compra p/ industrialização ou produção rural originada de encomenda p/ recebimento futuro',
            'tp_operacao': '0',
            'id_dest': '1',
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'fiscal/natureza_operacao/natureza_operacao_list.html')

        # Assert form invalido
        data['cfop'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'cfop', 'Este campo é obrigatório.')

    def test_add_grupo_fiscal_view_post_request(self):
        url = reverse('djangosige.apps.fiscal:addgrupofiscalview')

        data = {
            'descricao': 'Grupo Fiscal Teste1',
            'regime_trib': '1',  # Simples
            'icmssn_form-csosn': '102',  # Tributada sem permissao de credito
            'icmssn_form-mod_bcst': '4',
            'icmssn_form-mod_bc': '3',
            'ipi_form-cst': '02',  # Entrada isenta
            'ipi_form-tipo_ipi': '0',  # Nao sujeito ao IPI
            'pis_form-cst': '07',  # Operacao isenta da contribuicao
            'cofins_form-cst': '07',  # Operacao isenta da contribuicao
            'icms_dest_form-p_fcp_dest': '2',
            'icms_dest_form-p_icms_dest': '18',
            'icms_dest_form-p_icms_inter': '7.00',
            'icms_dest_form-p_icms_inter_part': '60.00',
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'fiscal/grupo_fiscal/grupo_fiscal_list.html')

        # Assert form invalido
        data['descricao'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'descricao', 'Este campo é obrigatório.')

    def test_add_nota_fiscal_saida_view_post_request(self):
        url = reverse('djangosige.apps.fiscal:addnotafiscalsaidaview')
        dhatual = timezone.now().strftime('%d/%m/%Y %H:%M')

        data = {
            'versao': '4.00',
            'natop': 'Natureza qualquer',
            'indpag': '0',
            'mod': '55',
            'serie': '101',
            'dhemi': dhatual,
            'dhsaient': dhatual,
            'iddest': '1',
            'tp_imp': '1',
            'tp_emis': '1',
            'tp_amb': '2',
            'fin_nfe': '1',
            'ind_final': '0',
            'ind_pres': '0',
            'status_nfe': '3',
            'tpnf': '1',
            'n_nf_saida': '333333333',
        }

        data.update(AUT_XML_FORMSET_DATA)

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'fiscal/nota_fiscal/nota_fiscal_list.html')

        # Assert form invalido
        data['versao'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'versao', 'Este campo é obrigatório.')

    def test_gerar_nota_fiscal_saida_por_pedido_venda(self):
        # Buscar objeto qualquer
        obj = PedidoVenda.objects.order_by('pk').last()
        url = reverse('djangosige.apps.fiscal:gerarnotafiscalsaida',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context[
                        'object'], NotaFiscalSaida))


class FiscalListarViewsTestCase(BaseTestCase):

    def test_list_natureza_operacao_view_deletar_objeto(self):
        obj = NaturezaOperacao.objects.create(cfop='9999')
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.fiscal:listanaturezaoperacaoview'), deleted_object=obj)

    def test_list_grupo_fiscal_view_deletar_objeto(self):
        obj = GrupoFiscal.objects.create(
            descricao='Grupo Fiscal Delete Teste', regime_trib='0')
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.fiscal:listagrupofiscalview'), deleted_object=obj)

    def test_list_nota_fiscal_saida_view_deletar_objeto(self):
        obj = NotaFiscalSaida.objects.create(dhemi=timezone.now())
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.fiscal:listanotafiscalsaidaview'), deleted_object=obj)

    def test_list_nota_fiscal_entrada_view_deletar_objeto(self):
        obj = NotaFiscalEntrada.objects.create(dhemi=timezone.now())
        self.check_list_view_delete(url=reverse(
            'djangosige.apps.fiscal:listanotafiscalentradaview'), deleted_object=obj)


class FiscalEditarViewsTestCase(BaseTestCase):

    def test_edit_natureza_operacao_get_post_request(self):
        # Buscar objeto qualquer
        obj = NaturezaOperacao.objects.order_by('pk').last()
        url = reverse('djangosige.apps.fiscal:editarnaturezaoperacaoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['descricao'] = 'Natureza Operacao Editada.'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'fiscal/natureza_operacao/natureza_operacao_list.html')

    def test_edit_grupo_fiscal_get_post_request(self):
        # Buscar objeto qualquer
        obj = GrupoFiscal.objects.order_by('pk').last()
        url = reverse('djangosige.apps.fiscal:editargrupofiscalview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        if response.context['icms_form'].initial:
            data['icms_form-mod_bc'] = response.context['icms_form'].initial['mod_bc']
            data['icms_form-mod_bcst'] = response.context['icms_form'].initial['mod_bcst']
        elif response.context['icmssn_form'].initial:
            data['icmssn_form-mod_bc'] = response.context['icmssn_form'].initial['mod_bc']
            data[
                'icmssn_form-mod_bcst'] = response.context['icmssn_form'].initial['mod_bcst']
        data['ipi_form-tipo_ipi'] = response.context['ipi_form'].initial['tipo_ipi']
        data['descricao'] = 'Grupo Fiscal Editado.'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'fiscal/grupo_fiscal/grupo_fiscal_list.html')

    def test_edit_nota_fiscal_saida_get_post_request(self):
        # Buscar objeto qualquer
        obj = NotaFiscalSaida.objects.order_by('pk').last()
        url = reverse('djangosige.apps.fiscal:editarnotafiscalsaidaview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        data.update(AUT_XML_FORMSET_DATA)
        data['dhemi'] = timezone.now().strftime('%d/%m/%Y %H:%M')
        data['natop'] = data['natop'] + ' (Nota fiscal editada)'
        replace_none_values_in_dictionary(data)
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'fiscal/nota_fiscal/nota_fiscal_list.html')

        # Assert form invalido
        data['natop'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'natop', 'Este campo é obrigatório.')

    def test_edit_nota_fiscal_entrada_get_post_request(self):
        # Buscar objeto qualquer
        obj = NotaFiscalEntrada.objects.order_by('pk').last()
        url = reverse('djangosige.apps.fiscal:editarnotafiscalentradaview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        data['dhemi'] = timezone.now().strftime('%d/%m/%Y %H:%M')
        data['natop'] = data['natop'] + ' (Nota fiscal editada)'
        replace_none_values_in_dictionary(data)
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'fiscal/nota_fiscal/nota_fiscal_list.html')

        # Assert form invalido
        data['natop'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'natop', 'Este campo é obrigatório.')


class FiscalConfiguracaoNotaFiscalViewTestCase(BaseTestCase):
    url = reverse('djangosige.apps.fiscal:configuracaonotafiscal')

    def test_configuracao_nfe_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Testar permissao
        permission_codename = 'configurar_nfe'
        self.check_user_get_permission(
            self.url, permission_codename=permission_codename)
