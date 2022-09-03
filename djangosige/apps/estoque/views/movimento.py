# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.shortcuts import redirect

from itertools import chain
from datetime import datetime
from decimal import Decimal

from djangosige.apps.base.custom_views import CustomDetailView, CustomCreateView, CustomListView

from djangosige.apps.estoque.forms import EntradaEstoqueForm, SaidaEstoqueForm, TransferenciaEstoqueForm, ItensMovimentoFormSet
from djangosige.apps.estoque.models import MovimentoEstoque, EntradaEstoque, SaidaEstoque, TransferenciaEstoque, ProdutoEstocado


class MovimentoEstoqueMixin(object):

    def adicionar_novo_movimento_estoque(self, itens_mvmt_obj, pform, lista_produtos, lista_produtos_estocados):
        prod = itens_mvmt_obj.produto
        lista_produtos.append(prod)

        # Modificar valor do estoque atual dos produtos
        if prod.estoque_atual is not None and isinstance(self.object, EntradaEstoque):
            prod_estocado = ProdutoEstocado.objects.get_or_create(
                local=self.object.local_dest, produto=itens_mvmt_obj.produto)[0]
            prod_estocado.quantidade = prod_estocado.quantidade + itens_mvmt_obj.quantidade
            lista_produtos_estocados.append(prod_estocado)
            prod.estoque_atual = prod.estoque_atual + itens_mvmt_obj.quantidade

        elif prod.estoque_atual is not None and isinstance(self.object, SaidaEstoque):
            prod_estocado = ProdutoEstocado.objects.get_or_create(
                local=self.object.local_orig, produto=itens_mvmt_obj.produto)[0]

            if itens_mvmt_obj.quantidade > prod_estocado.quantidade:
                itens_mvmt_obj.quantidade = prod_estocado.quantidade
                prod_estocado.quantidade = Decimal('0.00')
            else:
                prod_estocado.quantidade = prod_estocado.quantidade - itens_mvmt_obj.quantidade

            lista_produtos_estocados.append(prod_estocado)

            if prod.estoque_atual < itens_mvmt_obj.quantidade:
                pform.add_error('quantidade', 'Quantidade retirada do estoque maior que o estoque atual (' +
                                str(prod.estoque_atual).replace('.', ',') + ') do produto.')
            else:
                prod.estoque_atual = prod.estoque_atual - itens_mvmt_obj.quantidade

        elif isinstance(self.object, TransferenciaEstoque):
            prod_estocado_orig = ProdutoEstocado.objects.get_or_create(
                local=self.object.local_estoque_orig, produto=itens_mvmt_obj.produto)[0]
            prod_estocado_dest = ProdutoEstocado.objects.get_or_create(
                local=self.object.local_estoque_dest, produto=itens_mvmt_obj.produto)[0]

            if itens_mvmt_obj.quantidade > prod_estocado_orig.quantidade:
                itens_mvmt_obj.quantidade = prod_estocado_orig.quantidade
                prod_estocado_orig.quantidade = Decimal('0.00')
            else:
                prod_estocado_orig.quantidade = prod_estocado_orig.quantidade - \
                    itens_mvmt_obj.quantidade

            prod_estocado_dest.quantidade = prod_estocado_dest.quantidade + \
                itens_mvmt_obj.quantidade

            lista_produtos_estocados.append(prod_estocado_orig)
            lista_produtos_estocados.append(prod_estocado_dest)


