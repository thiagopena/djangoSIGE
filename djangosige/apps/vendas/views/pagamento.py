# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.views.generic import View
from django.http import HttpResponse
from django.core import serializers

from djangosige.apps.base.custom_views import CustomCreateView, CustomListView, CustomUpdateView

from djangosige.apps.vendas.forms import CondicaoPagamentoForm
from djangosige.apps.vendas.models import CondicaoPagamento


class AdicionarCondicaoPagamentoView(CustomCreateView):
    form_class = CondicaoPagamentoForm
    template_name = "vendas/pagamento/condicao_pagamento_add.html"
    success_url = reverse_lazy('djangosige.apps.vendas:listacondicaopagamentoview')
    success_message = "Condição de pagamento <b>%(descricao)s </b>adicionada com sucesso."
    permission_codename = 'add_condicaopagamento'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(AdicionarCondicaoPagamentoView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR CONDIÇÃO DE PAGAMENTO'
        context['return_url'] = reverse_lazy(
            'djangosige.apps.vendas:listacondicaopagamentoview')
        return context


class CondicaoPagamentoListView(CustomListView):
    template_name = 'vendas/pagamento/condicao_pagamento_list.html'
    model = CondicaoPagamento
    context_object_name = 'all_cond_pagamento'
    success_url = reverse_lazy('djangosige.apps.vendas:listacondicaopagamentoview')
    permission_codename = 'view_condicaopagamento'

    def get_context_data(self, **kwargs):
        context = super(CondicaoPagamentoListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONDIÇÕES DE PAGAMENTO CADASTRADAS'
        context['add_url'] = reverse_lazy('djangosige.apps.vendas:addcondicaopagamentoview')
        return context


class EditarCondicaoPagamentoView(CustomUpdateView):
    form_class = CondicaoPagamentoForm
    model = CondicaoPagamento
    template_name = "vendas/pagamento/condicao_pagamento_edit.html"
    success_url = reverse_lazy('djangosige.apps.vendas:listacondicaopagamentoview')
    success_message = "Condição de pagamento <b>%(descricao)s </b>editada com sucesso."
    permission_codename = 'change_condicaopagamento'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(EditarCondicaoPagamentoView,
                        self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy(
            'djangosige.apps.vendas:listacondicaopagamentoview')
        return context


class InfoCondicaoPagamento(View):

    def post(self, request, *args, **kwargs):
        pag = CondicaoPagamento.objects.get(pk=request.POST['pagamentoId'])
        data = serializers.serialize('json', [pag, ], fields=(
            'n_parcelas', 'parcela_inicial', 'dias_recorrencia'))
        return HttpResponse(data, content_type='application/json')
