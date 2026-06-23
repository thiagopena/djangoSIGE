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

    def get_quantidade_cadastro(self):
        return {
            'clientes': Cliente.objects.count(),
            'fornecedores': Fornecedor.objects.count(),
            'produtos': Produto.objects.count(),
            'empresas': Empresa.objects.count(),
            'transportadoras': Transportadora.objects.count(),
        }

    def get_agenda_hoje(self, data_atual):
        return {
            'orcamento_venda_hoje': OrcamentoVenda.objects.filter(data_vencimento=data_atual, status='0').count(),
            'orcamento_compra_hoje': OrcamentoCompra.objects.filter(data_vencimento=data_atual, status='0').count(),
            'pedido_venda_hoje': PedidoVenda.objects.filter(data_entrega=data_atual, status='0').count(),
            'pedido_compra_hoje': PedidoCompra.objects.filter(data_entrega=data_atual, status='0').count(),
            'contas_receber_hoje': Entrada.objects.filter(data_vencimento=data_atual, status__in=['1', '2']).count(),
            'contas_pagar_hoje': Saida.objects.filter(data_vencimento=data_atual, status__in=['1', '2']).count(),
        }

    def get_alertas(self, data_atual):
        return {
            'produtos_baixo_estoque': Produto.objects.filter(estoque_atual__lte=F('estoque_minimo')).count(),
            'orcamentos_venda_vencidos': OrcamentoVenda.objects.filter(data_vencimento__lt=data_atual, status='0').count(),
            'pedidos_venda_atrasados': PedidoVenda.objects.filter(data_entrega__lt=data_atual, status='0').count(),
            'orcamentos_compra_vencidos': OrcamentoCompra.objects.filter(data_vencimento__lt=data_atual, status='0').count(),
            'pedidos_compra_atrasados': PedidoCompra.objects.filter(data_entrega__lt=data_atual, status='0').count(),
            'contas_receber_atrasadas': Entrada.objects.filter(data_vencimento__lt=data_atual, status__in=['1', '2']).count(),
            'contas_pagar_atrasadas': Saida.objects.filter(data_vencimento__lt=data_atual, status__in=['1', '2']).count(),
        }

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        data_atual = datetime.now().date()

        context.update({
            'data_atual': data_atual.strftime('%d/%m/%Y'),
            'quantidade_cadastro': self.get_quantidade_cadastro(),
            'agenda_hoje': self.get_agenda_hoje(data_atual),
            'alertas': self.get_alertas(data_atual),
        })

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
