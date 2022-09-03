# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse

from djangosige.apps.base.custom_views import CustomView, CustomCreateView, CustomListView, CustomUpdateView

from djangosige.apps.compras.forms import OrcamentoCompraForm, PedidoCompraForm, ItensCompraFormSet, PagamentoFormSet
from djangosige.apps.compras.models import OrcamentoCompra, PedidoCompra, ItensCompra, Pagamento
from djangosige.apps.cadastro.models import MinhaEmpresa
from djangosige.apps.estoque.models import ProdutoEstocado, EntradaEstoque, ItensMovimento
from djangosige.apps.login.models import Usuario
from djangosige.configs.settings import MEDIA_ROOT
from .report_compras import CompraReport

from geraldo.generators import PDFGenerator
from datetime import datetime
import io


class AdicionarCompraView(CustomCreateView):

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(AdicionarCompraView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get(self, request, form_class, *args, **kwargs):
        self.object = None

        form = self.get_form(form_class)
        form.initial['data_emissao'] = datetime.today().strftime('%d/%m/%Y')

        produtos_form = ItensCompraFormSet(prefix='produtos_form')
        pagamento_form = PagamentoFormSet(prefix='pagamento_form')

        return self.render_to_response(self.get_context_data(form=form,
                                                             produtos_form=produtos_form,
                                                             pagamento_form=pagamento_form))

    def post(self, request, form_class, *args, **kwargs):
        self.object = None

        # Tirar . dos campos decimais
        req_post = request.POST.copy()

        for key in req_post:
            if ('desconto' in key or
                'quantidade' in key or
                'valor' in key or
                'frete' in key or
                'despesas' in key or
                'seguro' in key or
                    'total' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        form = self.get_form(form_class)
        produtos_form = ItensCompraFormSet(
            request.POST, prefix='produtos_form')
        pagamento_form = PagamentoFormSet(
            request.POST, prefix='pagamento_form')

        if (form.is_valid() and produtos_form.is_valid() and pagamento_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()

            for pform in produtos_form:
                if pform.cleaned_data != {}:
                    itens_compra_obj = pform.save(commit=False)
                    itens_compra_obj.compra_id = self.object
                    itens_compra_obj.save()

            pagamento_form.instance = self.object
            pagamento_form.save()

            return self.form_valid(form)

        return self.form_invalid(form=form,
                                 produtos_form=produtos_form,
                                 pagamento_form=pagamento_form)


class AdicionarOrcamentoCompraView(AdicionarCompraView):
    form_class = OrcamentoCompraForm
    template_name = "compras/orcamento_compra/orcamento_compra_add.html"
    success_url = reverse_lazy('djangosige.apps.compras:listaorcamentocompraview')
    success_message = "<b>Orçamento de compra %(id)s </b>adicionado com sucesso."
    permission_codename = 'add_orcamentocompra'

    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR ORÇAMENTO DE COMPRA'
        context['return_url'] = reverse_lazy(
            'djangosige.apps.compras:listaorcamentocompraview')
        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarOrcamentoCompraView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarOrcamentoCompraView, self).post(request, form_class, *args, **kwargs)


class AdicionarPedidoCompraView(AdicionarCompraView):
    form_class = PedidoCompraForm
    template_name = "compras/pedido_compra/pedido_compra_add.html"
    success_url = reverse_lazy('djangosige.apps.compras:listapedidocompraview')
    success_message = "<b>Pedido de compra %(id)s </b>adicionado com sucesso."
    permission_codename = 'add_pedidocompra'

    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR PEDIDO DE COMPRA'
        context['return_url'] = reverse_lazy('djangosige.apps.compras:listapedidocompraview')
        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarPedidoCompraView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarPedidoCompraView, self).post(request, form_class, *args, **kwargs)


class CompraListView(CustomListView):

    def get_context_data(self, **kwargs):
        context = super(CompraListView, self).get_context_data(**kwargs)
        return self.view_context(context)


class OrcamentoCompraListView(CompraListView):
    template_name = 'compras/orcamento_compra/orcamento_compra_list.html'
    model = OrcamentoCompra
    context_object_name = 'all_orcamentos'
    success_url = reverse_lazy('djangosige.apps.compras:listaorcamentocompraview')
    permission_codename = 'view_orcamentocompra'

    def view_context(self, context):
        context['title_complete'] = 'ORÇAMENTOS DE COMPRA'
        context['add_url'] = reverse_lazy('djangosige.apps.compras:addorcamentocompraview')
        return context


class OrcamentoCompraVencidosListView(OrcamentoCompraListView):
    success_url = reverse_lazy('djangosige.apps.compras:listaorcamentocompravencidosview')

    def view_context(self, context):
        context['title_complete'] = 'ORÇAMENTOS DE COMPRA VENCIDOS'
        context['add_url'] = reverse_lazy('djangosige.apps.compras:addorcamentocompraview')
        return context

    def get_queryset(self):
        return OrcamentoCompra.objects.filter(data_vencimento__lte=datetime.now().date(), status='0')


class OrcamentoCompraVencimentoHojeListView(OrcamentoCompraListView):
    success_url = reverse_lazy('djangosige.apps.compras:listaorcamentocomprahojeview')

    def view_context(self, context):
        context['title_complete'] = 'ORÇAMENTOS DE COMPRA COM VENCIMENTO DIA ' + \
            datetime.now().date().strftime('%d/%m/%Y')
        context['add_url'] = reverse_lazy('djangosige.apps.compras:addorcamentocompraview')
        return context

    def get_queryset(self):
        return OrcamentoCompra.objects.filter(data_vencimento=datetime.now().date(), status='0')


class PedidoCompraListView(CompraListView):
    template_name = 'compras/pedido_compra/pedido_compra_list.html'
    model = PedidoCompra
    context_object_name = 'all_pedidos'
    success_url = reverse_lazy('djangosige.apps.compras:listapedidocompraview')
    permission_codename = 'view_pedidocompra'

    def view_context(self, context):
        context['title_complete'] = 'PEDIDOS DE COMPRA'
        context['add_url'] = reverse_lazy('djangosige.apps.compras:addpedidocompraview')
        return context


class PedidoCompraAtrasadosListView(PedidoCompraListView):
    success_url = reverse_lazy('djangosige.apps.compras:listapedidocompraatrasadosview')

    def view_context(self, context):
        context['title_complete'] = 'PEDIDOS DE COMPRA ATRASADOS'
        context['add_url'] = reverse_lazy('djangosige.apps.compras:addpedidocompraview')
        return context

    def get_queryset(self):
        return PedidoCompra.objects.filter(data_entrega__lte=datetime.now().date(), status='0')


class PedidoCompraEntregaHojeListView(PedidoCompraListView):
    success_url = reverse_lazy('djangosige.apps.compras:listapedidocomprahojeview')

    def view_context(self, context):
        context['title_complete'] = 'PEDIDOS DE COMPRA COM ENTREGA DIA ' + \
            datetime.now().date().strftime('%d/%m/%Y')
        context['add_url'] = reverse_lazy('djangosige.apps.compras:addpedidocompraview')
        return context

    def get_queryset(self):
        return PedidoCompra.objects.filter(data_entrega=datetime.now().date(), status='0')


class EditarCompraView(CustomUpdateView):

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(EditarCompraView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get(self, request, form_class, *args, **kwargs):

        form = form = self.get_form(form_class)
        produtos_form = ItensCompraFormSet(
            instance=self.object, prefix='produtos_form')
        itens_list = ItensCompra.objects.filter(compra_id=self.object.id)
        produtos_form.initial = [{'total_sem_desconto': item.get_total_sem_desconto(),
                                  'total_impostos': item.get_total_impostos(),
                                  'total_com_impostos': item.get_total_com_impostos()} for item in itens_list]

        pagamento_form = PagamentoFormSet(
            instance=self.object, prefix='pagamento_form')

        itens_compra = ItensCompra.objects.filter(compra_id=self.object.pk)
        pagamentos = Pagamento.objects.filter(compra_id=self.object.pk)

        if len(itens_compra):
            produtos_form.extra = 0
        if len(pagamentos):
            pagamento_form.extra = 0

        return self.render_to_response(self.get_context_data(form=form,
                                                             produtos_form=produtos_form,
                                                             pagamento_form=pagamento_form))

    def post(self, request, form_class, *args, **kwargs):
        # Tirar . dos campos decimais
        req_post = request.POST.copy()

        for key in req_post:
            if ('desconto' in key or
                'quantidade' in key or
                'valor' in key or
                'frete' in key or
                'despesas' in key or
                'seguro' in key or
                    'total' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        form = self.get_form(form_class)
        produtos_form = ItensCompraFormSet(
            request.POST, prefix='produtos_form', instance=self.object)
        pagamento_form = PagamentoFormSet(
            request.POST, prefix='pagamento_form', instance=self.object)

        if (form.is_valid() and produtos_form.is_valid() and pagamento_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()

            for pform in produtos_form:
                if pform.cleaned_data != {}:
                    itens_compra_obj = pform.save(commit=False)
                    itens_compra_obj.compra_id = self.object
                    itens_compra_obj.save()

            pagamento_form.instance = self.object
            pagamento_form.save()

            return self.form_valid(form)

        return self.form_invalid(form=form,
                                 produtos_form=produtos_form,
                                 pagamento_form=pagamento_form)


class EditarOrcamentoCompraView(EditarCompraView):
    form_class = OrcamentoCompraForm
    model = OrcamentoCompra
    template_name = "compras/orcamento_compra/orcamento_compra_edit.html"
    success_url = reverse_lazy('djangosige.apps.compras:listaorcamentocompraview')
    success_message = "<b>Orçamento de compra %(id)s </b>editado com sucesso."
    permission_codename = 'change_orcamentocompra'

    def view_context(self, context):
        context['title_complete'] = 'EDITAR ORÇAMENTO DE COMPRA N°' + \
            str(self.object.id)
        context['return_url'] = reverse_lazy(
            'djangosige.apps.compras:listaorcamentocompraview')
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarOrcamentoCompraView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarOrcamentoCompraView, self).post(request, form_class, *args, **kwargs)


class EditarPedidoCompraView(EditarCompraView):
    form_class = PedidoCompraForm
    model = PedidoCompra
    template_name = "compras/pedido_compra/pedido_compra_edit.html"
    success_url = reverse_lazy('djangosige.apps.compras:listapedidocompraview')
    success_message = "<b>Pedido de compra %(id)s </b>editado com sucesso."
    permission_codename = 'change_pedidocompra'

    def view_context(self, context):
        context['title_complete'] = 'EDITAR PEDIDO DE COMPRA N°' + \
            str(self.object.id)
        context['return_url'] = reverse_lazy('djangosige.apps.compras:listapedidocompraview')
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarPedidoCompraView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarPedidoCompraView, self).post(request, form_class, *args, **kwargs)


class GerarPedidoCompraView(CustomView):
    permission_codename = ['add_pedidocompra', 'change_pedidocompra', ]

    def get(self, request, *args, **kwargs):
        orcamento_id = kwargs.get('pk', None)
        orcamento = OrcamentoCompra.objects.get(id=orcamento_id)
        itens_compra = orcamento.itens_compra.all()
        pagamentos = orcamento.parcela_pagamento.all()
        novo_pedido = PedidoCompra()

        for field in orcamento._meta.fields:
            setattr(novo_pedido, field.name, getattr(orcamento, field.name))

        novo_pedido.compra_ptr = None
        novo_pedido.pk = None
        novo_pedido.id = None
        novo_pedido.status = '0'
        orcamento.status = '1'  # Baixado
        orcamento.save()
        novo_pedido.orcamento = orcamento
        novo_pedido.save()

        for item in itens_compra:
            item.pk = None
            item.id = None
            item.save()
            novo_pedido.itens_compra.add(item)

        for pagamento in pagamentos:
            pagamento.pk = None
            pagamento.id = None
            pagamento.save()
            novo_pedido.parcela_pagamento.add(pagamento)

        return redirect(reverse_lazy('djangosige.apps.compras:editarpedidocompraview', kwargs={'pk': novo_pedido.id}))


class CancelarOrcamentoCompraView(CustomView):
    permission_codename = 'change_orcamentocompra'

    def get(self, request, *args, **kwargs):
        compra_id = kwargs.get('pk', None)
        instance = OrcamentoCompra.objects.get(id=compra_id)
        instance.status = '2'
        instance.save()
        return redirect(reverse_lazy('djangosige.apps.compras:editarorcamentocompraview', kwargs={'pk': instance.id}))


class CancelarPedidoCompraView(CustomView):
    permission_codename = 'change_pedidocompra'

    def get(self, request, *args, **kwargs):
        compra_id = kwargs.get('pk', None)
        instance = PedidoCompra.objects.get(id=compra_id)
        instance.status = '2'
        instance.save()
        return redirect(reverse_lazy('djangosige.apps.compras:editarpedidocompraview', kwargs={'pk': instance.id}))


class GerarCopiaCompraView(CustomView):

    def get(self, request, instance, redirect_url, *args, **kwargs):
        itens_compra = instance.itens_compra.all()
        pagamentos = instance.parcela_pagamento.all()

        instance.pk = None
        instance.id = None
        instance.status = '0'
        instance.save()

        for item in itens_compra:
            item.pk = None
            item.id = None
            item.save()
            instance.itens_compra.add(item)

        for pagamento in pagamentos:
            pagamento.pk = None
            pagamento.id = None
            pagamento.save()
            instance.parcela_pagamento.add(pagamento)

        return redirect(reverse_lazy(redirect_url, kwargs={'pk': instance.id}))


class GerarCopiaOrcamentoCompraView(GerarCopiaCompraView):
    permission_codename = 'add_orcamentocompra'

    def get(self, request, *args, **kwargs):
        compra_id = kwargs.get('pk', None)
        instance = OrcamentoCompra.objects.get(id=compra_id)
        redirect_url = 'djangosige.apps.compras:editarorcamentocompraview'
        return super(GerarCopiaOrcamentoCompraView, self).get(request, instance, redirect_url, *args, **kwargs)


class GerarCopiaPedidoCompraView(GerarCopiaCompraView):
    permission_codename = 'add_pedidocompra'

    def get(self, request, *args, **kwargs):
        compra_id = kwargs.get('pk', None)
        instance = PedidoCompra.objects.get(id=compra_id)
        redirect_url = 'djangosige.apps.compras:editarpedidocompraview'
        return super(GerarCopiaPedidoCompraView, self).get(request, instance, redirect_url, *args, **kwargs)


class ReceberPedidoCompraView(CustomView):
    permission_codename = 'change_pedidocompra'

    def get(self, request, *args, **kwargs):
        compra_id = kwargs.get('pk', None)
        pedido = PedidoCompra.objects.get(id=compra_id)
        lista_prod_estocado = []
        lista_itens_entrada = []

        if pedido.movimentar_estoque:
            for item in pedido.itens_compra.all():
                if item.produto.controlar_estoque:
                    prod_estocado = ProdutoEstocado.objects.get_or_create(
                        local=pedido.local_dest, produto=item.produto)[0]
                    item_mvmt = ItensMovimento()

                    prod_estocado.produto.estoque_atual += item.quantidade
                    prod_estocado.quantidade += item.quantidade

                    item_mvmt.produto = item.produto
                    item_mvmt.quantidade = item.quantidade
                    item_mvmt.valor_unit = item.valor_unit
                    item_mvmt.subtotal = item.vprod

                    lista_prod_estocado.append(prod_estocado)
                    lista_itens_entrada.append(item_mvmt)

            entrada_estoque = EntradaEstoque()
            if pedido.data_entrega:
                entrada_estoque.data_movimento = pedido.data_entrega
            else:
                entrada_estoque.data_movimento = datetime.now().date()

            entrada_estoque.quantidade_itens = pedido.itens_compra.count()
            entrada_estoque.observacoes = 'Entrada de estoque pelo pedido de compra nº{}'.format(
                str(pedido.id))
            entrada_estoque.tipo_movimento = u'1'
            entrada_estoque.valor_total = pedido.get_total_produtos_estoque()
            entrada_estoque.pedido_compra = pedido
            entrada_estoque.local_dest = pedido.local_dest

            entrada_estoque.save()

            for i in lista_itens_entrada:
                i.movimento_id = entrada_estoque
                i.save()

            for p in lista_prod_estocado:
                p.produto.save()
                p.save()

        pedido.status = u'4'
        pedido.save()

        messages.success(
            request, "<b>Pedido de compra {0} </b>recebido com sucesso.".format(str(pedido.id)))

        return redirect(reverse_lazy('djangosige.apps.compras:listapedidocompraview'))


class GerarPDFCompra(CustomView):

    def gerar_pdf(self, title, compra, user_id):
        resp = HttpResponse(content_type='application/pdf')

        compra_pdf = io.BytesIO()
        compra_report = CompraReport(queryset=[compra, ])
        compra_report.title = title

        compra_report.band_page_footer = compra_report.banda_foot

        try:
            usuario = Usuario.objects.get(pk=user_id)
            m_empresa = MinhaEmpresa.objects.get(m_usuario=usuario)
            flogo = m_empresa.m_empresa.logo_file
            logo_path = '{0}{1}'.format(MEDIA_ROOT, flogo.name)
            if flogo != 'imagens/logo.png':
                compra_report.topo_pagina.inserir_logo(logo_path)

            compra_report.band_page_footer.inserir_nome_empresa(
                m_empresa.m_empresa.nome_razao_social)
            if m_empresa.m_empresa.endereco_padrao:
                compra_report.band_page_footer.inserir_endereco_empresa(
                    m_empresa.m_empresa.endereco_padrao.format_endereco_completo)
            if m_empresa.m_empresa.telefone_padrao:
                compra_report.band_page_footer.inserir_telefone_empresa(
                    m_empresa.m_empresa.telefone_padrao.telefone)
        except:
            pass

        compra_report.topo_pagina.inserir_data_emissao(compra.data_emissao)
        if isinstance(compra, OrcamentoCompra):
            compra_report.topo_pagina.inserir_data_validade(
                compra.data_vencimento)
        elif isinstance(compra, PedidoCompra):
            compra_report.topo_pagina.inserir_data_entrega(compra.data_entrega)
        compra_report.band_page_header = compra_report.topo_pagina

        if compra.fornecedor.tipo_pessoa == 'PJ':
            compra_report.dados_fornecedor.inserir_informacoes_pj()
        elif compra.fornecedor.tipo_pessoa == 'PF':
            compra_report.dados_fornecedor.inserir_informacoes_pf()

        if compra.fornecedor.endereco_padrao:
            compra_report.dados_fornecedor.inserir_informacoes_endereco()
        if compra.fornecedor.telefone_padrao:
            compra_report.dados_fornecedor.inserir_informacoes_telefone()
        if compra.fornecedor.email_padrao:
            compra_report.dados_fornecedor.inserir_informacoes_email()

        compra_report.band_page_header.child_bands.append(
            compra_report.dados_fornecedor)

        compra_report.dados_produtos.band_detail.set_band_height(
            len(ItensCompra.objects.filter(compra_id=compra)))
        compra_report.banda_produtos.elements.append(
            compra_report.dados_produtos)
        compra_report.band_page_header.child_bands.append(
            compra_report.banda_produtos)

        compra_report.band_page_header.child_bands.append(
            compra_report.totais_venda)

        if compra.cond_pagamento:
            compra_report.banda_pagamento.elements.append(
                compra_report.dados_pagamento)
            compra_report.band_page_header.child_bands.append(
                compra_report.banda_pagamento)

        compra_report.band_page_header.child_bands.append(
            compra_report.observacoes)

        compra_report.generate_by(PDFGenerator, filename=compra_pdf)
        pdf = compra_pdf.getvalue()
        resp.write(pdf)

        return resp


class GerarPDFOrcamentoCompra(GerarPDFCompra):
    permission_codename = 'change_orcamentocompra'

    def get(self, request, *args, **kwargs):
        compra_id = kwargs.get('pk', None)

        if not compra_id:
            return HttpResponse('Objeto não encontrado.')

        obj = OrcamentoCompra.objects.get(pk=compra_id)
        title = 'Orçamento de compra nº {}'.format(compra_id)

        return self.gerar_pdf(title, obj, request.user.id)


class GerarPDFPedidoCompra(GerarPDFCompra):
    permission_codename = 'change_pedidocompra'

    def get(self, request, *args, **kwargs):
        compra_id = kwargs.get('pk', None)

        if not compra_id:
            return HttpResponse('Objeto não encontrado.')

        obj = PedidoCompra.objects.get(pk=compra_id)
        title = 'Pedido de compra nº {}'.format(compra_id)

        return self.gerar_pdf(title, obj, request.user.id)
