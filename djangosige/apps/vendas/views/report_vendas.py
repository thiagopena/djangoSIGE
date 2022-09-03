# -*- coding: utf-8 -*-

from djangosige.apps.vendas.models import ItensVenda, Pagamento

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from geraldo import Report, ReportBand, SubReport
from geraldo.widgets import Label, SystemField, ObjectValue
from geraldo.graphics import Image, Line
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

REPORT_FONT = 'Times'
REPORT_FONT_BOLD = REPORT_FONT + '-Bold'


class VendaReport(Report):

    def __init__(self, *args, **kargs):
        super(VendaReport, self).__init__(*args, **kargs)
        self.title = 'Relatorio de venda'

        self.page_size = A4
        self.margin_left = 0.8 * cm
        self.margin_top = 0.8 * cm
        self.margin_right = 0.8 * cm
        self.margin_bottom = 0.8 * cm

        self.topo_pagina = TopoPagina()
        self.dados_cliente = DadosCliente()
        self.banda_produtos = BandaProdutos()
        self.dados_produtos = DadosProdutos()
        self.totais_venda = TotaisVenda()
        self.banda_pagamento = BandaPagamento()
        self.dados_pagamento = DadosPagamento()
        self.observacoes = Observacoes()
        self.banda_foot = BandaFoot()


