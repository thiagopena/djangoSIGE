# -*- coding: utf-8 -*-

from djangosige.apps.compras.models import ItensCompra, Pagamento
from djangosige.apps.vendas.views.report_vendas import VendaReport, REPORT_FONT_BOLD, REPORT_FONT, DadosProdutos, DadosPagamento

from geraldo import ReportBand
from geraldo.widgets import ObjectValue
from reportlab.lib.units import cm


class CompraReport(VendaReport):

    def __init__(self, *args, **kargs):
        super(CompraReport, self).__init__(*args, **kargs)
        self.title = 'Relatorio de compra'

        self.dados_fornecedor = DadosFornecedor()
        self.dados_produtos = DadosProdutosCompra()
        self.dados_pagamento = DadosPagamentoCompra()


class DadosFornecedor(ReportBand):

    def __init__(self):
        super(DadosFornecedor, self).__init__()
        self.ender_info = False
        self.elements = []
        txt = ObjectValue(attribute_name='fornecedor.nome_razao_social',
                          top=0.3 * cm, left=0.3 * cm, width=8 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 12, 'leading': 12}
        self.elements.append(txt)

        self.height = 2.7 * cm

    def inserir_informacoes_pj(self):
        txt = ObjectValue(attribute_name='fornecedor.pessoa_jur_info.format_cnpj',
                          top=0.3 * cm, left=8.1 * cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='fornecedor.pessoa_jur_info.format_ie',
                          top=0.3 * cm, left=13 * cm, width=6.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

    def inserir_informacoes_pf(self):
        txt = ObjectValue(attribute_name='fornecedor.pessoa_fis_info.format_cpf',
                          top=0.3 * cm, left=8.1 * cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='fornecedor.pessoa_fis_info.format_rg',
                          top=0.3 * cm, left=13 * cm, width=6.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

    def inserir_informacoes_endereco(self):
        self.ender_info = True
        txt = ObjectValue(attribute_name='fornecedor.endereco_padrao.format_endereco',
                          display_format='Endereço: %s', top=1.1 * cm, left=0.3 * cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='fornecedor.endereco_padrao.municipio',
                          display_format='Cidade: %s', top=1.6 * cm, left=0.3 * cm, width=8 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='fornecedor.endereco_padrao.uf',
                          display_format='UF: %s', top=1.6 * cm, left=8.1 * cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='fornecedor.endereco_padrao.cep', display_format='CEP: %s',
                          top=1.6 * cm, left=13 * cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

    def inserir_informacoes_telefone(self):
        if not self.ender_info:
            top = 1.1 * cm
        else:
            top = 2.1 * cm

        txt = ObjectValue(attribute_name='fornecedor.telefone_padrao.telefone',
                          display_format='Tel: %s', top=top, left=0.3 * cm, width=8 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

    def inserir_informacoes_email(self):
        if not self.ender_info:
            top = 1.1 * cm
        else:
            top = 2.1 * cm

        txt = ObjectValue(attribute_name='fornecedor.email_padrao.email',
                          display_format='Email: %s', top=top, left=8.1 * cm, width=11.3 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)


class DadosProdutosCompra(DadosProdutos):

    def __init__(self):
        super(DadosProdutosCompra, self).__init__()
        self.get_queryset = lambda self, parent_object: ItensCompra.objects.filter(
            compra_id=parent_object) or []


class DadosPagamentoCompra(DadosPagamento):

    def __init__(self):
        super(DadosPagamento, self).__init__()
        self.get_queryset = lambda self, parent_object: Pagamento.objects.filter(
            compra_id=parent_object) or []
