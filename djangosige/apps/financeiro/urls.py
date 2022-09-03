# -*- coding: utf-8 -*-

from django.urls import re_path as url
from . import views

app_name = 'djangosige.apps.financeiro'
urlpatterns = [
    # Lancamentos
    # Gerar lancamento
    url(r'gerarlancamento/$', views.GerarLancamentoView.as_view(),
        name='gerarlancamento'),
    # Lista todos lancamentos
    url(r'lancamentos/$', views.LancamentoListView.as_view(),
        name='listalancamentoview'),

    # Contas a pagar
    # financeiro/contapagar/adicionar/
    url(r'contapagar/adicionar/$',
        views.AdicionarContaPagarView.as_view(), name='addcontapagarview'),
    # financeiro/contapagar/listacontapagar
    url(r'contapagar/listacontapagar/$',
        views.ContaPagarListView.as_view(), name='listacontapagarview'),
    # financeiro/contapagar/editar/
    url(r'contapagar/editar/(?P<pk>[0-9]+)/$',
        views.EditarContaPagarView.as_view(), name='editarcontapagarview'),
    # financeiro/contapagar/listacontapagar/atrasadas/
    url(r'contapagar/listacontapagar/atrasadas/$',
        views.ContaPagarAtrasadasListView.as_view(), name='listacontapagaratrasadasview'),
    # financeiro/contapagar/listacontapagar/hoje/
    url(r'contapagar/listacontapagar/hoje/$',
        views.ContaPagarHojeListView.as_view(), name='listacontapagarhojeview'),

    # Contas a receber
    # financeiro/contareceber/adicionar/
    url(r'contareceber/adicionar/$',
        views.AdicionarContaReceberView.as_view(), name='addcontareceberview'),
    # financeiro/contareceber/listacontapagar
    url(r'contareceber/listacontareceber/$',
        views.ContaReceberListView.as_view(), name='listacontareceberview'),
    # financeiro/contareceber/editar/
    url(r'contareceber/editar/(?P<pk>[0-9]+)/$',
        views.EditarContaReceberView.as_view(), name='editarcontareceberview'),
    # financeiro/contareceber/listacontapagar/atrasadas/
    url(r'contareceber/listacontareceber/atrasadas/$',
        views.ContaReceberAtrasadasListView.as_view(), name='listacontareceberatrasadasview'),
    # financeiro/contareceber/listacontapagar/hoje/
    url(r'contareceber/listacontareceber/hoje/$',
        views.ContaReceberHojeListView.as_view(), name='listacontareceberhojeview'),

    # Pagamentos
    # financeiro/pagamento/adicionar/
    url(r'pagamento/adicionar/$',
        views.AdicionarSaidaView.as_view(), name='addpagamentoview'),
    # financeiro/pagamento/listacontapagar
    url(r'pagamento/listapagamento/$',
        views.SaidaListView.as_view(), name='listapagamentosview'),
    # financeiro/pagamento/editar/
    url(r'pagamento/editar/(?P<pk>[0-9]+)/$',
        views.EditarSaidaView.as_view(), name='editarpagamentoview'),

    # Recebimentos
    # financeiro/recebimento/adicionar/
    url(r'recebimento/adicionar/$',
        views.AdicionarEntradaView.as_view(), name='addrecebimentoview'),
    # financeiro/recebimento/listarecebimento
    url(r'recebimento/listarecebimento/$',
        views.EntradaListView.as_view(), name='listarecebimentosview'),
    # financeiro/recebimento/editar/
    url(r'recebimento/editar/(?P<pk>[0-9]+)/$',
        views.EditarEntradaView.as_view(), name='editarrecebimentoview'),

    # Faturar Pedido de venda
    url(r'faturarpedidovenda/(?P<pk>[0-9]+)/$',
        views.FaturarPedidoVendaView.as_view(), name='faturarpedidovenda'),
    # Faturar Pedido de compra
    url(r'faturarpedidocompra/(?P<pk>[0-9]+)/$',
        views.FaturarPedidoCompraView.as_view(), name='faturarpedidocompra'),

    # Plano de contas
    # financeiro/planodecontas
    url(r'planodecontas/$', views.PlanoContasView.as_view(), name='planocontasview'),
    # financeiro/planodecontas/adicionargrupo/
    url(r'planodecontas/adicionargrupo/$',
        views.AdicionarGrupoPlanoContasView.as_view(), name='addgrupoview'),
    # financeiro/planodecontas/editargrupo/
    url(r'planodecontas/editargrupo/(?P<pk>[0-9]+)/$',
        views.EditarGrupoPlanoContasView.as_view(), name='editargrupoview'),

    # Fluxo de caixa
    # financeiro/fluxodecaixa
    url(r'fluxodecaixa/$', views.FluxoCaixaView.as_view(), name='fluxodecaixaview'),
]