class AdicionarMovimentoEstoqueBaseView(CustomCreateView, MovimentoEstoqueMixin):
    permission_codename = 'add_movimentoestoque'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(AdicionarMovimentoEstoqueBaseView,
                        self).get_context_data(**kwargs)
        return self.view_context(context)

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = form_class()
        form.initial['data_movimento'] = datetime.today().strftime('%d/%m/%Y')

        itens_form = ItensMovimentoFormSet(prefix='itens_form')

        return self.render_to_response(self.get_context_data(form=form, itens_form=itens_form,))

    def post(self, request, *args, **kwargs):
        self.object = None
        # Tirar . dos campos decimais
        req_post = request.POST.copy()
        for key in req_post:
            if ('quantidade' in key or
                'valor' in key or
                    'total' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        itens_form = ItensMovimentoFormSet(request.POST, prefix='itens_form')

        if (form.is_valid() and itens_form.is_valid()):
            self.object = form.save(commit=False)
            lista_produtos = []
            lista_produtos_estocados = []
            itens_form.instance = self.object

            for pform in itens_form:
                if pform.cleaned_data != {}:
                    itens_mvmt_obj = pform.save(commit=False)
                    itens_mvmt_obj.movimento_id = self.object

                    self.adicionar_novo_movimento_estoque(
                        itens_mvmt_obj, pform, lista_produtos, lista_produtos_estocados)

            # Verificar se movimentos de estoque invalidos existem
            if len(pform.errors):
                return self.form_invalid(form=form, itens_form=itens_form)
            else:
                self.object.save()
                itens_form.save()
                for prod in lista_produtos:
                    prod.save()
                for prod_estocado in lista_produtos_estocados:
                    prod_estocado.save()
                return self.form_valid(form)

        return self.form_invalid(form=form, itens_form=itens_form)


class AdicionarEntradaEstoqueView(AdicionarMovimentoEstoqueBaseView):
    form_class = EntradaEstoqueForm
    template_name = "estoque/movimento/movimento_estoque_add.html"
    success_url = reverse_lazy('djangosige.apps.estoque:listaentradasestoqueview')
    success_message = "<b>Movimento de estoque de entrada nº%(pk)s</b> adicionado com sucesso."

    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR ENTRADA EM ESTOQUE'
        context['return_url'] = reverse_lazy(
            'djangosige.apps.estoque:listaentradasestoqueview')
        return context


class AdicionarSaidaEstoqueView(AdicionarMovimentoEstoqueBaseView):
    form_class = SaidaEstoqueForm
    template_name = "estoque/movimento/movimento_estoque_add.html"
    success_url = reverse_lazy('djangosige.apps.estoque:listasaidasestoqueview')
    success_message = "<b>Movimento de estoque de saída nº%(pk)s</b> adicionado com sucesso."

    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR SAÍDA EM ESTOQUE'
        context['return_url'] = reverse_lazy('djangosige.apps.estoque:listasaidasestoqueview')
        return context


class AdicionarTransferenciaEstoqueView(AdicionarMovimentoEstoqueBaseView):
    form_class = TransferenciaEstoqueForm
    template_name = "estoque/movimento/movimento_estoque_add.html"
    success_url = reverse_lazy('djangosige.apps.estoque:listatransferenciasestoqueview')
    success_message = "<b>Movimento de estoque de transferência nº%(pk)s</b> adicionado com sucesso."

    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR TRANSFERÊNCIA EM ESTOQUE'
        context['return_url'] = reverse_lazy(
            'djangosige.apps.estoque:listatransferenciasestoqueview')
        return context


class MovimentoEstoqueBaseListView(CustomListView):
    permission_codename = 'view_movimentoestoque'

    def get_context_data(self, **kwargs):
        context = super(MovimentoEstoqueBaseListView,
                        self).get_context_data(**kwargs)
        return self.view_context(context)


class MovimentoEstoqueListView(MovimentoEstoqueBaseListView):
    template_name = 'estoque/movimento/movimento_estoque_list.html'
    context_object_name = 'all_movimentos'
    success_url = reverse_lazy('djangosige.apps.estoque:listamovimentoestoqueview')

    def view_context(self, context):
        context['title_complete'] = 'TODAS AS MOVIMENTAÇÕES DE ESTOQUE'
        return context

    def get_queryset(self):
        all_entradas = EntradaEstoque.objects.all()
        all_saidas = SaidaEstoque.objects.all()
        all_transferencias = TransferenciaEstoque.objects.all()
        all_movimentos = list(
            chain(all_saidas, all_entradas, all_transferencias))
        return all_movimentos

    def post(self, request, *args, **kwargs):
        if self.check_user_delete_permission(request, MovimentoEstoque):
            for key, value in request.POST.items():
                if value == "on":
                    if EntradaEstoque.objects.filter(id=key).exists():
                        instance = EntradaEstoque.objects.get(id=key)
                    elif SaidaEstoque.objects.filter(id=key).exists():
                        instance = SaidaEstoque.objects.get(id=key)
                    elif TransferenciaEstoque.objects.filter(id=key).exists():
                        instance = TransferenciaEstoque.objects.get(id=key)

                    instance.delete()
        return redirect(self.success_url)


class EntradaEstoqueListView(MovimentoEstoqueBaseListView):
    template_name = 'estoque/movimento/movimento_estoque_list.html'
    model = EntradaEstoque
    context_object_name = 'all_entradas'
    success_url = reverse_lazy('djangosige.apps.estoque:listaentradasestoqueview')

    def view_context(self, context):
        context['title_complete'] = 'ENTRADAS EM ESTOQUE'
        context['add_url'] = reverse_lazy('djangosige.apps.estoque:addentradaestoqueview')
        return context


class SaidaEstoqueListView(MovimentoEstoqueBaseListView):
    template_name = 'estoque/movimento/movimento_estoque_list.html'
    model = SaidaEstoque
    context_object_name = 'all_saidas'
    success_url = reverse_lazy('djangosige.apps.estoque:listasaidasestoqueview')

    def view_context(self, context):
        context['title_complete'] = 'SAÍDAS EM ESTOQUE'
        context['add_url'] = reverse_lazy('djangosige.apps.estoque:addsaidaestoqueview')
        return context


class TransferenciaEstoqueListView(MovimentoEstoqueBaseListView):
    template_name = 'estoque/movimento/movimento_estoque_list.html'
    model = TransferenciaEstoque
    context_object_name = 'all_transferencias'
    success_url = reverse_lazy('djangosige.apps.estoque:listatransferenciasestoqueview')

    def view_context(self, context):
        context['title_complete'] = 'TRANSFERÊNCIAS EM ESTOQUE'
        context['add_url'] = reverse_lazy(
            'djangosige.apps.estoque:addtransferenciaestoqueview')
        return context


class DetalharMovimentoEstoqueBaseView(CustomDetailView):
    template_name = "estoque/movimento/movimento_estoque_detail.html"
    permission_codename = 'view_movimentoestoque'

    def get_context_data(self, **kwargs):
        context = super(DetalharMovimentoEstoqueBaseView,
                        self).get_context_data(**kwargs)
        return self.view_context(context)


class DetalharEntradaEstoqueView(DetalharMovimentoEstoqueBaseView):
    model = EntradaEstoque

    def view_context(self, context):
        context['title_complete'] = 'MOVIMENTO DE ENTRADA EM ESTOQUE N°' + \
            str(self.object.id)
        context['return_url'] = reverse_lazy(
            'djangosige.apps.estoque:listaentradasestoqueview')
        return context


class DetalharSaidaEstoqueView(DetalharMovimentoEstoqueBaseView):
    model = SaidaEstoque

    def view_context(self, context):
        context['title_complete'] = 'MOVIMENTO DE SAÍDA EM ESTOQUE N°' + \
            str(self.object.id)
        context['return_url'] = reverse_lazy('djangosige.apps.estoque:listasaidasestoqueview')
        return context


class DetalharTransferenciaEstoqueView(DetalharMovimentoEstoqueBaseView):
    model = TransferenciaEstoque

    def view_context(self, context):
        context['title_complete'] = 'MOVIMENTO DE TRANSFERÊNCIA EM ESTOQUE N°' + \
            str(self.object.id)
        context['return_url'] = reverse_lazy(
            'djangosige.apps.estoque:listatransferenciasestoqueview')
        return context
