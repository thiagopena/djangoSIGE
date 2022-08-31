# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory

from djangosige.apps.compras.models import OrcamentoCompra, PedidoCompra, ItensCompra, Compra


class CompraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = '0'

        self.fields['valor_total'].localize = True
        self.fields['valor_total'].initial = '0.00'

        self.fields['desconto'].localize = True
        self.fields['desconto'].initial = '0.00'

        self.fields['despesas'].localize = True
        self.fields['despesas'].initial = '0.00'

        self.fields['seguro'].localize = True
        self.fields['seguro'].initial = '0.00'

        self.fields['frete'].localize = True
        self.fields['frete'].initial = '0.00'

        self.fields['total_ipi'].localize = True
        self.fields['total_ipi'].initial = '0.00'

        self.fields['total_icms'].localize = True
        self.fields['total_icms'].initial = '0.00'

    class Meta:
        fields = ('data_emissao', 'fornecedor', 'mod_frete', 'desconto', 'tipo_desconto', 'frete', 'despesas', 'local_dest',
                  'movimentar_estoque', 'seguro', 'total_ipi', 'total_icms', 'valor_total', 'cond_pagamento', 'observacoes', )

        widgets = {
            'data_emissao': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'mod_frete': forms.Select(attrs={'class': 'form-control'}),
            'local_dest': forms.Select(attrs={'class': 'form-control'}),
            'movimentar_estoque': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'valor_total': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
            'tipo_desconto': forms.Select(attrs={'class': 'form-control'}),
            'desconto': forms.TextInput(attrs={'class': 'form-control decimal-mask-four'}),
            'frete': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'despesas': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'seguro': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'total_icms': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
            'total_ipi': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
            'cond_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'data_emissao': _('Data de Emissão'),
            'fornecedor': _('Fornecedor'),
            'mod_frete': _('Modalidade do frete'),
            'local_dest': _('Localização de estoque de destino dos produtos'),
            'movimentar_estoque': _('Movimentar estoque?'),
            'vendedor': _('Vendedor'),
            'valor_total': _('Total (R$)'),
            'tipo_desconto': _('Tipo de desconto'),
            'desconto': _('Desconto (% ou R$)'),
            'frete': _('Frete (R$)'),
            'despesas': _('Despesas (R$)'),
            'seguro': _('Seguro (R$)'),
            'total_ipi': _('Valor total IPI (R$)'),
            'total_icms': _('Valor total ICMS (R$)'),
            'cond_pagamento': _('Condição de pagamento'),
            'observacoes': _('Observações'),
        }


class OrcamentoCompraForm(CompraForm):

    class Meta(CompraForm.Meta):
        model = OrcamentoCompra
        fields = CompraForm.Meta.fields + ('data_vencimento', 'status',)
        widgets = CompraForm.Meta.widgets
        widgets['data_vencimento'] = forms.DateInput(
            attrs={'class': 'form-control datepicker'})
        widgets['status'] = forms.Select(
            attrs={'class': 'form-control', 'disabled': True})
        labels = CompraForm.Meta.labels
        labels['data_vencimento'] = _('Data de Vencimento')
        labels['status'] = _('Status')


class PedidoCompraForm(CompraForm):

    class Meta(CompraForm.Meta):
        model = PedidoCompra
        fields = CompraForm.Meta.fields + \
            ('data_entrega', 'status', 'orcamento',)
        widgets = CompraForm.Meta.widgets
        widgets['data_entrega'] = forms.DateInput(
            attrs={'class': 'form-control datepicker'})
        widgets['status'] = forms.Select(
            attrs={'class': 'form-control', 'disabled': True})
        widgets['orcamento'] = forms.Select(
            attrs={'class': 'form-control', 'disabled': True})
        labels = CompraForm.Meta.labels
        labels['data_entrega'] = _('Data de Entrega')
        labels['status'] = _('Status')
        labels['orcamento'] = _('Orçamento')


class ItensCompraForm(forms.ModelForm):
    total_sem_desconto = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'readonly': True}), label='Subtotal s/ desconto', required=False)
    total_impostos = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'readonly': True}), label='Impostos', required=False)
    total_com_impostos = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'readonly': True}), label='Total', required=False)
    calculo_imposto = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'hidden', 'disabled': True}), label='Cálc. Impostos', required=False)

    # IMPOSTO
    p_red_bc = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'modal-field', 'disabled': True}), required=False)
    tipo_ipi = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'modal-field', 'disabled': True}), choices=([('1', '1'), ('2', '2'), ('3', '3'), ]), required=False)
    vfixo_ipi = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'modal-field', 'disabled': True}), required=False)

    def __init__(self, *args, **kwargs):
        super(ItensCompraForm, self).__init__(*args, **kwargs)
        self.fields['quantidade'].localize = True
        self.fields['valor_unit'].localize = True
        self.fields['desconto'].localize = True
        self.fields['subtotal'].localize = True

        self.fields['total_sem_desconto'].localize = True
        self.fields['total_impostos'].localize = True
        self.fields['total_com_impostos'].localize = True
        self.fields['p_red_bc'].localize = True
        self.fields['vfixo_ipi'].localize = True

        self.fields['vicms'].localize = True
        self.fields['vipi'].localize = True
        self.fields['p_icms'].localize = True
        self.fields['p_ipi'].localize = True

    class Meta:
        model = ItensCompra
        fields = ('produto', 'quantidade', 'valor_unit', 'tipo_desconto', 'desconto',
                  'subtotal', 'vicms', 'vipi', 'p_icms', 'p_ipi',
                  'incluir_bc_icms', 'ipi_incluido_preco', 'icms_incluido_preco', 'auto_calcular_impostos',)

        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control select-produto'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'valor_unit': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'subtotal': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
            'tipo_desconto': forms.Select(attrs={'class': 'form-control'}),
            'desconto': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),

            'vicms': forms.TextInput(attrs={'class': 'modal-field'}),
            'vipi': forms.TextInput(attrs={'class': 'modal-field'}),
            'p_icms': forms.TextInput(attrs={'class': 'modal-field'}),
            'p_ipi': forms.TextInput(attrs={'class': 'modal-field'}),

            'ipi_incluido_preco': forms.CheckboxInput(attrs={'class': 'modal-field'}),
            'icms_incluido_preco': forms.CheckboxInput(attrs={'class': 'modal-field'}),
            'incluir_bc_icms': forms.CheckboxInput(attrs={'class': 'modal-field'}),
            'auto_calcular_impostos': forms.CheckboxInput(attrs={'class': 'modal-field'}),

        }
        labels = {
            'produto': _('Produto'),
            'quantidade': _('Quantidade'),
            'valor_unit': _('Vl. Unit.'),
            'subtotal': _('Subtotal'),
            'tipo_desconto': _('Tipo de desconto'),
            'desconto': _('Desconto (% ou R$)'),
        }

    def is_valid(self):
        valid = super(ItensCompraForm, self).is_valid()
        if self.cleaned_data.get('produto', None) is None:
            self.cleaned_data = {}
        return valid


ItensCompraFormSet = inlineformset_factory(
    Compra, ItensCompra, form=ItensCompraForm, extra=1, can_delete=True)
