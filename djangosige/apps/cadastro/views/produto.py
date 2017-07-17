# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import F

from djangosige.apps.cadastro.forms import ProdutoForm, CategoriaForm, UnidadeForm, MarcaForm
from djangosige.apps.cadastro.models import Produto, Categoria, Unidade, Marca, Fornecedor
from djangosige.apps.estoque.models import ItensMovimento, EntradaEstoque, ProdutoEstocado

from datetime import datetime


class AdicionarProdutoView(CreateView):
    form_class = ProdutoForm
    template_name = "cadastro/produto/produto_add.html"
    success_url = reverse_lazy('cadastro:listaprodutosview')
    success_message = "Produto <b>%(descricao)s </b>adicionado com sucesso."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(AdicionarProdutoView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CADASTRAR PRODUTO'
        context['return_url'] = reverse_lazy('cadastro:listaprodutosview')
        return context

    def get(self, request, *args, **kwargs):
        return super(AdicionarProdutoView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        # Tirar . dos campos decimais
        req_post = request.POST.copy()

        for key, value in req_post.items():
            if ('venda' in key or
                'custo' in key or
                'estoque_minimo' in key or
                    'estoque_atual' in key):
                req_post[key] = req_post[key].replace('.', '')

        if 'EX:' in req_post['ncm']:
            ncm = req_post['ncm'][0:8]
            ex_start = req_post['ncm'].find('EX:') + 3
            ex_end = req_post['ncm'].find(']')
            ex_tipi = req_post['ncm'][ex_start:ex_end]
            req_post['ncm'] = ncm + ex_tipi

        request.POST = req_post

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            self.object = form.save(commit=False)

            if self.object.controlar_estoque and form.cleaned_data['estoque_inicial'] > 0:
                # Gerar movimento de estoque inicial
                mov_inicial = EntradaEstoque()
                item_entrada = ItensMovimento()
                prod_estocado = ProdutoEstocado()

                mov_inicial.data_movimento = datetime.now().date()
                mov_inicial.quantidade_itens = 1
                mov_inicial.tipo_movimento = u'3'
                mov_inicial.observacoes = ''
                mov_inicial.valor_total = round(
                    self.object.venda * form.cleaned_data['estoque_inicial'], 2)

                if form.cleaned_data['fornecedor']:
                    mov_inicial.fornecedor = Fornecedor.objects.get(
                        id=form.cleaned_data['fornecedor'])
                if form.cleaned_data['local_dest']:
                    mov_inicial.local_dest = form.cleaned_data['local_dest']

                item_entrada.quantidade = form.cleaned_data['estoque_inicial']
                item_entrada.valor_unit = self.object.venda
                item_entrada.subtotal = mov_inicial.valor_total

                prod_estocado.local = mov_inicial.local_dest
                prod_estocado.quantidade = form.cleaned_data['estoque_inicial']

                self.object.estoque_atual = form.cleaned_data[
                    'estoque_inicial']
                self.object.save()
                mov_inicial.save()

                item_entrada.movimento_id = mov_inicial
                item_entrada.produto = self.object
                item_entrada.save()

                prod_estocado.produto = self.object
                prod_estocado.save()

            else:
                self.object.save()

            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        super(AdicionarProdutoView, self).form_valid(form)
        messages.success(
            self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,))


class ProdutosListView(ListView):
    template_name = 'cadastro/produto/produto_list.html'
    model = Produto
    context_object_name = 'all_produtos'
    success_url = reverse_lazy('cadastro:listaprodutosview')

    def get_context_data(self, **kwargs):
        context = super(ProdutosListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'PRODUTOS CADASTRADOS'
        context['add_url'] = reverse_lazy('cadastro:addprodutoview')
        return context

    def get_queryset(self):
        return Produto.objects.all()

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if value == "on":
                instance = Produto.objects.get(id=key)
                instance.delete()
        return redirect(self.success_url)


class ProdutosBaixoEstoqueListView(ProdutosListView):
    success_url = reverse_lazy('cadastro:listaprodutosbaixoestoqueview')

    def get_context_data(self, **kwargs):
        context = super(ProdutosBaixoEstoqueListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'PRODUTOS COM BAIXO ESTOQUE'
        return context

    def get_queryset(self):
        return Produto.objects.filter(estoque_atual__lte=F('estoque_minimo'))


class EditarProdutoView(UpdateView):
    form_class = ProdutoForm
    model = Produto
    template_name = "cadastro/produto/produto_edit.html"
    success_url = reverse_lazy('cadastro:listaprodutosview')
    success_message = "Produto <b>%(descricao)s </b>editado com sucesso."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(EditarProdutoView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('cadastro:listaprodutosview')
        return context

    def post(self, request, *args, **kwargs):
        # Tirar . dos campos decimais
        req_post = request.POST.copy()

        for key, value in req_post.items():
            if ('venda' in key or
                'custo' in key or
                'estoque_minimo' in key or
                    'estoque_atual' in key):
                req_post[key] = req_post[key].replace('.', '')

        if 'EX:' in req_post['ncm']:
            ncm = req_post['ncm'][0:8]
            ex_start = req_post['ncm'].find('EX:') + 3
            ex_end = req_post['ncm'].find(']')
            ex_tipi = req_post['ncm'][ex_start:ex_end]
            req_post['ncm'] = ncm + ex_tipi

        request.POST = req_post

        return super(EditarProdutoView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        super(EditarProdutoView, self).form_valid(form)
        messages.success(
            self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)


class AdicionarCategoriaView(CreateView):
    form_class = CategoriaForm
    template_name = "base/popup_form.html"
    success_url = reverse_lazy('cadastro:addcategoriaview')

    def get_context_data(self, **kwargs):
        context = super(AdicionarCategoriaView,
                        self).get_context_data(**kwargs)
        context['titulo'] = 'Adicionar categoria'
        return context


class CategoriasListView(ListView):
    model = Categoria
    template_name = 'cadastro/produto/categoria_list.html'
    context_object_name = 'all_categorias'
    success_url = reverse_lazy('cadastro:listacategoriasview')

    def get_queryset(self):
        return Categoria.objects.all()

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if value == "on":
                instance = Categoria.objects.get(id=key)
                instance.delete()
        return redirect(self.success_url)


class EditarCategoriaView(UpdateView):
    form_class = CategoriaForm
    model = Categoria
    template_name = "base/popup_form.html"
    success_url = reverse_lazy('cadastro:listacategoriasview')

    def get_context_data(self, **kwargs):
        context = super(EditarCategoriaView, self).get_context_data(**kwargs)
        context['titulo'] = 'Editar categoria: ' + str(self.object)
        return context


class AdicionarUnidadeView(CreateView):
    form_class = UnidadeForm
    template_name = "base/popup_form.html"
    success_url = reverse_lazy('cadastro:addunidadeview')

    def get_context_data(self, **kwargs):
        context = super(AdicionarUnidadeView, self).get_context_data(**kwargs)
        context['titulo'] = 'Adicionar unidade'
        return context


class UnidadesListView(ListView):
    model = Unidade
    template_name = 'cadastro/produto/unidade_list.html'
    context_object_name = 'all_unidades'
    success_url = reverse_lazy('cadastro:listaunidadesview')

    def get_queryset(self):
        return Unidade.objects.all()

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if value == "on":
                instance = Unidade.objects.get(id=key)
                instance.delete()
        return redirect(self.success_url)


class EditarUnidadeView(UpdateView):
    form_class = UnidadeForm
    model = Unidade
    template_name = "base/popup_form.html"
    success_url = reverse_lazy('cadastro:listaunidadesview')

    def get_context_data(self, **kwargs):
        context = super(EditarUnidadeView, self).get_context_data(**kwargs)
        context['titulo'] = 'Editar unidade: ' + str(self.object)
        return context


class AdicionarMarcaView(CreateView):
    form_class = MarcaForm
    template_name = "base/popup_form.html"
    success_url = reverse_lazy('cadastro:addmarcaview')

    def get_context_data(self, **kwargs):
        context = super(AdicionarMarcaView, self).get_context_data(**kwargs)
        context['titulo'] = 'Adicionar marca'
        return context


class MarcasListView(ListView):
    model = Marca
    template_name = 'cadastro/produto/marca_list.html'
    context_object_name = 'all_marcas'
    success_url = reverse_lazy('cadastro:listamarcasview')

    def get_queryset(self):
        return Marca.objects.all()

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if value == "on":
                instance = Marca.objects.get(id=key)
                instance.delete()
        return redirect(self.success_url)


class EditarMarcaView(UpdateView):
    form_class = MarcaForm
    model = Marca
    template_name = "base/popup_form.html"
    success_url = reverse_lazy('cadastro:listamarcasview')

    def get_context_data(self, **kwargs):
        context = super(EditarMarcaView, self).get_context_data(**kwargs)
        context['titulo'] = 'Editar marca: ' + str(self.object)
        return context
