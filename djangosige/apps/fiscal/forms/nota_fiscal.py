# -*- coding: utf-8 -*-

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from djangosige.apps.fiscal.models import NotaFiscalSaida, NotaFiscalEntrada, AutXML, ConfiguracaoNotaFiscal, TP_AMB_ESCOLHAS, MOD_NFE_ESCOLHAS
from djangosige.apps.cadastro.models import Empresa

try:
    from pysignfe.nfe.manifestacao_destinatario import MD_CONFIRMACAO_OPERACAO, MD_DESCONHECIMENTO_OPERACAO, MD_OPERACAO_NAO_REALIZADA, MD_CIENCIA_OPERACAO
except ImportError:
    MD_CONFIRMACAO_OPERACAO = u'210200'
    MD_DESCONHECIMENTO_OPERACAO = u'210220'
    MD_OPERACAO_NAO_REALIZADA = u'210240'
    MD_CIENCIA_OPERACAO = u'210210'

TP_MANIFESTO_OPCOES = (
    (MD_CONFIRMACAO_OPERACAO, u'Confirmação da Operação'),
    (MD_DESCONHECIMENTO_OPERACAO, u'Desconhecimento da Operação'),
    (MD_OPERACAO_NAO_REALIZADA, u'Operação Não Realizada'),
    (MD_CIENCIA_OPERACAO, u'Ciência da Emissão (ou Ciência da Operação)'),
)


class NotaFiscalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NotaFiscalForm, self).__init__(*args, **kwargs)
        self.fields['dhemi'].input_formats = ('%d/%m/%Y %H:%M',)

    class Meta:
        fields = ('versao', 'status_nfe', 'natop', 'indpag', 'mod', 'serie', 'dhemi', 'dhsaient', 'iddest',
                  'tp_imp', 'tp_emis', 'tp_amb', 'fin_nfe', 'ind_final', 'ind_pres', 'inf_ad_fisco', 'inf_cpl',)

        widgets = {
            'versao': forms.Select(attrs={'class': 'form-control'}),
            'status_nfe': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'natop': forms.TextInput(attrs={'class': 'form-control'}),
            'indpag': forms.Select(attrs={'class': 'form-control'}),
            'mod': forms.Select(attrs={'class': 'form-control'}),
            'serie': forms.TextInput(attrs={'class': 'form-control'}),
            'dhemi': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}, format='%d/%m/%Y %H:%M'),
            'dhsaient': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}, format='%d/%m/%Y %H:%M'),
            'iddest': forms.Select(attrs={'class': 'form-control'}),
            'tp_imp': forms.Select(attrs={'class': 'form-control'}),
            'tp_emis': forms.Select(attrs={'class': 'form-control'}),
            'tp_amb': forms.Select(attrs={'class': 'form-control'}),
            'fin_nfe': forms.Select(attrs={'class': 'form-control'}),
            'ind_final': forms.Select(attrs={'class': 'form-control'}),
            'ind_pres': forms.Select(attrs={'class': 'form-control'}),
            'inf_ad_fisco': forms.Textarea(attrs={'class': 'form-control'}),
            'inf_cpl': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'versao': _('Versão'),
            'status_nfe': _('Status'),
            'natop': _('Natureza da Operação'),
            'indpag': _('Forma de pagamento'),
            'mod': _('Modelo'),
            'serie': _('Série'),
            'dhemi': _('Data e hora de emissão'),
            'dhsaient': _('Data e hora de Saída/Entrada'),
            'iddest': _('Destino da operação'),
            'tp_imp': _('Tipo impressão da DANFE'),
            'tp_emis': _('Forma de emissão'),
            'tp_amb': _('Ambiente'),
            'fin_nfe': _('Finalidade da emissão'),
            'ind_final': _('Consumidor final'),
            'ind_pres': _('Tipo de atendimento'),
            'inf_ad_fisco': _('Informações Adicionais de Interesse do Fisco'),
            'inf_cpl': _('Informações Complementares de interesse do Contribuinte'),
        }

        error_messages = {
            'n_nf': {
                'unique': _("Nota fiscal com este número já existe"),
            },
        }


