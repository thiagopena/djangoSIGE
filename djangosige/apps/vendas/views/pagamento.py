# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, View
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core import serializers

from djangosige.apps.vendas.forms import CondicaoPagamentoForm
from djangosige.apps.vendas.models import CondicaoPagamento


class AdicionarCondicaoPagamentoView(CreateView):
    form_class = CondicaoPagamentoForm
    template_name = "vendas/pagamento/condicao_pagamento_add.html"
    success_url = reverse_lazy('vendas:listacondicaopagamentoview')
    success_message = "Condição de pagamento <b>%(descricao)s </b>adicionada com sucesso."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(AdicionarCondicaoPagamentoView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR CONDIÇÃO DE PAGAMENTO'
        context['return_url'] = reverse_lazy(
            'vendas:listacondicaopagamentoview')
        return context

    def form_valid(self, form):
        super(AdicionarCondicaoPagamentoView, self).form_valid(form)
        messages.success(
            self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)


class CondicaoPagamentoListView(ListView):
    template_name = 'vendas/pagamento/condicao_pagamento_list.html'
    model = CondicaoPagamento
    context_object_name = 'all_cond_pagamento'
    success_url = reverse_lazy('vendas:listacondicaopagamentoview')

    def get_context_data(self, **kwargs):
        context = super(CondicaoPagamentoListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONDIÇÕES DE PAGAMENTO CADASTRADAS'
        context['add_url'] = reverse_lazy('vendas:addcondicaopagamentoview')
        return context

    def get_queryset(self):
        return CondicaoPagamento.objects.all()

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if value == "on":
                instance = CondicaoPagamento.objects.get(id=key)
                instance.delete()
        return redirect(self.success_url)


class EditarCondicaoPagamentoView(UpdateView):
    form_class = CondicaoPagamentoForm
    model = CondicaoPagamento
    template_name = "vendas/pagamento/condicao_pagamento_edit.html"
    success_url = reverse_lazy('vendas:listacondicaopagamentoview')
    success_message = "Condição de pagamento <b>%(descricao)s </b>editada com sucesso."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(EditarCondicaoPagamentoView,
                        self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy(
            'vendas:listacondicaopagamentoview')
        return context

    def form_valid(self, form):
        super(EditarCondicaoPagamentoView, self).form_valid(form)
        messages.success(
            self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)


class InfoCondicaoPagamento(View):

    def post(self, request, *args, **kwargs):
        pag = CondicaoPagamento.objects.get(pk=request.POST['pagamentoId'])
        data = serializers.serialize('json', [pag, ], fields=(
            'n_parcelas', 'parcela_inicial', 'dias_recorrencia'))
        return HttpResponse(data, content_type='application/json')
