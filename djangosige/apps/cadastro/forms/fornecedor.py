# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _

from djangosige.apps.cadastro.models import Fornecedor


class FornecedorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FornecedorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Fornecedor
        fields = ('nome_razao_social', 'tipo_pessoa',
                  'inscricao_municipal', 'ramo', 'informacoes_adicionais', )
        widgets = {
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pessoa': forms.RadioSelect(attrs={'class': 'form-control'}),
            'ramo': forms.TextInput(attrs={'class': 'form-control'}),
            'inscricao_municipal': forms.TextInput(attrs={'class': 'form-control'}),
            'informacoes_adicionais': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_razao_social': _('Razão Social'),
            'tipo_pessoa': _(''),
            'ramo': _('Ramo'),
            'inscricao_municipal': _('Inscrição Municipal'),
            'informacoes_adicionais': _('Informações Adicionais'),
        }

    def save(self, commit=True):
        instance = super(FornecedorForm, self).save(commit=False)
        instance.criado_por = self.request.user
        if commit:
            instance.save()
        return instance