class NotaFiscalSaidaForm(NotaFiscalForm):

    def __init__(self, *args, **kwargs):
        super(NotaFiscalSaidaForm, self).__init__(*args, **kwargs)
        self.fields['v_orig'].localize = True
        self.fields['v_desc'].localize = True
        self.fields['v_liq'].localize = True

    class Meta(NotaFiscalForm.Meta):
        model = NotaFiscalSaida
        fields = NotaFiscalForm.Meta.fields + ('n_nf_saida', 'tpnf', 'venda', 'emit_saida',
                                               'dest_saida', 'n_fat', 'v_orig', 'v_desc', 'v_liq', 'grupo_cobr', 'arquivo_proc',)
        widgets = NotaFiscalForm.Meta.widgets
        widgets['n_nf_saida'] = forms.TextInput(
            attrs={'class': 'form-control'})
        widgets['venda'] = forms.Select(attrs={'class': 'form-control'})
        widgets['emit_saida'] = forms.Select(attrs={'class': 'form-control'})
        widgets['dest_saida'] = forms.Select(attrs={'class': 'form-control'})
        widgets['n_fat'] = forms.TextInput(attrs={'class': 'form-control'})
        widgets['tpnf'] = forms.Select(attrs={'class': 'form-control'})
        widgets['v_orig'] = forms.TextInput(
            attrs={'class': 'form-control decimal-mask'})
        widgets['v_desc'] = forms.TextInput(
            attrs={'class': 'form-control decimal-mask'})
        widgets['v_liq'] = forms.TextInput(
            attrs={'class': 'form-control decimal-mask'})
        widgets['grupo_cobr'] = forms.CheckboxInput(
            attrs={'class': 'form-control'})
        widgets['arquivo_proc'] = forms.FileInput(
            attrs={'class': 'form-control'})
        labels = NotaFiscalForm.Meta.labels
        labels['n_nf_saida'] = _('Número')
        labels['venda'] = _('Venda')
        labels['emit_saida'] = _('Emitente (Empresa)')
        labels['dest_saida'] = _('Destinatário (Cliente)')
        labels['n_fat'] = _('Número da fatura')
        labels['tpnf'] = _('Tipo de Operação')
        labels['v_orig'] = _('Valor original da fatura')
        labels['v_desc'] = _('Valor do desconto')
        labels['v_liq'] = _('Valor líquido da fatura')
        labels['grupo_cobr'] = _(
            'Inserir dados de cobrança (Fatura/Duplicatas) na NF-e?')
        labels['arquivo_proc'] = _('Arquivo de processamento (*_procNFe.xml)')


class NotaFiscalEntradaForm(NotaFiscalForm):

    class Meta(NotaFiscalForm.Meta):
        model = NotaFiscalEntrada
        fields = NotaFiscalForm.Meta.fields + \
            ('n_nf_entrada', 'compra', 'emit_entrada', 'dest_entrada',)
        widgets = NotaFiscalForm.Meta.widgets
        widgets['n_nf_entrada'] = forms.TextInput(
            attrs={'class': 'form-control'})
        widgets['compra'] = forms.Select(attrs={'class': 'form-control'})
        widgets['emit_entrada'] = forms.Select(attrs={'class': 'form-control'})
        widgets['dest_entrada'] = forms.Select(attrs={'class': 'form-control'})
        labels = NotaFiscalForm.Meta.labels
        labels['n_nf_entrada'] = _('Número')
        labels['compra'] = _('Compra')
        labels['emit_entrada'] = _('Emitente (Fornecedor)')
        labels['dest_entrada'] = _('Destinatário (Empresa)')


class EmissaoNotaFiscalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmissaoNotaFiscalForm, self).__init__(*args, **kwargs)
        self.fields['dhemi'].input_formats = ('%d/%m/%Y %H:%M',)

    class Meta:
        model = NotaFiscalSaida
        fields = ('versao', 'dhemi', 'dhsaient',
                  'tp_imp', 'tp_emis', 'tp_amb',)

        widgets = {
            'versao': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'dhemi': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker', 'required': True}, format='%d/%m/%Y %H:%M'),
            'dhsaient': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}, format='%d/%m/%Y %H:%M'),
            'tp_imp': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'tp_emis': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'tp_amb': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
        labels = {
            'versao': _('Versão'),
            'dhemi': _('Data e hora de emissão'),
            'dhsaient': _('Data e hora de Saída/Entrada'),
            'tp_imp': _('Tipo impressão da DANFE'),
            'tp_emis': _('Forma de emissão'),
            'tp_amb': _('Ambiente'),
        }


class CancelamentoNotaFiscalForm(forms.ModelForm):

    class Meta:
        model = NotaFiscalSaida
        fields = ('just_canc', 'chave',
                  'numero_protocolo', 'tp_emis', 'tp_amb',)

        widgets = {
            'just_canc': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'chave': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'numero_protocolo': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'tp_emis': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'tp_amb': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
        labels = {
            'just_canc': _('Justificativa do cancelamento'),
            'chave': _('Chave'),
            'numero_protocolo': _('Número do protocolo'),
            'tp_emis': _('Forma de emissão'),
            'tp_amb': _('Ambiente'),
        }


class ConsultarCadastroForm(forms.Form):
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', }), label='Selecionar empresa', required=True)
    salvar_arquivos = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='Salvar arquivos XML gerados?', required=False)


