# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'compras'
urlpatterns = [
    # Orcamentos de compra
    #/compras/orcamentocompra/adicionar/
    url(r'orcamentocompra/adicionar/$',
        views.AdicionarOrcamentoCompraView.as_view(), name='addorcamentocompraview'),
    #/compras/orcamentocompra/listaorcamentocompra
    url(r'orcamentocompra/listaorcamentocompra/$',
        views.OrcamentoCompraListView.as_view(), name='listaorcamentocompraview'),
    #/compras/orcamentocompra/editar/
    url(r'orcamentocompra/editar/(?P<pk>[0-9]+)/$',
        views.EditarOrcamentoCompraView.as_view(), name='editarorcamentocompraview'),
    #/compras/orcamentocompra/listaorcamentocompra/vencidos/
    url(r'orcamentocompra/listaorcamentocompra/vencidos/$',
        views.OrcamentoCompraVencidosListView.as_view(), name='listaorcamentocompravencidosview'),
    #/compras/orcamentocompra/listaorcamentocompra/hoje/
    url(r'orcamentocompra/listaorcamentocompra/hoje/$',
        views.OrcamentoCompraVencimentoHojeListView.as_view(), name='listaorcamentocomprahojeview'),

    # Pedidos de compra
    #/compras/pedidocompra/adicionar/
    url(r'pedidocompra/adicionar/$',
        views.AdicionarPedidoCompraView.as_view(), name='addpedidocompraview'),
    #/compras/pedidocompra/listapedidocompra
    url(r'pedidocompra/listapedidocompra/$',
        views.PedidoCompraListView.as_view(), name='listapedidocompraview'),
    #/compras/pedidocompra/editar/
    url(r'pedidocompra/editar/(?P<pk>[0-9]+)/$',
        views.EditarPedidoCompraView.as_view(), name='editarpedidocompraview'),
    #/compras/pedidocompra/listapedidocompra/atrasados/
    url(r'pedidocompra/listapedidocompra/atrasados/$',
        views.PedidoCompraAtrasadosListView.as_view(), name='listapedidocompraatrasadosview'),
    #/compras/pedidocompra/listapedidocompra/hoje/
    url(r'pedidocompra/listapedidocompra/hoje/$',
        views.PedidoCompraEntregaHojeListView.as_view(), name='listapedidocomprahojeview'),

    # Request ajax
    url(r'infofornecedor/$', views.InfoFornecedor.as_view(), name='infofornecedor'),
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
    # Copiar orcamento/pedido cancelado ou realizado
    url(r'copiarcompra/(?P<pk>[0-9]+)/$',
        views.GerarCopiaCompraView.as_view(), name='copiarcompra'),
    # Cancelar Pedido/Orcamento de compra
    url(r'cancelarcompra/(?P<pk>[0-9]+)/$',
        views.CancelarCompraView.as_view(), name='cancelarcompra'),
    # Receber Pedido de compra
    url(r'recebercompra/(?P<pk>[0-9]+)/$',
        views.ReceberCompraView.as_view(), name='recebercompra'),
]
