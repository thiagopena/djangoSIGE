# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory

from djangosige.apps.compras.models import Compra, Pagamento


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


PagamentoFormSet = inlineformset_factory(
    Compra, Pagamento, form=PagamentoForm, extra=1, can_delete=True)
