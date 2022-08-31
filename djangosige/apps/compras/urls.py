# -*- coding: utf-8 -*-

from django.urls import re_path as url
from . import views

app_name = 'djangosige.apps.compras'
urlpatterns = [
    # Orcamentos de compra
    # compras/orcamentocompra/adicionar/
    url(r'orcamentocompra/adicionar/$',
        views.AdicionarOrcamentoCompraView.as_view(), name='addorcamentocompraview'),
    # compras/orcamentocompra/listaorcamentocompra
    url(r'orcamentocompra/listaorcamentocompra/$',
        views.OrcamentoCompraListView.as_view(), name='listaorcamentocompraview'),
    # compras/orcamentocompra/editar/
    url(r'orcamentocompra/editar/(?P<pk>[0-9]+)/$',
        views.EditarOrcamentoCompraView.as_view(), name='editarorcamentocompraview'),
    # compras/orcamentocompra/listaorcamentocompra/vencidos/
    url(r'orcamentocompra/listaorcamentocompra/vencidos/$',
        views.OrcamentoCompraVencidosListView.as_view(), name='listaorcamentocompravencidosview'),
    # compras/orcamentocompra/listaorcamentocompra/hoje/
    url(r'orcamentocompra/listaorcamentocompra/hoje/$',
        views.OrcamentoCompraVencimentoHojeListView.as_view(), name='listaorcamentocomprahojeview'),

    # Pedidos de compra
    # compras/pedidocompra/adicionar/
    url(r'pedidocompra/adicionar/$',
        views.AdicionarPedidoCompraView.as_view(), name='addpedidocompraview'),
    # compras/pedidocompra/listapedidocompra
    url(r'pedidocompra/listapedidocompra/$',
        views.PedidoCompraListView.as_view(), name='listapedidocompraview'),
    # compras/pedidocompra/editar/
    url(r'pedidocompra/editar/(?P<pk>[0-9]+)/$',
        views.EditarPedidoCompraView.as_view(), name='editarpedidocompraview'),
    # compras/pedidocompra/listapedidocompra/atrasados/
    url(r'pedidocompra/listapedidocompra/atrasados/$',
        views.PedidoCompraAtrasadosListView.as_view(), name='listapedidocompraatrasadosview'),
    # compras/pedidocompra/listapedidocompra/hoje/
    url(r'pedidocompra/listapedidocompra/hoje/$',
        views.PedidoCompraEntregaHojeListView.as_view(), name='listapedidocomprahojeview'),

    # Request ajax
    url(r'infocompra/$', views.InfoCompra.as_view(), name='infocompra'),

    # Gerar pdf orcamento
    url(r'gerarpdforcamentocompra/(?P<pk>[0-9]+)/$',
        views.GerarPDFOrcamentoCompra.as_view(), name='gerarpdforcamentocompra'),
    # Gerar pdf pedido
    url(r'gerarpdfpedidocompra/(?P<pk>[0-9]+)/$',
        views.GerarPDFPedidoCompra.as_view(), name='gerarpdfpedidocompra'),
    # Gerar pedido a partir de um orçamento
    url(r'gerarpedidocompra/(?P<pk>[0-9]+)/$',
        views.GerarPedidoCompraView.as_view(), name='gerarpedidocompra'),
    # Copiar orcamento cancelado ou realizado
    url(r'copiarorcamentocompra/(?P<pk>[0-9]+)/$',
        views.GerarCopiaOrcamentoCompraView.as_view(), name='copiarorcamentocompra'),
    # Copiar pedido cancelado ou realizado
    url(r'copiarpedidocompra/(?P<pk>[0-9]+)/$',
        views.GerarCopiaPedidoCompraView.as_view(), name='copiarpedidocompra'),
    # Cancelar Pedido de compra
    url(r'cancelarpedidocompra/(?P<pk>[0-9]+)/$',
        views.CancelarPedidoCompraView.as_view(), name='cancelarpedidocompra'),
    # Cancelar Orcamento de compra
    url(r'cancelarorcamentocompra/(?P<pk>[0-9]+)/$',
        views.CancelarOrcamentoCompraView.as_view(), name='cancelarorcamentocompra'),
    # Receber Pedido de compra
    url(r'receberpedidocompra/(?P<pk>[0-9]+)/$',
        views.ReceberPedidoCompraView.as_view(), name='receberpedidocompra'),
]