class TopoPagina(ReportBand):

    def __init__(self):
        super(TopoPagina, self).__init__()
        self.elements = []
        txt = SystemField(expression='%(report_title)s', top=0.65 *
                          cm, left=0 * cm, width=19.4 * cm, height=0.8 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 15, 'alignment': TA_CENTER, 'leading': 15}
        self.elements.append(txt)

        txt = SystemField(expression='Página %(page_number)s de %(last_page_number)s',
                          top=4.0 * cm, left=0 * cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 8.5,
                     'alignment': TA_RIGHT, 'leading': 8.5}
        self.elements.append(txt)

        self.elements.append(Line(top=3.6 * cm, bottom=3.6 *
                                  cm, left=0 * cm, right=19.4 * cm, stroke_width=0.3))

        self.height = 3.65 * cm

    def inserir_data_emissao(self, data_emissao):
        if data_emissao:
            txt = ObjectValue(attribute_name='format_data_emissao', display_format='Data: %s',
                              top=1.45 * cm, left=0 * cm, width=19.4 * cm, height=0.5 * cm)
        else:
            txt = SystemField(expression='Data: %(now:%d/%m/%Y)s',
                              top=1.45 * cm, left=0 * cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 9, 'alignment': TA_CENTER, 'leading': 9}
        self.elements.append(txt)

    def inserir_data_validade(self, data_validade):
        if data_validade:
            txt = ObjectValue(attribute_name='format_data_vencimento', display_format='Válido até: %s',
                              top=2.05 * cm, left=0 * cm, width=19.4 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'fontSize': 9, 'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)

    def inserir_data_entrega(self, data_entrega):
        if data_entrega:
            txt = ObjectValue(attribute_name='format_data_entrega', display_format='Data de entrega: %s',
                              top=2.05 * cm, left=0 * cm, width=19.4 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'fontSize': 9, 'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)

    def inserir_logo(self, path_imagem):
        logo = Image(left=0.5 * cm, top=0.3 * cm, right=10 * cm, bottom=0.5 *
                     cm, width=5.5 * cm, height=5.5 * cm, filename=path_imagem)
        self.elements.append(logo)


class DadosCliente(ReportBand):

    def __init__(self):
        super(DadosCliente, self).__init__()
        self.ender_info = False
        self.elements = []
        txt = ObjectValue(attribute_name='cliente.nome_razao_social',
                          top=0.3 * cm, left=0.3 * cm, width=8 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 12, 'leading': 12}
        self.elements.append(txt)

        self.height = 2.7 * cm

    def inserir_informacoes_pj(self):
        txt = ObjectValue(attribute_name='cliente.pessoa_jur_info.format_cnpj',
                          top=0.3 * cm, left=8.1 * cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='cliente.pessoa_jur_info.format_ie',
                          top=0.3 * cm, left=13 * cm, width=6.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

    def inserir_informacoes_pf(self):
        txt = ObjectValue(attribute_name='cliente.pessoa_fis_info.format_cpf',
                          top=0.3 * cm, left=8.1 * cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='cliente.pessoa_fis_info.format_rg',
                          top=0.3 * cm, left=13 * cm, width=6.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

    def inserir_informacoes_endereco(self):
        self.ender_info = True
        txt = ObjectValue(attribute_name='cliente.endereco_padrao.format_endereco',
                          display_format='Endereço: %s', top=1.1 * cm, left=0.3 * cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='cliente.endereco_padrao.municipio',
                          display_format='Cidade: %s', top=1.6 * cm, left=0.3 * cm, width=8 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='cliente.endereco_padrao.uf', display_format='UF: %s',
                          top=1.6 * cm, left=8.1 * cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='cliente.endereco_padrao.cep', display_format='CEP: %s',
                          top=1.6 * cm, left=13 * cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

    def inserir_informacoes_telefone(self):
        if not self.ender_info:
            top = 1.1 * cm
        else:
            top = 2.1 * cm

        txt = ObjectValue(attribute_name='cliente.telefone_padrao.telefone',
                          display_format='Tel: %s', top=top, left=0.3 * cm, width=8 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)

    def inserir_informacoes_email(self):
        if not self.ender_info:
            top = 1.1 * cm
        else:
            top = 2.1 * cm

        txt = ObjectValue(attribute_name='cliente.email_padrao.email', display_format='Email: %s',
                          top=top, left=8.1 * cm, width=11.3 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10, 'leading': 10}
        self.elements.append(txt)


class BandaProdutos(ReportBand):

    def __init__(self):
        super(BandaProdutos, self).__init__()
        self.elements = []

        self.height = 0 * cm


class DadosProdutos(SubReport):

    def __init__(self):
        super(DadosProdutos, self).__init__()
        self.get_queryset = lambda self, parent_object: ItensVenda.objects.filter(
            venda_id=parent_object) or []

    class band_header(ReportBand):

        def __init__(self):
            super(DadosProdutos.band_header, self).__init__()
            self.elements = []

            self.elements.append(Line(
                top=0.1 * cm, bottom=0.1 * cm, left=0 * cm, right=19.4 * cm, stroke_width=0.3))

            txt = Label(text='Produtos', top=0.2 * cm, left=0 *
                        cm, width=19.4 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'fontSize': 11, 'alignment': TA_CENTER, 'leading': 11}
            self.elements.append(txt)

            txt = Label(text='Cód.', top=1.1 * cm, left=0 *
                        cm, width=2.1 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'alignment': TA_CENTER, 'fontSize': 9, 'leading': 9}
            self.elements.append(txt)
            txt = Label(text='Descrição', top=1.1 * cm, left=2.1 *
                        cm, width=4.8 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'fontSize': 9, 'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = Label(text='Un.', top=1.1 * cm, left=6.9 *
                        cm, width=1.5 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'fontSize': 9, 'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = Label(text='Qtde.', top=1.1 * cm, left=8.4 *
                        cm, width=1.9 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'fontSize': 9, 'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = Label(text='Vl. Unit. (R$)', top=1.1 * cm,
                        left=10.3 * cm, width=3.5 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'fontSize': 9, 'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = Label(text='Desconto (R$)', top=1.1 * cm,
                        left=13.8 * cm, width=2.4 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'fontSize': 9, 'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = Label(text='Total (R$)', top=1.1 * cm,
                        left=16.2 * cm, width=3.2 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'fontSize': 9, 'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)

            self.height = 1.8 * cm

    class band_detail(ReportBand):

        def __init__(self):
            super(DadosProdutos.band_detail, self).__init__()

            txt = ObjectValue(attribute_name='produto.codigo', top=0 *
                              cm, left=0 * cm, width=2.1 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                         'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = ObjectValue(attribute_name='produto.descricao', top=0 *
                              cm, left=2.1 * cm, width=4.8 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                         'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = ObjectValue(attribute_name='produto.format_unidade',
                              top=0 * cm, left=6.9 * cm, width=1.5 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                         'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = ObjectValue(attribute_name='format_quantidade', top=0 *
                              cm, left=8.4 * cm, width=1.9 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                         'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = ObjectValue(attribute_name='format_valor_unit', top=0 *
                              cm, left=10.3 * cm, width=3.5 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                         'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = ObjectValue(attribute_name='format_desconto', top=0 *
                              cm, left=13.8 * cm, width=2.4 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                         'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = ObjectValue(attribute_name='format_total', top=0 *
                              cm, left=16.2 * cm, width=3.2 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                         'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)

        def set_band_height(self, n_produtos):
            self.height = 0.4 * cm * n_produtos


class TotaisVenda(ReportBand):

    def __init__(self):
        super(TotaisVenda, self).__init__()
        self.elements = []
        self.elements.append(Line(top=0.1 * cm, bottom=0.1 *
                                  cm, left=0 * cm, right=19.4 * cm, stroke_width=0.3))

        txt = Label(text='Totais', top=0.2 * cm, left=0 *
                    cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 11, 'alignment': TA_CENTER, 'leading': 11}
        self.elements.append(txt)

        txt = Label(text='Frete', top=1 * cm, left=0 *
                    cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'alignment': TA_CENTER, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='format_frete', display_format='R$ %s',
                          top=1.5 * cm, left=0 * cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10,
                     'alignment': TA_CENTER, 'leading': 10}
        self.elements.append(txt)

        txt = Label(text='Seguro', top=1 * cm, left=4 *
                    cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'alignment': TA_CENTER, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='format_seguro', display_format='R$ %s',
                          top=1.5 * cm, left=4 * cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10,
                     'alignment': TA_CENTER, 'leading': 10}
        self.elements.append(txt)

        txt = Label(text='Despesas', top=1 * cm, left=8 *
                    cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'alignment': TA_CENTER, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='format_despesas', display_format='R$ %s',
                          top=1.5 * cm, left=8 * cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10,
                     'alignment': TA_CENTER, 'leading': 10}
        self.elements.append(txt)

        txt = Label(text='Desconto', top=1 * cm, left=12 *
                    cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'alignment': TA_CENTER, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='format_desconto', display_format='R$ %s',
                          top=1.5 * cm, left=12 * cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10,
                     'alignment': TA_CENTER, 'leading': 10}
        self.elements.append(txt)

        txt = Label(text='Impostos', top=1 * cm, left=16 *
                    cm, width=3.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'alignment': TA_CENTER, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='format_impostos', display_format='R$ %s',
                          top=1.5 * cm, left=16 * cm, width=3.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10,
                     'alignment': TA_CENTER, 'leading': 10}
        self.elements.append(txt)

        # Totais
        self.elements.append(Line(top=2.3 * cm, bottom=2.3 *
                                  cm, left=0.4 * cm, right=19 * cm, stroke_width=0.3))
        txt = Label(text='Total sem impostos:', top=2.4 * cm,
                    left=0 * cm, width=13.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'alignment': TA_RIGHT, 'leading': 10}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='format_total_sem_imposto', display_format='R$ %s',
                          top=2.4 * cm, left=13.4 * cm, width=5.6 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 10,
                     'alignment': TA_RIGHT, 'leading': 10}
        self.elements.append(txt)

        self.elements.append(Line(top=2.9 * cm, bottom=2.9 *
                                  cm, left=9.7 * cm, right=19 * cm, stroke_width=0.3))
        txt = Label(text='Total:', top=3 * cm, left=0 *
                    cm, width=13.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 11, 'alignment': TA_RIGHT, 'leading': 11}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='format_valor_total', display_format='R$ %s',
                          top=3 * cm, left=13.4 * cm, width=5.6 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 10, 'alignment': TA_RIGHT, 'leading': 10}
        self.elements.append(txt)

        self.height = 3.6 * cm


class BandaPagamento(ReportBand):

    def __init__(self):
        super(BandaPagamento, self).__init__()
        self.elements = []

        self.elements.append(Line(top=0.1 * cm, bottom=0.1 *
                                  cm, left=0 * cm, right=19.4 * cm, stroke_width=0.3))

        txt = Label(text='Pagamento', top=0.2 * cm, left=0 *
                    cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 11, 'alignment': TA_CENTER, 'leading': 11}
        self.elements.append(txt)

        # Condicao de pagamento
        txt = ObjectValue(attribute_name='cond_pagamento.get_forma_display',
                          display_format='Forma: %s', top=1 * cm, left=0.5 * cm, width=4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 9, 'leading': 9}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='cond_pagamento.n_parcelas',
                          display_format='Nº de parcelas: %s', top=1 * cm, left=5 * cm, width=3 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 9, 'leading': 9}
        self.elements.append(txt)

        self.height = 2 * cm


class DadosPagamento(SubReport):

    def __init__(self):
        super(DadosPagamento, self).__init__()
        self.get_queryset = lambda self, parent_object: Pagamento.objects.filter(
            venda_id=parent_object) or []

    class band_header(ReportBand):

        def __init__(self):
            super(DadosPagamento.band_header, self).__init__()
            self.elements = []

            txt = Label(text='Parcela', top=2 * cm, left=0 *
                        cm, width=4 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'alignment': TA_CENTER, 'fontSize': 10, 'leading': 10}
            self.elements.append(txt)

            txt = Label(text='Vencimento', top=2 * cm, left=4.1 *
                        cm, width=4.1 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'alignment': TA_CENTER, 'fontSize': 10, 'leading': 10}
            self.elements.append(txt)

            txt = Label(text='Valor', top=2 * cm, left=8.3 *
                        cm, width=4.5 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT_BOLD,
                         'alignment': TA_CENTER, 'fontSize': 10, 'leading': 10}
            self.elements.append(txt)

            self.height = 2.7 * cm

    class band_detail(ReportBand):

        def __init__(self):
            super(DadosPagamento.band_detail, self).__init__()

            txt = ObjectValue(attribute_name='indice_parcela',
                              top=0 * cm, left=0 * cm, width=4 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                         'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = ObjectValue(attribute_name='format_vencimento', top=0 *
                              cm, left=4.1 * cm, width=4.1 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                         'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)
            txt = ObjectValue(attribute_name='format_valor_parcela',
                              top=0 * cm, left=8.3 * cm, width=4.5 * cm, height=0.5 * cm)
            txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                         'alignment': TA_CENTER, 'leading': 9}
            self.elements.append(txt)

            self.height = 0.6 * cm

        def set_band_height(self, n_produtos):
            self.height = 0.4 * cm * n_produtos


class Observacoes(ReportBand):

    def __init__(self):
        super(Observacoes, self).__init__()
        self.elements = []

        self.elements.append(Line(top=0.1 * cm, bottom=0.1 *
                                  cm, left=0 * cm, right=19.4 * cm, stroke_width=0.3))

        txt = Label(text='Observações', top=0.2 * cm, left=0 *
                    cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 11, 'alignment': TA_CENTER, 'leading': 11}
        self.elements.append(txt)

        txt = ObjectValue(attribute_name='observacoes', top=0.8 *
                          cm, left=0.5 * cm, width=19.4 * cm, height=2 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 9, 'leading': 9}
        self.elements.append(txt)

        self.height = 2 * cm

    def inserir_vendedor(self):
        self.elements.append(Line(top=2.5 * cm, bottom=2.5 *
                                  cm, left=0 * cm, right=19.4 * cm, stroke_width=0.3))

        txt = ObjectValue(attribute_name='vendedor', display_format='Vendedor: %s',
                          top=2.6 * cm, left=0.5 * cm, width=19.4 * cm, height=2 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 9, 'leading': 9}
        self.elements.append(txt)


class BandaFoot(ReportBand):

    def __init__(self):
        super(BandaFoot, self).__init__()
        self.ender_info = False
        self.elements = []

        self.elements.append(Line(top=1.5 * cm, bottom=1.5 *
                                  cm, left=0 * cm, right=19.4 * cm, stroke_width=0.3))

        txt = Label(text='Gerado por djangoSIGE', top=1.5 * cm,
                    left=0 * cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT_BOLD,
                     'fontSize': 8, 'alignment': TA_LEFT, 'leading': 8}
        self.elements.append(txt)

        txt = SystemField(expression='Data da impressão: %(now:%d/%m/%Y)s',
                          top=1.5 * cm, left=0 * cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 8,
                     'alignment': TA_RIGHT, 'leading': 8}
        self.elements.append(txt)

        self.height = 2 * cm

    def inserir_nome_empresa(self, nome):
        txt = Label(text=nome, top=0 * cm, left=0 * cm,
                    width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                     'alignment': TA_CENTER, 'leading': 9}
        self.elements.append(txt)

    def inserir_endereco_empresa(self, endereco):
        self.ender_info = True
        txt = Label(text=endereco, top=0.5 * cm, left=0 *
                    cm, width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                     'alignment': TA_CENTER, 'leading': 9}
        self.elements.append(txt)

    def inserir_telefone_empresa(self, telefone):
        if self.ender_info:
            top = 1 * cm
        else:
            top = 0.5 * cm

        txt = Label(text=telefone, top=top, left=0 * cm,
                    width=19.4 * cm, height=0.5 * cm)
        txt.style = {'fontName': REPORT_FONT, 'fontSize': 9,
                     'alignment': TA_CENTER, 'leading': 9}
        self.elements.append(txt)
