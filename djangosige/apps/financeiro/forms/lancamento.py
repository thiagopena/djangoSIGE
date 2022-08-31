# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _
from djangosige.apps.financeiro.models import Saida, Entrada, STATUS_CONTA_ENTRADA_ESCOLHAS, STATUS_CONTA_SAIDA_ESCOLHAS
from djangosige.apps.financeiro.models import PlanoContasGrupo
from djangosige.apps.login.models import Usuario
from djangosige.apps.cadastro.models import MinhaEmpresa, Banco


class LancamentoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LancamentoForm, self).__init__(*args, **kwargs)
        self.fields['abatimento'].localize = True
        self.fields['juros'].localize = True
        self.fields['valor_liquido'].localize = True
        self.fields['valor_total'].localize = True

        if user:
            try:
                usuario = Usuario.objects.get(user=user)
                m_empresa = MinhaEmpresa.objects.get(
                    m_usuario=usuario).m_empresa
                if m_empresa:
                    if Banco.objects.filter(pessoa_banco=m_empresa).count():
                        self.fields['conta_corrente'].choices = (
                            (None, '----------'),)
                        self.fields['conta_corrente'].choices += (
                            (conta.id, str(conta)) for conta in Banco.objects.filter(pessoa_banco=m_empresa))
                    else:
                        self.fields['conta_corrente'].choices = (
                            (None, '----------'),)
            except:
                self.fields['conta_corrente'].choices = ((None, '----------'),)
        else:
            self.fields['conta_corrente'].choices = ((None, '----------'),)

    class Meta:
        fields = ('descricao', 'grupo_plano', 'conta_corrente', 'data_pagamento', 'data_vencimento',
                  'valor_total', 'abatimento', 'juros', 'valor_liquido', 'movimentar_caixa',)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'grupo_plano': forms.Select(attrs={'class': 'form-control'}),
            'conta_corrente': forms.Select(attrs={'class': 'form-control'}),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'valor_total': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'abatimento': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'juros': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'valor_liquido': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'movimentar_caixa': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao': _('Descrição'),
            'grupo_plano': _('Grupo (Plano de contas)'),
            'conta_corrente': _('Conta corrente (Banco/Agência/Conta)'),
            'data_pagamento': _('Data do pagamento'),
            'data_vencimento': _('Data de vencimento'),
            'valor_total': _('Valor total (bruto)'),
            'abatimento': _('Abatimento'),
            'juros': _('Juros'),
            'valor_liquido': _('Valor líquido'),
            'movimentar_caixa': _('Movimentar Caixa?'),
        }


class EntradaForm(LancamentoForm):

    def __init__(self, *args, **kwargs):
        super(EntradaForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = '0'

        if PlanoContasGrupo.objects.filter(tipo_grupo='1').count():
            self.fields['grupo_plano'].choices = ((grupo.id, str(grupo.codigo) + ' - ' + str(
                grupo.descricao)) for grupo in PlanoContasGrupo.objects.filter(tipo_grupo='0'))
        else:
            self.fields['grupo_plano'].choices = ((None, '----------'),)

    class Meta(LancamentoForm.Meta):
        model = Entrada
        fields = LancamentoForm.Meta.fields + ('cliente', 'status',)
        widgets = LancamentoForm.Meta.widgets
        widgets['cliente'] = forms.Select(attrs={'class': 'form-control'})
        widgets['status'] = forms.Select(
            attrs={'class': 'form-control', 'disabled': True})
        labels = LancamentoForm.Meta.labels
        labels['cliente'] = _('Cliente')
        labels['status'] = _('Status')


class SaidaForm(LancamentoForm):

    def __init__(self, *args, **kwargs):
        super(SaidaForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = '0'

        if PlanoContasGrupo.objects.filter(tipo_grupo='1').count():
            self.fields['grupo_plano'].choices = ((grupo.id, str(grupo.codigo) + ' - ' + str(
                grupo.descricao)) for grupo in PlanoContasGrupo.objects.filter(tipo_grupo='1'))
        else:
            self.fields['grupo_plano'].choices = ((None, '----------'),)

    class Meta(LancamentoForm.Meta):
        model = Saida
        fields = LancamentoForm.Meta.fields + ('fornecedor', 'status',)
        widgets = LancamentoForm.Meta.widgets
        widgets['fornecedor'] = forms.Select(attrs={'class': 'form-control'})
        widgets['status'] = forms.Select(
            attrs={'class': 'form-control', 'disabled': True})
        labels = LancamentoForm.Meta.labels
        labels['fornecedor'] = _('Fornecedor')
        labels['status'] = _('Status')


class ContaReceberForm(EntradaForm):

    def __init__(self, *args, **kwargs):
        super(ContaReceberForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = STATUS_CONTA_ENTRADA_ESCOLHAS
        self.fields['status'].initial = '1'
        self.fields['data_pagamento'].widget.attrs = {
            'class': 'form-control hidden', 'disabled': True, 'style': 'background-color:lightgrey;'}


class ContaPagarForm(SaidaForm):

    def __init__(self, *args, **kwargs):
        super(ContaPagarForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = STATUS_CONTA_SAIDA_ESCOLHAS
        self.fields['status'].initial = '1'
        self.fields['data_pagamento'].widget.attrs = {
            'class': 'form-control hidden', 'disabled': True, 'style': 'background-color:lightgrey;'}
