# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, View
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core import serializers

from djangosige.apps.vendas.forms import OrcamentoVendaForm, PedidoVendaForm, ItensVendaFormSet, PagamentoFormSet
from djangosige.apps.vendas.models import OrcamentoVenda, PedidoVenda, ItensVenda, Pagamento
from djangosige.apps.cadastro.models import Pessoa, Cliente, Transportadora, Produto, MinhaEmpresa
from djangosige.apps.fiscal.models import ICMS, ICMSSN, IPI, ICMSUFDest
from djangosige.apps.estoque.models import SaidaEstoque, ProdutoEstocado
from djangosige.apps.login.models import Usuario
from djangosige.configs.settings import MEDIA_ROOT

from geraldo.generators import PDFGenerator
from datetime import datetime
import io
import json

from .report_vendas import VendaReport


class AdicionarVendaView(CreateView):
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)
    
    def get_context_data(self, **kwargs):
        context = super(AdicionarVendaView, self).get_context_data(**kwargs)
        return self.view_context(context)
        
    def get(self, request, form_class, *args, **kwargs):
        self.object = None
        
        form = self.get_form(form_class)
        form.initial['vendedor'] = request.user.first_name or request.user
        form.initial['data_emissao'] = datetime.today().strftime('%d/%m/%Y')
        
        produtos_form = ItensVendaFormSet(prefix='produtos_form')
        pagamento_form = PagamentoFormSet(prefix='pagamento_form')
        
        return self.render_to_response(self.get_context_data(form=form, produtos_form=produtos_form, pagamento_form=pagamento_form))
    
    def post(self, request, form_class, *args, **kwargs):
        self.object = None
        ##Tirar . dos campos decimais
        req_post = request.POST.copy()
        
        for key,value in req_post.items():
            if ('desconto' in key or
            'quantidade' in key or
            'valor' in key or
            'frete' in key or
            'despesas' in key or
            'seguro' in key or
            'total' in key):
                req_post[key] = req_post[key].replace('.','')
                
        request.POST = req_post
        
        form = self.get_form(form_class)
        produtos_form = ItensVendaFormSet(request.POST, prefix='produtos_form')
        pagamento_form = PagamentoFormSet(request.POST, prefix='pagamento_form')
        
        if (form.is_valid() and produtos_form.is_valid() and pagamento_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()
            
            for pform in produtos_form:
                if pform.cleaned_data != {}:
                    itens_venda_obj = pform.save(commit=False)
                    itens_venda_obj.venda_id = self.object
                    itens_venda_obj.calcular_pis_cofins()
                    itens_venda_obj.save()
            
            pagamento_form.instance = self.object
            pagamento_form.save()
            
            return self.form_valid(form)
        
        return self.form_invalid(form, produtos_form, pagamento_form)
            
    def form_valid(self, form):
        super(AdicionarVendaView, self).form_valid(form)
        messages.success(self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)
    
    def form_invalid(self, form, produtos_form, pagamento_form):
        return self.render_to_response(self.get_context_data(form=form, produtos_form=produtos_form, pagamento_form=pagamento_form, invalid=True))


class AdicionarOrcamentoVendaView(AdicionarVendaView):
    form_class = OrcamentoVendaForm
    template_name = "vendas/orcamento_venda/orcamento_venda_add.html"
    success_url = reverse_lazy('vendas:listaorcamentovendaview')
    success_message = "<b>Orçamento de venda %(id)s </b>adicionado com sucesso."
    
    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR ORÇAMENTO DE VENDA'
        context['return_url'] = reverse_lazy('vendas:listaorcamentovendaview')
        return context
    
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarOrcamentoVendaView, self).get(request, form_class, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarOrcamentoVendaView, self).post(request, form_class, *args, **kwargs)
        

class AdicionarPedidoVendaView(AdicionarVendaView):
    form_class = PedidoVendaForm
    template_name = "vendas/pedido_venda/pedido_venda_add.html"
    success_url = reverse_lazy('vendas:listapedidovendaview')
    success_message = "<b>Pedido de venda %(id)s </b>adicionado com sucesso."
    
    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR PEDIDO DE VENDA'
        context['return_url'] = reverse_lazy('vendas:listapedidovendaview')
        return context
    
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarPedidoVendaView, self).get(request, form_class, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarPedidoVendaView, self).post(request, form_class, *args, **kwargs)


