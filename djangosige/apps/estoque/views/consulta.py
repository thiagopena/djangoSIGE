# -*- coding: utf-8 -*-

from django.urls import reverse_lazy

from djangosige.apps.base.custom_views import CustomListView

from djangosige.apps.cadastro.models import Produto
from djangosige.apps.estoque.models import LocalEstoque


class ConsultaEstoqueView(CustomListView):
    template_name = "estoque/consulta/consulta_estoque.html"
    success_url = reverse_lazy('djangosige.apps.estoque:consultaestoqueview')
    context_object_name = 'produtos_filtrados'
    permission_codename = 'consultar_estoque'

    def get_context_data(self, **kwargs):
        context = super(ConsultaEstoqueView, self).get_context_data(**kwargs)
        context['todos_produtos'] = Produto.objects.filter(
            controlar_estoque=True)
        context['todos_locais'] = LocalEstoque.objects.all()
        context['title_complete'] = 'CONSULTA DE ESTOQUE'
        return context

    def get_queryset(self):
        produto = self.request.GET.get('produto')
        local = self.request.GET.get('local')

        if produto:
            produtos_filtrados = Produto.objects.filter(id=produto)
        elif local:
            produtos_filtrados = LocalEstoque.objects.get(
                id=local).produtos_estoque.filter(controlar_estoque=True, estoque_atual__gt=0)
        else:
            produtos_filtrados = Produto.objects.filter(
                controlar_estoque=True, estoque_atual__gt=0)

        return produtos_filtrados
