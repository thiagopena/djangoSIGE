# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _

from djangosige.apps.estoque.models import LocalEstoque


class LocalEstoqueForm(forms.ModelForm):

    class Meta:
        model = LocalEstoque
        fields = ('descricao',)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao': _('Descrição'),
        }