class VendaListView(ListView):
    def get_queryset(self, object):
        return object.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(VendaListView, self).get_context_data(**kwargs)
        return self.view_context(context)
    
    def post(self, request, object, *args, **kwargs):
        for key, value in request.POST.items():
            if value=="on":
                instance = object.objects.get(id=key)
                instance.delete()
        return redirect(self.success_url)
        
        
class OrcamentoVendaListView(VendaListView):
    template_name = 'vendas/orcamento_venda/orcamento_venda_list.html'
    model = OrcamentoVenda
    context_object_name = 'all_orcamentos'
    success_url = reverse_lazy('vendas:listaorcamentovendaview')
    
    def view_context(self, context):
        context['title_complete'] = 'ORÇAMENTOS DE VENDA'
        context['add_url'] = reverse_lazy('vendas:addorcamentovendaview')
        return context
    
    def get_queryset(self):
        return super(OrcamentoVendaListView, self).get_queryset(object=OrcamentoVenda)
    
    def post(self, request, *args, **kwargs):
        return super(OrcamentoVendaListView, self).post(request, OrcamentoVenda)
        
        
class OrcamentoVendaVencidosListView(VendaListView):
    template_name = 'vendas/orcamento_venda/orcamento_venda_list.html'
    model = OrcamentoVenda
    context_object_name = 'all_orcamentos'
    success_url = reverse_lazy('vendas:listaorcamentovendavencidoview')
    
    def view_context(self, context):
        context['title_complete'] = 'ORÇAMENTOS DE VENDA VENCIDOS'
        context['add_url'] = reverse_lazy('vendas:addorcamentovendaview')
        return context
    
    def get_queryset(self):
        return OrcamentoVenda.objects.filter(data_vencimento__lte=datetime.now().date(), status='0')
    
    def post(self, request, *args, **kwargs):
        return super(OrcamentoVendaVencidosListView, self).post(request, OrcamentoVenda)

        
class OrcamentoVendaVencimentoHojeListView(OrcamentoVendaVencidosListView):
    success_url = reverse_lazy('vendas:listaorcamentovendahojeview')
    def view_context(self, context):
        context['title_complete'] = 'ORÇAMENTOS DE VENDA COM VENCIMENTO DIA ' + datetime.now().date().strftime('%d/%m/%Y')
        context['add_url'] = reverse_lazy('vendas:addorcamentovendaview')
        return context
    
    def get_queryset(self):
        return OrcamentoVenda.objects.filter(data_vencimento=datetime.now().date(), status='0')
    
        
class PedidoVendaListView(VendaListView):
    template_name = 'vendas/pedido_venda/pedido_venda_list.html'
    model = PedidoVenda
    context_object_name = 'all_pedidos'
    success_url = reverse_lazy('vendas:listapedidovendaview')
    
    def view_context(self, context):
        context['title_complete'] = 'PEDIDOS DE VENDA'
        context['add_url'] = reverse_lazy('vendas:addpedidovendaview')
        return context
    
    def get_queryset(self):
        return super(PedidoVendaListView, self).get_queryset(object=PedidoVenda)
    
    def post(self, request, *args, **kwargs):
        return super(PedidoVendaListView, self).post(request, PedidoVenda)
        

class PedidoVendaAtrasadosListView(VendaListView):
    template_name = 'vendas/pedido_venda/pedido_venda_list.html'
    model = PedidoVenda
    context_object_name = 'all_pedidos'
    success_url = reverse_lazy('vendas:listapedidovendaatrasadosview')
    
    def view_context(self, context):
        context['title_complete'] = 'PEDIDOS DE VENDA ATRASADOS'
        context['add_url'] = reverse_lazy('vendas:addpedidovendaview')
        return context
    
    def get_queryset(self):
        return PedidoVenda.objects.filter(data_entrega__lte=datetime.now().date(), status='0')
    
    def post(self, request, *args, **kwargs):
        return super(PedidoVendaAtrasadosListView, self).post(request, PedidoVenda)
        
        
