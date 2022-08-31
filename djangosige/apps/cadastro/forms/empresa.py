# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _

from djangosige.apps.cadastro.models import Empresa, MinhaEmpresa


class EmpresaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EmpresaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Empresa
        fields = ('nome_razao_social', 'inscricao_municipal', 'cnae',
                  'logo_file', 'iest', 'informacoes_adicionais',)

        widgets = {
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'cnae': forms.TextInput(attrs={'class': 'form-control'}),
            'inscricao_municipal': forms.TextInput(attrs={'class': 'form-control'}),
            'logo_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'iest': forms.TextInput(attrs={'class': 'form-control'}),
            'informacoes_adicionais': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_razao_social': _('Razão Social'),
            'cnae': _('CNAE'),
            'inscricao_municipal': _('Inscrição Municipal'),
            'logo_file': _('Logo'),
            'iest': _('IE do substituto tributário'),
            'informacoes_adicionais': _('Informações Adicionais'),
        }

    def save(self, commit=True):
        instance = super(EmpresaForm, self).save(commit=False)
        instance.tipo_pessoa = 'PJ'
        instance.criado_por = self.request.user
        if 'empresa_form-logo_file' in self.request.FILES:
            instance.logo_file = self.request.FILES['empresa_form-logo_file']
        if commit:
            instance.save()
        return instance


class MinhaEmpresaForm(forms.ModelForm):

    class Meta:
        model = MinhaEmpresa
        fields = ('m_empresa',)

        widgets = {
            'm_empresa': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'm_empresa': _('Minha Empresa'),
        }
