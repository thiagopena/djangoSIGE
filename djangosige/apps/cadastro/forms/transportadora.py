# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory

from djangosige.apps.cadastro.models import Transportadora, Veiculo


class TransportadoraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TransportadoraForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Transportadora
        fields = ('nome_razao_social', 'tipo_pessoa',
                  'informacoes_adicionais',)
        widgets = {
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pessoa': forms.RadioSelect(attrs={'class': 'form-control'}),
            'informacoes_adicionais': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_razao_social': _('Razão Social'),
            'tipo_pessoa': _(''),
            'informacoes_adicionais': _('Informações Adicionais'),
        }

    def save(self, commit=True):
        instance = super(TransportadoraForm, self).save(commit=False)
        instance.criado_por = self.request.user
        if commit:
            instance.save()
        return instance


class VeiculoForm(forms.ModelForm):

    class Meta:
        model = Veiculo
        fields = ('descricao', 'placa', 'uf',)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao': _('Descrição'),
            'placa': _('Placa'),
            'uf': _('UF'),
        }


VeiculoFormSet = inlineformset_factory(
    Transportadora, Veiculo, form=VeiculoForm, extra=1, can_delete=True)