class PedidoVendaEntregaHojeListView(PedidoVendaAtrasadosListView):
    success_url = reverse_lazy('vendas:listapedidovendahojeview')
    def view_context(self, context):
        context['title_complete'] = 'PEDIDOS DE VENDA COM ENTREGA DIA ' + datetime.now().date().strftime('%d/%m/%Y')
        context['add_url'] = reverse_lazy('vendas:addpedidovendaview')
        return context
    
    def get_queryset(self):
        return PedidoVenda.objects.filter(data_entrega=datetime.now().date(), status='0')
    
        
class EditarVendaView(UpdateView):
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)
        
    def get_context_data(self, **kwargs):
        context = super(EditarVendaView, self).get_context_data(**kwargs)
        return self.view_context(context)
    
    def get(self, request, form_class, *args, **kwargs):
        
        form = form = self.get_form(form_class)
        form.initial['total_sem_imposto'] = self.object.get_total_sem_imposto()
        
        produtos_form = ItensVendaFormSet(instance=self.object, prefix='produtos_form')
        itens_list = ItensVenda.objects.filter(venda_id=self.object.id)
        produtos_form.initial = [{'total_sem_desconto': item.get_total_sem_desconto(), 
                                  'total_impostos': item.get_total_impostos(),
                                  'total_com_impostos': item.get_total_com_impostos()} for item in itens_list]
        
        pagamento_form = PagamentoFormSet(instance=self.object, prefix='pagamento_form')
        
        if ItensVenda.objects.filter(venda_id=self.object.pk).count():
            produtos_form.extra = 0
        if Pagamento.objects.filter(venda_id=self.object.pk).count():
            pagamento_form.extra = 0
        
        return self.render_to_response(self.get_context_data(form=form, produtos_form=produtos_form, pagamento_form=pagamento_form))
    
    def post(self, request, form_class, *args, **kwargs):
        ##Tirar . dos campos decimais
        req_post = request.POST.copy()
        
        for key,value in req_post.items():
            if ('desconto' in key or 
            'quantidade' in key or
            'valor' in key or
            'frete' in key or
            'despesas' in key or
            'seguro' in key or
            'total' in key):                    
                req_post[key] = req_post[key].replace('.','')
                
        request.POST = req_post
        
        form = self.get_form(form_class)
        produtos_form = ItensVendaFormSet(request.POST, prefix='produtos_form', instance=self.object)
        pagamento_form = PagamentoFormSet(request.POST, prefix='pagamento_form', instance=self.object)
        
        if (form.is_valid() and produtos_form.is_valid() and pagamento_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()
            
            for pform in produtos_form:
                if pform.cleaned_data != {}:
                    itens_venda_obj = pform.save(commit=False)
                    itens_venda_obj.venda_id = self.object
                    itens_venda_obj.calcular_pis_cofins()
                    itens_venda_obj.save()
            
            pagamento_form.instance = self.object
            pagamento_form.save()
            
            return self.form_valid(form)
        
        return self.form_invalid(form, produtos_form, pagamento_form)
            
    def form_valid(self, form):
        super(EditarVendaView, self).form_valid(form)
        messages.success(self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)
    
    def form_invalid(self, form, produtos_form, pagamento_form):
        return self.render_to_response(self.get_context_data(form=form, produtos_form=produtos_form, pagamento_form=pagamento_form))

        
class EditarOrcamentoVendaView(EditarVendaView):
    form_class = OrcamentoVendaForm
    model = OrcamentoVenda
    template_name = "vendas/orcamento_venda/orcamento_venda_edit.html"
    success_url = reverse_lazy('vendas:listaorcamentovendaview')
    success_message = "<b>Orçamento de venda %(id)s </b>editado com sucesso."
    
    def view_context(self, context):
        context['title_complete'] = 'EDITAR ORÇAMENTO DE VENDA N°' + str(self.object.id)
        context['return_url'] = reverse_lazy('vendas:listaorcamentovendaview')
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()        
        return super(EditarOrcamentoVendaView, self).get(request, form_class, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()        
        return super(EditarOrcamentoVendaView, self).post(request, form_class, *args, **kwargs)
        
        
class EditarPedidoVendaView(EditarVendaView):
    form_class = PedidoVendaForm
    model = PedidoVenda
    template_name = "vendas/pedido_venda/pedido_venda_edit.html"
    success_url = reverse_lazy('vendas:listapedidovendaview')
    success_message = "<b>Pedido de venda %(id)s </b>editado com sucesso."
    
    def view_context(self, context):
        context['title_complete'] = 'EDITAR PEDIDO DE VENDA N°' + str(self.object.id)
        context['return_url'] = reverse_lazy('vendas:listapedidovendaview')
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarPedidoVendaView, self).get(request, form_class, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarPedidoVendaView, self).post(request, form_class, *args, **kwargs)
    
    
class InfoCliente(View):
    def post(self, request, *args, **kwargs):
        obj_list = []
        pessoa  = Pessoa.objects.get(pk=request.POST['pessoaId'])
        cliente = Cliente.objects.get(pk=request.POST['pessoaId'])
        obj_list.append(cliente)
        
        if pessoa.endereco_padrao:
            obj_list.append(pessoa.endereco_padrao)
        if pessoa.email_padrao:
            obj_list.append(pessoa.email_padrao)
        if pessoa.telefone_padrao:
            obj_list.append(pessoa.telefone_padrao)
        
        if pessoa.tipo_pessoa == 'PJ':
            obj_list.append(pessoa.pessoa_jur_info)
        elif pessoa.tipo_pessoa == 'PF':
            obj_list.append(pessoa.pessoa_fis_info)
        
        data = serializers.serialize('json', obj_list, fields=('indicador_ie', 'limite_de_credito', 'cnpj', 'inscricao_estadual', 'responsavel', 'cpf', 'rg', 'id_estrangeiro', 'logradouro', 'numero', 'bairro', 
            'municipio', 'cmun', 'uf', 'pais', 'complemento', 'cep', 'email', 'telefone',))
            
        return HttpResponse(data, content_type='application/json')
        

class InfoTransportadora(View):
    def post(self, request, *args, **kwargs):
        veiculos  = Transportadora.objects.get(pk=request.POST['transportadoraId']).veiculo.all()
        data = serializers.serialize('json', veiculos, fields=('id', 'descricao',))
        
        return HttpResponse(data, content_type='application/json')
        
        
class InfoProduto(View):   
    def get(self, request, *args, **kwargs):
        try:
            data = serializers.serialize('json', Produto.objects.all())
        except:
            data = ""
            
        return HttpResponse(data, content_type='application/json')
        
    def post(self, request, *args, **kwargs):
        obj_list = []
        pro = Produto.objects.get(pk=request.POST['produtoId'])
        obj_list.append(pro)
        
        if pro.grupo_fiscal:
            if pro.grupo_fiscal.regime_trib == '0':
                icms, created = ICMS.objects.get_or_create(grupo_fiscal=pro.grupo_fiscal)
            else:
                icms, created = ICMSSN.objects.get_or_create(grupo_fiscal=pro.grupo_fiscal)
            
            ipi, created = IPI.objects.get_or_create(grupo_fiscal=pro.grupo_fiscal)
            icms_dest, created = ICMSUFDest.objects.get_or_create(grupo_fiscal=pro.grupo_fiscal)
            obj_list.append(icms)
            obj_list.append(ipi)
            obj_list.append(icms_dest)
                
        data = serializers.serialize('json', obj_list, fields=('venda', 'controlar_estoque', 'estoque_atual',
            'tipo_ipi', 'p_ipi', 'valor_fixo', 'p_icms', 'p_red_bc', 'p_icmsst', 'p_red_bcst', 'p_mvast',
            'p_fcp_dest', 'p_icms_dest', 'p_icms_inter', 'p_icms_inter_part',
            'ipi_incluido_preco', 'incluir_bc_icms', 'incluir_bc_icmsst', 'icmssn_incluido_preco', 
            'icmssnst_incluido_preco', 'icms_incluido_preco', 'icmsst_incluido_preco'))
        return HttpResponse(data, content_type='application/json')
        
        
class InfoVenda(View):
    def post(self, request, *args, **kwargs):
        venda  = PedidoVenda.objects.get(pk=request.POST['vendaId'])
        itens_venda = venda.itens_venda.all()
        pagamentos = venda.parcela_pagamento.all()
        data = []
        
        pedido_dict = {}
        pedido_dict['model'] = 'vendas.pedidovenda'
        pedido_dict['pk'] = venda.id
        pedido_fields_dict = {}
        pedido_fields_dict['dest'] = venda.cliente.id
        pedido_fields_dict['local'] = venda.get_local_orig_id()
        pedido_fields_dict['status'] = venda.get_status_display()
        pedido_fields_dict['desconto'] = venda.format_desconto()
        pedido_fields_dict['frete'] = venda.format_frete()
        pedido_fields_dict['despesas'] = venda.format_despesas()
        pedido_fields_dict['seguro'] = venda.format_seguro()
        pedido_fields_dict['impostos'] = venda.format_impostos()
        pedido_fields_dict['valor_total'] = venda.format_valor_total()
        pedido_fields_dict['total_sem_desconto'] = venda.format_total_sem_desconto()
        pedido_fields_dict['ind_final'] = venda.ind_final
        pedido_fields_dict['forma_pag'] = venda.get_forma_pagamento()
        pedido_fields_dict['n_itens'] = str(len(itens_venda))
        pedido_fields_dict['valor_total_produtos'] = venda.format_total_produtos()
        
        if venda.cond_pagamento:
            pedido_fields_dict['n_parcelas'] = venda.cond_pagamento.n_parcelas
        else:
            pedido_fields_dict['n_parcelas'] = 1
        
        pedido_dict['fields'] = pedido_fields_dict
        
        data.append(pedido_dict)
        
        for item in itens_venda:
            itens_venda_dict = {}
            itens_venda_dict['model'] = 'vendas.itensvenda'
            itens_venda_dict['pk'] = item.id
            itens_fields_dict = {}
            itens_hidden_fields_dict = {}
            itens_editable_fields_dict = {}
            itens_fields_dict['produto_id'] = item.produto.id
            itens_fields_dict['controlar_estoque'] = item.produto.controlar_estoque
            itens_fields_dict['produto'] = item.produto.descricao
            itens_hidden_fields_dict['codigo'] = item.produto.codigo
            itens_hidden_fields_dict['unidade'] = item.produto.get_sigla_unidade()
            itens_hidden_fields_dict['cfop'] = item.produto.get_cfop_padrao()
            itens_hidden_fields_dict['ncm'] = item.produto.ncm
            itens_fields_dict['quantidade'] = item.format_quantidade()
            itens_fields_dict['valor_unit'] = item.format_valor_unit()
            itens_fields_dict['desconto'] = item.format_desconto()
            itens_hidden_fields_dict['frete'] = item.format_valor_attr('valor_rateio_frete')
            itens_hidden_fields_dict['despesas'] = item.format_valor_attr('valor_rateio_despesas')
            itens_hidden_fields_dict['seguro'] = item.format_valor_attr('valor_rateio_seguro')
            itens_hidden_fields_dict['subtotal'] = item.format_valor_attr('subtotal')
            
            itens_fields_dict['impostos'] = item.format_total_impostos()
            itens_fields_dict['total'] = item.format_total_com_imposto()
            itens_fields_dict['vprod'] = item.format_vprod()
            
            itens_hidden_fields_dict['vicms'] = item.format_valor_attr('vicms')
            itens_hidden_fields_dict['vipi'] = item.format_valor_attr('vipi')
            itens_hidden_fields_dict['vicms_st'] = item.format_valor_attr('vicms_st')
            itens_hidden_fields_dict['vfcp'] = item.format_valor_attr('vfcp')
            itens_hidden_fields_dict['vicmsufdest'] = item.format_valor_attr('vicmsufdest')
            itens_hidden_fields_dict['vicmsufremet'] = item.format_valor_attr('vicmsufremet')
            itens_hidden_fields_dict['aliq_pis'] = item.get_aliquota_pis()
            itens_hidden_fields_dict['aliq_cofins'] = item.get_aliquota_cofins()
            itens_hidden_fields_dict['mot_des_icms'] = item.get_mot_deson_icms()
            
            itens_editable_fields_dict['editable_field_vq_bcpis'] = item.format_valor_attr('vq_bcpis')
            itens_editable_fields_dict['editable_field_vq_bccofins'] = item.format_valor_attr('vq_bccofins')
            #itens_editable_fields_dict['aliq_pis'] = item.get_aliquota_pis()
            #itens_editable_fields_dict['aliq_cofins'] = item.get_aliquota_cofins()
            itens_editable_fields_dict['editable_field_vpis'] = item.format_valor_attr('vpis')
            itens_editable_fields_dict['editable_field_vcofins'] = item.format_valor_attr('vcofins')
            itens_editable_fields_dict['editable_field_vicms_deson'] = item.format_valor_attr('vicms_deson')
            itens_editable_fields_dict['editable_field_inf_ad_prod'] = item.inf_ad_prod
                        
            itens_venda_dict['fields'] = itens_fields_dict
            itens_venda_dict['hidden_fields'] = itens_hidden_fields_dict
            itens_venda_dict['editable_fields'] = itens_editable_fields_dict
            
            data.append(itens_venda_dict)
        
        for pagamento in pagamentos:
            pagamento_dict = {}
            pagamento_dict['model'] = 'vendas.pagamento'
            pagamento_dict['pk'] = pagamento.id
            pagamento_fields_dict = {}
            pagamento_fields_dict['id'] = pagamento.id
            pagamento_fields_dict['vencimento'] = pagamento.format_vencimento
            pagamento_fields_dict['valor_parcela'] = pagamento.format_valor_parcela
            
            pagamento_dict['fields'] = pagamento_fields_dict
            
            data.append(pagamento_dict)
        
        #return HttpResponse(data, content_type='application/json')
        return HttpResponse(json.dumps(data), content_type='application/json')
        
        
class GerarPedidoVendaView(View):
    def get(self, request, *args, **kwargs):
        orcamento_id = kwargs.get('pk', None)
        orcamento = OrcamentoVenda.objects.get(id=orcamento_id)
        itens_venda = orcamento.itens_venda.all()
        pagamentos = orcamento.parcela_pagamento.all()
        novo_pedido = PedidoVenda()
        
        for field in orcamento._meta.fields:
            setattr(novo_pedido, field.name, getattr(orcamento, field.name))
            
        novo_pedido.venda_ptr = None
        novo_pedido.pk = None
        novo_pedido.id = None
        novo_pedido.status = '0'
        orcamento.status = '1' #Baixado
        orcamento.save()
        novo_pedido.orcamento = orcamento
        novo_pedido.save()
        
        for item in itens_venda:
            item.pk = None
            item.id = None
            item.save()
            novo_pedido.itens_venda.add(item)
            
        for pagamento in pagamentos:
            pagamento.pk = None
            pagamento.id = None
            pagamento.save()
            novo_pedido.parcela_pagamento.add(pagamento)
            
        return redirect(reverse_lazy('vendas:editarpedidovendaview', kwargs={'pk':novo_pedido.id}))
        

class CancelarVendaView(View):
    def get(self, request, *args, **kwargs):
        venda_id = kwargs.get('pk', None)
        venda = None
        try:
           venda = PedidoVenda.objects.get(id=venda_id)
        except PedidoVenda.DoesNotExist:
           venda = OrcamentoVenda.objects.get(id=venda_id)
        venda.status = '2'
        venda.save()
        
        return redirect(request.META.get('HTTP_REFERER'))
        
        
class GerarCopiaVendaView(View):
    def get(self, request, *args, **kwargs):
        venda_id = kwargs.get('pk', None)
        if PedidoVenda.objects.filter(id=venda_id).exists():
            instance = PedidoVenda.objects.get(id=venda_id)
            redirect_url = 'vendas:editarpedidovendaview'
        else:
            instance = OrcamentoVenda.objects.get(id=venda_id)
            redirect_url = 'vendas:editarorcamentovendaview'
            
        itens_venda = instance.itens_venda.all()
        pagamentos = instance.parcela_pagamento.all()
        
        instance.pk = None
        instance.id = None
        instance.status = '0'
        instance.save()
        
        for item in itens_venda:
            item.pk = None
            item.id = None
            item.save()
            instance.itens_venda.add(item)
            
        for pagamento in pagamentos:
            pagamento.pk = None
            pagamento.id = None
            pagamento.save()
            instance.parcela_pagamento.add(pagamento)
            
        return redirect(reverse_lazy(redirect_url, kwargs={'pk':instance.id}))
        

class GerarPDFVenda(View):
    def gerar_pdf(self, title, venda, user_id):
        resp = HttpResponse(content_type='application/pdf')
        
        venda_pdf = io.BytesIO()
        venda_report = VendaReport(queryset=[venda,])
        venda_report.title = title
        
        venda_report.band_page_footer = venda_report.banda_foot
        
        try:
            usuario = Usuario.objects.get(pk=user_id)
            m_empresa = MinhaEmpresa.objects.get(m_usuario=usuario)
            flogo = m_empresa.m_empresa.logo_file
            logo_path = '{0}{1}'.format(MEDIA_ROOT, flogo.name)
            if flogo != 'imagens/logo.png':
                venda_report.topo_pagina.inserir_logo(logo_path)
            
            venda_report.band_page_footer.inserir_nome_empresa(m_empresa.m_empresa.nome_razao_social)
            if m_empresa.m_empresa.endereco_padrao:
                venda_report.band_page_footer.inserir_endereco_empresa(m_empresa.m_empresa.endereco_padrao.format_endereco_completo)
            if m_empresa.m_empresa.telefone_padrao:
                venda_report.band_page_footer.inserir_telefone_empresa(m_empresa.m_empresa.telefone_padrao.telefone)
        except:
            pass
        
        venda_report.topo_pagina.inserir_data_emissao(venda.data_emissao)
        if isinstance(venda, OrcamentoVenda):
            venda_report.topo_pagina.inserir_data_validade(venda.data_vencimento)
        elif isinstance(venda, PedidoVenda):
            venda_report.topo_pagina.inserir_data_entrega(venda.data_entrega)
        venda_report.band_page_header = venda_report.topo_pagina
        
        if venda.cliente.tipo_pessoa == 'PJ':
            venda_report.dados_cliente.inserir_informacoes_pj()
        elif venda.cliente.tipo_pessoa == 'PF':
            venda_report.dados_cliente.inserir_informacoes_pf()
        
        if venda.cliente.endereco_padrao:
            venda_report.dados_cliente.inserir_informacoes_endereco()
        if venda.cliente.telefone_padrao:
            venda_report.dados_cliente.inserir_informacoes_telefone()
        if venda.cliente.email_padrao:
            venda_report.dados_cliente.inserir_informacoes_email()
        
        venda_report.band_page_header.child_bands.append(venda_report.dados_cliente)
        
        venda_report.dados_produtos.band_detail.set_band_height(len(ItensVenda.objects.filter(venda_id=venda)))
        venda_report.banda_produtos.elements.append(venda_report.dados_produtos)
        venda_report.band_page_header.child_bands.append(venda_report.banda_produtos)
        
        venda_report.band_page_header.child_bands.append(venda_report.totais_venda)
        
        if venda.cond_pagamento:
            venda_report.banda_pagamento.elements.append(venda_report.dados_pagamento)
            venda_report.band_page_header.child_bands.append(venda_report.banda_pagamento)
        
        venda_report.observacoes.inserir_vendedor()
        venda_report.band_page_header.child_bands.append(venda_report.observacoes)
                
        venda_report.generate_by(PDFGenerator, filename=venda_pdf)
        pdf = venda_pdf.getvalue()
        resp.write(pdf)
        
        return resp
        
        
class GerarPDFOrcamentoVenda(GerarPDFVenda):
    def get(self, request, *args, **kwargs):
        venda_id = kwargs.get('pk', None)
        
        if not venda_id:
            return HttpResponse('Objeto não encontrado.')
                    
        obj = OrcamentoVenda.objects.get(pk=venda_id)
        title = 'Orçamento de venda nº {}'.format(venda_id)
        
        return self.gerar_pdf(title, obj, request.user.id)
                
        
        
class GerarPDFPedidoVenda(GerarPDFVenda):
    def get(self, request, *args, **kwargs):
        venda_id = kwargs.get('pk', None)
        
        if not venda_id:
            return HttpResponse('Objeto não encontrado.')
                    
        obj = PedidoVenda.objects.get(pk=venda_id)
        title = 'Pedido de venda nº {}'.format(venda_id)
        
        return self.gerar_pdf(title, obj, request.user.id)
