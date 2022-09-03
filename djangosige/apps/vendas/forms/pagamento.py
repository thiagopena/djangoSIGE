# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory

from djangosige.apps.vendas.models import Venda, Pagamento, CondicaoPagamento


class PagamentoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PagamentoForm, self).__init__(*args, **kwargs)
        self.fields['valor_parcela'].localize = True

    class Meta:
        model = Pagamento
        fields = ('indice_parcela', 'vencimento', 'valor_parcela',)
        widgets = {
            'indice_parcela': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'vencimento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'valor_parcela': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
        }
        labels = {
            'indice_parcela': _('Ind. Parcela'),
            'vencimento': _('Vencimento'),
            'valor_parcela': _('Valor'),
        }


class CondicaoPagamentoForm(forms.ModelForm):

    class Meta:
        model = CondicaoPagamento
        fields = ('descricao', 'forma', 'n_parcelas',
                  'dias_recorrencia', 'parcela_inicial',)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'title': 'Insira uma breve descrição da condição de pagamento, EX: Entrada + 3x s/ juros'}),
            'forma': forms.Select(attrs={'class': 'form-control'}),
            'n_parcelas': forms.NumberInput(attrs={'class': 'form-control'}),
            'dias_recorrencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'parcela_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao': _('Descrição'),
            'forma': _('Forma'),
            'n_parcelas': _('Número de parcelas'),
            'dias_recorrencia': _('Recorrência (dias)'),
            'parcela_inicial': _('1ª parcela em (dias)'),
        }


PagamentoFormSet = inlineformset_factory(
    Venda, Pagamento, form=PagamentoForm, extra=1, can_delete=True)