class InutilizarNotasForm(forms.Form):
    ambiente = forms.ChoiceField(choices=TP_AMB_ESCOLHAS, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Ambiente', initial='2', required=True)
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', }), label='Selecionar empresa emitente', required=True)
    modelo = forms.ChoiceField(choices=MOD_NFE_ESCOLHAS, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Modelo', required=True)
    serie = forms.CharField(max_length=3, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='Série', required=True)
    numero_inicial = forms.CharField(max_length=9, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='Número inicial', required=True)
    numero_final = forms.CharField(max_length=9, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='Número final', required=False)
    justificativa = forms.CharField(max_length=255, widget=forms.Textarea(
        attrs={'class': 'form-control', }), label='Justificativa', required=False)
    salvar_arquivos = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='Salvar arquivos XML gerados?', required=False)


class ConsultarNotaForm(forms.Form):
    ambiente = forms.ChoiceField(choices=TP_AMB_ESCOLHAS, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Ambiente', initial='2', required=True)
    nota = forms.ModelChoiceField(queryset=NotaFiscalSaida.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', }), label='Selecionar nota da base de dados', required=False)
    chave = forms.CharField(max_length=44, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='Chave da nota', required=False)
    salvar_arquivos = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='Salvar arquivos XML gerados?', required=False)


class BaixarNotaForm(forms.Form):
    ambiente = forms.ChoiceField(choices=TP_AMB_ESCOLHAS, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Ambiente', initial='2', required=True)
    nota = forms.ModelChoiceField(queryset=NotaFiscalSaida.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', }), label='Selecionar nota da base de dados', required=False)
    chave = forms.CharField(max_length=44, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='Chave da nota', required=False)
    ambiente_nacional = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='Utilizar ambiente nacional?(Recomendado)', initial=True, required=False)
    salvar_arquivos = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='Salvar arquivos XML gerados?', required=False)


class ManifestacaoDestinatarioForm(forms.Form):
    cnpj = forms.CharField(max_length=16, widget=forms.TextInput(attrs={
                           'class': 'form-control', }), label='CNPJ do autor do Evento(apenas digitos)', required=True)
    tipo_manifesto = forms.ChoiceField(choices=TP_MANIFESTO_OPCOES, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Tipo de manifesto', required=True)
    ambiente = forms.ChoiceField(choices=TP_AMB_ESCOLHAS, widget=forms.Select(
        attrs={'class': 'form-control', }), label='Ambiente', initial='2', required=True)
    nota = forms.ModelChoiceField(queryset=NotaFiscalSaida.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', }), label='Selecionar nota da base de dados', required=False)
    chave = forms.CharField(max_length=44, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='Chave da nota', required=False)
    ambiente_nacional = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='Utilizar ambiente nacional?(Recomendado)', initial=True, required=False)
    justificativa = forms.CharField(max_length=255, widget=forms.Textarea(
        attrs={'class': 'form-control', }), label='Justificativa', required=False)
    salvar_arquivos = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-control', }), label='Salvar arquivos XML gerados?', required=False)


class AutXMLForm(forms.ModelForm):

    class Meta:
        model = AutXML
        fields = ('cpf_cnpj',)
        labels = {
            'cpf_cnpj': _('CPF/CNPJ (Apenas digitos)'),
        }
        widgets = {
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ConfiguracaoNotaFiscalForm(forms.ModelForm):

    class Meta:
        model = ConfiguracaoNotaFiscal
        fields = ('serie_atual', 'ambiente', 'imp_danfe', 'arquivo_certificado_a1',
                  'senha_certificado', 'inserir_logo_danfe', 'orientacao_logo_danfe', 'csc', 'cidtoken',)
        labels = {
            'arquivo_certificado_a1': _('Certificado A1'),
            'serie_atual': _('Série atual'),
            'ambiente': _('Ambiente'),
            'imp_danfe': _('Tipo de impressão DANFE'),
            'senha_certificado': _('Senha do certificado'),
            'inserir_logo_danfe': _('Inserir logo da empresa no DANFE?'),
            'orientacao_logo_danfe': _('Orientação do logo'),
            'csc': _('Código de Segurança do Contribuinte'),
            'cidtoken': _('Identificador do CSC'),
        }
        widgets = {
            'arquivo_certificado_a1': forms.FileInput(attrs={'class': 'form-control'}),
            'serie_atual': forms.TextInput(attrs={'class': 'form-control'}),
            'ambiente': forms.Select(attrs={'class': 'form-control'}),
            'imp_danfe': forms.Select(attrs={'class': 'form-control'}),
            'senha_certificado': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
            'inserir_logo_danfe': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'orientacao_logo_danfe': forms.Select(attrs={'class': 'form-control'}),
            'csc': forms.TextInput(attrs={'class': 'form-control'}),
            'cidtoken': forms.TextInput(attrs={'class': 'form-control'}),
        }


AutXMLFormSet = inlineformset_factory(
    NotaFiscalSaida, AutXML, form=AutXMLForm, extra=1, can_delete=True)
