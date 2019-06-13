# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from djangosige.apps.cadastro.models import Cliente, Fornecedor, Produto, Empresa, Transportadora
from djangosige.apps.vendas.models import OrcamentoVenda, PedidoVenda
from djangosige.apps.compras.models import OrcamentoCompra, PedidoCompra
from djangosige.apps.financeiro.models import MovimentoCaixa, Entrada, Saida

from datetime import datetime


class IndexView(TemplateView):
    template_name = 'base/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        quantidade_cadastro = {}
        agenda_hoje = {}
        alertas = {}
        data_atual = datetime.now().date()

        context['data_atual'] = data_atual.strftime('%d/%m/%Y')

        quantidade_cadastro['clientes'] = Cliente.objects.all().count()
        quantidade_cadastro['fornecedores'] = Fornecedor.objects.all().count()
        quantidade_cadastro['produtos'] = Produto.objects.all().count()
        quantidade_cadastro['empresas'] = Empresa.objects.all().count()
        quantidade_cadastro[
            'transportadoras'] = Transportadora.objects.all().count()
        context['quantidade_cadastro'] = quantidade_cadastro

        agenda_hoje['orcamento_venda_hoje'] = OrcamentoVenda.objects.filter(
            data_vencimento=data_atual, status='0').count()
        agenda_hoje['orcamento_compra_hoje'] = OrcamentoCompra.objects.filter(
            data_vencimento=data_atual, status='0').count()
        agenda_hoje['pedido_venda_hoje'] = PedidoVenda.objects.filter(
            data_entrega=data_atual, status='0').count()
        agenda_hoje['pedido_compra_hoje'] = PedidoCompra.objects.filter(
            data_entrega=data_atual, status='0').count()
        agenda_hoje['contas_receber_hoje'] = Entrada.objects.filter(
            data_vencimento=data_atual, status__in=['1', '2']).count()
        agenda_hoje['contas_pagar_hoje'] = Saida.objects.filter(
            data_vencimento=data_atual, status__in=['1', '2']).count()
        context['agenda_hoje'] = agenda_hoje

        alertas['produtos_baixo_estoque'] = Produto.objects.filter(
            estoque_atual__lte=F('estoque_minimo')).count()
        alertas['orcamentos_venda_vencidos'] = OrcamentoVenda.objects.filter(
            data_vencimento__lte=data_atual, status='0').count()
        alertas['pedidos_venda_atrasados'] = PedidoVenda.objects.filter(
            data_entrega__lte=data_atual, status='0').count()
        alertas['orcamentos_compra_vencidos'] = OrcamentoCompra.objects.filter(
            data_vencimento__lte=data_atual, status='0').count()
        alertas['pedidos_compra_atrasados'] = PedidoCompra.objects.filter(
            data_entrega__lte=data_atual, status='0').count()
        alertas['contas_receber_atrasadas'] = Entrada.objects.filter(
            data_vencimento__lte=data_atual, status__in=['1', '2']).count()
        alertas['contas_pagar_atrasadas'] = Saida.objects.filter(
            data_vencimento__lte=data_atual, status__in=['1', '2']).count()
        context['alertas'] = alertas

        try:
            context['movimento_dia'] = MovimentoCaixa.objects.get(
                data_movimento=data_atual)
        except (MovimentoCaixa.DoesNotExist, ObjectDoesNotExist):
            ultimo_mvmt = MovimentoCaixa.objects.filter(
                data_movimento__lt=data_atual)
            if ultimo_mvmt:
                context['saldo'] = ultimo_mvmt.latest(
                    'data_movimento').saldo_final
            else:
                context['saldo'] = '0,00'

        return context


def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
