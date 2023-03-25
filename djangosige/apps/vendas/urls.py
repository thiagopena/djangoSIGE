from django.urls import re_path

from . import views

app_name = "vendas"
urlpatterns = [
    # Orcamentos de venda
    # vendas/orcamentovenda/adicionar/
    re_path(
        r"orcamentovenda/adicionar/$",
        views.AdicionarOrcamentoVendaView.as_view(),
        name="addorcamentovendaview",
    ),
    # vendas/orcamentovenda/listaorcamentovenda
    re_path(
        r"orcamentovenda/listaorcamentovenda/$",
        views.OrcamentoVendaListView.as_view(),
        name="listaorcamentovendaview",
    ),
    # vendas/orcamentovenda/editar/
    re_path(
        r"orcamentovenda/editar/(?P<pk>[0-9]+)/$",
        views.EditarOrcamentoVendaView.as_view(),
        name="editarorcamentovendaview",
    ),
    # vendas/orcamentovenda/listaorcamentovenda/vencidos
    re_path(
        r"orcamentovenda/listaorcamentovenda/vencidos/$",
        views.OrcamentoVendaVencidosListView.as_view(),
        name="listaorcamentovendavencidoview",
    ),
    # vendas/orcamentovenda/listaorcamentovenda/hoje
    re_path(
        r"orcamentovenda/listaorcamentovenda/hoje/$",
        views.OrcamentoVendaVencimentoHojeListView.as_view(),
        name="listaorcamentovendahojeview",
    ),
    # Pedidos de venda
    # vendas/pedidovenda/adicionar/
    re_path(
        r"pedidovenda/adicionar/$",
        views.AdicionarPedidoVendaView.as_view(),
        name="addpedidovendaview",
    ),
    # vendas/pedidovenda/listapedidovenda
    re_path(
        r"pedidovenda/listapedidovenda/$",
        views.PedidoVendaListView.as_view(),
        name="listapedidovendaview",
    ),
    # vendas/pedidovenda/editar/
    re_path(
        r"pedidovenda/editar/(?P<pk>[0-9]+)/$",
        views.EditarPedidoVendaView.as_view(),
        name="editarpedidovendaview",
    ),
    # vendas/pedidovenda/listapedidovenda/atrasados
    re_path(
        r"pedidovenda/listapedidovenda/atrasados/$",
        views.PedidoVendaAtrasadosListView.as_view(),
        name="listapedidovendaatrasadosview",
    ),
    # vendas/pedidovenda/listapedidovenda/hoje
    re_path(
        r"pedidovenda/listapedidovenda/hoje/$",
        views.PedidoVendaEntregaHojeListView.as_view(),
        name="listapedidovendahojeview",
    ),
    # Condicao pagamento
    # vendas/pagamento/adicionar/
    re_path(
        r"pagamento/adicionar/$",
        views.AdicionarCondicaoPagamentoView.as_view(),
        name="addcondicaopagamentoview",
    ),
    # vendas/pagamento/listacondicaopagamento
    re_path(
        r"pagamento/listacondicaopagamento/$",
        views.CondicaoPagamentoListView.as_view(),
        name="listacondicaopagamentoview",
    ),
    # vendas/pagamento/editar/
    re_path(
        r"pagamento/editar/(?P<pk>[0-9]+)/$",
        views.EditarCondicaoPagamentoView.as_view(),
        name="editarcondicaopagamentoview",
    ),
    # Request ajax views
    re_path(
        r"infocondpagamento/$",
        views.InfoCondicaoPagamento.as_view(),
        name="infocondpagamento",
    ),
    re_path(r"infovenda/$", views.InfoVenda.as_view(), name="infovenda"),
    # Gerar pdf orcamento
    re_path(
        r"gerarpdforcamentovenda/(?P<pk>[0-9]+)/$",
        views.GerarPDFOrcamentoVenda.as_view(),
        name="gerarpdforcamentovenda",
    ),
    # Gerar pdf pedido
    re_path(
        r"gerarpdfpedidovenda/(?P<pk>[0-9]+)/$",
        views.GerarPDFPedidoVenda.as_view(),
        name="gerarpdfpedidovenda",
    ),
    # Gerar pedido a partir de um orçamento
    re_path(
        r"gerarpedidovenda/(?P<pk>[0-9]+)/$",
        views.GerarPedidoVendaView.as_view(),
        name="gerarpedidovenda",
    ),
    # Copiar orcamento cancelado ou baixado
    re_path(
        r"copiarorcamentovenda/(?P<pk>[0-9]+)/$",
        views.GerarCopiaOrcamentoVendaView.as_view(),
        name="copiarorcamentovenda",
    ),
    # Copiar pedido cancelado ou baixado
    re_path(
        r"copiarpedidovenda/(?P<pk>[0-9]+)/$",
        views.GerarCopiaPedidoVendaView.as_view(),
        name="copiarpedidovenda",
    ),
    # Cancelar Orcamento de venda
    re_path(
        r"cancelarorcamentovenda/(?P<pk>[0-9]+)/$",
        views.CancelarOrcamentoVendaView.as_view(),
        name="cancelarorcamentovenda",
    ),
    # Cancelar Pedido de venda
    re_path(
        r"cancelarpedidovenda/(?P<pk>[0-9]+)/$",
        views.CancelarPedidoVendaView.as_view(),
        name="cancelarpedidovenda",
    ),
]
