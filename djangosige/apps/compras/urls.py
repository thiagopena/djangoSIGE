from django.urls import re_path

from . import views

app_name = "compras"
urlpatterns = [
    # Orcamentos de compra
    # compras/orcamentocompra/adicionar/
    re_path(
        r"orcamentocompra/adicionar/$",
        views.AdicionarOrcamentoCompraView.as_view(),
        name="addorcamentocompraview",
    ),
    # compras/orcamentocompra/listaorcamentocompra
    re_path(
        r"orcamentocompra/listaorcamentocompra/$",
        views.OrcamentoCompraListView.as_view(),
        name="listaorcamentocompraview",
    ),
    # compras/orcamentocompra/editar/
    re_path(
        r"orcamentocompra/editar/(?P<pk>[0-9]+)/$",
        views.EditarOrcamentoCompraView.as_view(),
        name="editarorcamentocompraview",
    ),
    # compras/orcamentocompra/listaorcamentocompra/vencidos/
    re_path(
        r"orcamentocompra/listaorcamentocompra/vencidos/$",
        views.OrcamentoCompraVencidosListView.as_view(),
        name="listaorcamentocompravencidosview",
    ),
    # compras/orcamentocompra/listaorcamentocompra/hoje/
    re_path(
        r"orcamentocompra/listaorcamentocompra/hoje/$",
        views.OrcamentoCompraVencimentoHojeListView.as_view(),
        name="listaorcamentocomprahojeview",
    ),
    # Pedidos de compra
    # compras/pedidocompra/adicionar/
    re_path(
        r"pedidocompra/adicionar/$",
        views.AdicionarPedidoCompraView.as_view(),
        name="addpedidocompraview",
    ),
    # compras/pedidocompra/listapedidocompra
    re_path(
        r"pedidocompra/listapedidocompra/$",
        views.PedidoCompraListView.as_view(),
        name="listapedidocompraview",
    ),
    # compras/pedidocompra/editar/
    re_path(
        r"pedidocompra/editar/(?P<pk>[0-9]+)/$",
        views.EditarPedidoCompraView.as_view(),
        name="editarpedidocompraview",
    ),
    # compras/pedidocompra/listapedidocompra/atrasados/
    re_path(
        r"pedidocompra/listapedidocompra/atrasados/$",
        views.PedidoCompraAtrasadosListView.as_view(),
        name="listapedidocompraatrasadosview",
    ),
    # compras/pedidocompra/listapedidocompra/hoje/
    re_path(
        r"pedidocompra/listapedidocompra/hoje/$",
        views.PedidoCompraEntregaHojeListView.as_view(),
        name="listapedidocomprahojeview",
    ),
    # Request ajax
    re_path(r"infocompra/$", views.InfoCompra.as_view(), name="infocompra"),
    # Gerar pdf orcamento
    re_path(
        r"gerarpdforcamentocompra/(?P<pk>[0-9]+)/$",
        views.GerarPDFOrcamentoCompra.as_view(),
        name="gerarpdforcamentocompra",
    ),
    # Gerar pdf pedido
    re_path(
        r"gerarpdfpedidocompra/(?P<pk>[0-9]+)/$",
        views.GerarPDFPedidoCompra.as_view(),
        name="gerarpdfpedidocompra",
    ),
    # Gerar pedido a partir de um orçamento
    re_path(
        r"gerarpedidocompra/(?P<pk>[0-9]+)/$",
        views.GerarPedidoCompraView.as_view(),
        name="gerarpedidocompra",
    ),
    # Copiar orcamento cancelado ou realizado
    re_path(
        r"copiarorcamentocompra/(?P<pk>[0-9]+)/$",
        views.GerarCopiaOrcamentoCompraView.as_view(),
        name="copiarorcamentocompra",
    ),
    # Copiar pedido cancelado ou realizado
    re_path(
        r"copiarpedidocompra/(?P<pk>[0-9]+)/$",
        views.GerarCopiaPedidoCompraView.as_view(),
        name="copiarpedidocompra",
    ),
    # Cancelar Pedido de compra
    re_path(
        r"cancelarpedidocompra/(?P<pk>[0-9]+)/$",
        views.CancelarPedidoCompraView.as_view(),
        name="cancelarpedidocompra",
    ),
    # Cancelar Orcamento de compra
    re_path(
        r"cancelarorcamentocompra/(?P<pk>[0-9]+)/$",
        views.CancelarOrcamentoCompraView.as_view(),
        name="cancelarorcamentocompra",
    ),
    # Receber Pedido de compra
    re_path(
        r"receberpedidocompra/(?P<pk>[0-9]+)/$",
        views.ReceberPedidoCompraView.as_view(),
        name="receberpedidocompra",
    ),
]
