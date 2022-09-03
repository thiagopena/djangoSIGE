# -*- coding: utf-8 -*-

from django.urls import reverse_lazy

from djangosige.apps.base.custom_views import CustomCreateView, CustomListView, CustomUpdateView

from djangosige.apps.fiscal.forms import NaturezaOperacaoForm
from djangosige.apps.fiscal.models import NaturezaOperacao


class AdicionarNaturezaOperacaoView(CustomCreateView):
    form_class = NaturezaOperacaoForm
    template_name = "fiscal/natureza_operacao/natureza_operacao_add.html"
    success_url = reverse_lazy('djangosige.apps.fiscal:listanaturezaoperacaoview')
    success_message = "Natureza da operação <b>%(cfop)s </b>adicionada com sucesso."
    permission_codename = 'add_naturezaoperacao'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, cfop=self.object.cfop)

    def get_context_data(self, **kwargs):
        context = super(AdicionarNaturezaOperacaoView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR NATUREZA DA OPERAÇÃO'
        context['return_url'] = reverse_lazy(
            'djangosige.apps.fiscal:listanaturezaoperacaoview')
        return context


class NaturezaOperacaoListView(CustomListView):
    template_name = 'fiscal/natureza_operacao/natureza_operacao_list.html'
    model = NaturezaOperacao
    context_object_name = 'all_natops'
    success_url = reverse_lazy('djangosige.apps.fiscal:listanaturezaoperacaoview')
    permission_codename = 'view_naturezaoperacao'

    def get_context_data(self, **kwargs):
        context = super(NaturezaOperacaoListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'NATUREZAS DA OPERAÇÃO CADASTRADAS'
        context['add_url'] = reverse_lazy('djangosige.apps.fiscal:addnaturezaoperacaoview')
        return context


class EditarNaturezaOperacaoView(CustomUpdateView):
    form_class = NaturezaOperacaoForm
    model = NaturezaOperacao
    template_name = "fiscal/natureza_operacao/natureza_operacao_edit.html"
    success_url = reverse_lazy('djangosige.apps.fiscal:listanaturezaoperacaoview')
    success_message = "Natureza da operação <b>%(cfop)s </b>editada com sucesso."
    permission_codename = 'change_naturezaoperacao'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, cfop=self.object.cfop)

    def get_context_data(self, **kwargs):
        context = super(EditarNaturezaOperacaoView,
                        self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy(
            'djangosige.apps.fiscal:listanaturezaoperacaoview')
        return context
