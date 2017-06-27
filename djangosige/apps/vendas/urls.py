# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'vendas'
urlpatterns = [
    ##Orcamentos de venda
    #/vendas/orcamentovenda/adicionar/
    url(r'orcamentovenda/adicionar/$', views.AdicionarOrcamentoVendaView.as_view(), name='addorcamentovendaview'),
    #/vendas/orcamentovenda/listaorcamentovenda
    url(r'orcamentovenda/listaorcamentovenda/$', views.OrcamentoVendaListView.as_view(), name='listaorcamentovendaview'),
    #/vendas/orcamentovenda/editar/
    url(r'orcamentovenda/editar/(?P<pk>[0-9]+)/$', views.EditarOrcamentoVendaView.as_view(), name='editarorcamentovendaview'),
    #/vendas/orcamentovenda/listaorcamentovenda/vencidos
    url(r'orcamentovenda/listaorcamentovenda/vencidos/$', views.OrcamentoVendaVencidosListView.as_view(), name='listaorcamentovendavencidoview'),
    #/vendas/orcamentovenda/listaorcamentovenda/hoje
    url(r'orcamentovenda/listaorcamentovenda/hoje/$', views.OrcamentoVendaVencimentoHojeListView.as_view(), name='listaorcamentovendahojeview'),

    ##Pedidos de venda
    #/vendas/pedidovenda/adicionar/
    url(r'pedidovenda/adicionar/$', views.AdicionarPedidoVendaView.as_view(), name='addpedidovendaview'),
    #/vendas/pedidovenda/listapedidovenda
    url(r'pedidovenda/listapedidovenda/$', views.PedidoVendaListView.as_view(), name='listapedidovendaview'),
    #/vendas/pedidovenda/editar/
    url(r'pedidovenda/editar/(?P<pk>[0-9]+)/$', views.EditarPedidoVendaView.as_view(), name='editarpedidovendaview'),
    #/vendas/pedidovenda/listapedidovenda/atrasados
    url(r'pedidovenda/listapedidovenda/atrasados/$', views.PedidoVendaAtrasadosListView.as_view(), name='listapedidovendaatrasadosview'),
    #/vendas/pedidovenda/listapedidovenda/hoje
    url(r'pedidovenda/listapedidovenda/hoje/$', views.PedidoVendaEntregaHojeListView.as_view(), name='listapedidovendahojeview'),

    ##Condicao pagamento
    #/vendas/pagamento/adicionar/
    url(r'pagamento/adicionar/$', views.AdicionarCondicaoPagamentoView.as_view(), name='addcondicaopagamentoview'),
    #/vendas/pagamento/listacondicaopagamento
    url(r'pagamento/listacondicaopagamento/$', views.CondicaoPagamentoListView.as_view(), name='listacondicaopagamentoview'),
    #/vendas/pagamento/editar/
    url(r'pagamento/editar/(?P<pk>[0-9]+)/$', views.EditarCondicaoPagamentoView.as_view(), name='editarcondicaopagamentoview'),

    #Request ajax views
    url(r'infocliente/$', views.InfoCliente.as_view(), name='infocliente'),
    url(r'infotransportadora/$', views.InfoTransportadora.as_view(), name='infotransportadora'),
    url(r'infoproduto/$', views.InfoProduto.as_view(), name='infoproduto'),
    url(r'infocondpagamento/$', views.InfoCondicaoPagamento.as_view(), name='infocondpagamento'),
    url(r'infovenda/$', views.InfoVenda.as_view(), name='infovenda'),

    #Gerar pdf orcamento
    url(r'gerarpdforcamentovenda/(?P<pk>[0-9]+)/$', views.GerarPDFOrcamentoVenda.as_view(), name='gerarpdforcamentovenda'),
    #Gerar pdf pedido
    url(r'gerarpdfpedidovenda/(?P<pk>[0-9]+)/$', views.GerarPDFPedidoVenda.as_view(), name='gerarpdfpedidovenda'),
    #Gerar pedido a partir de um orçamento
    url(r'gerarpedidovenda/(?P<pk>[0-9]+)/$', views.GerarPedidoVendaView.as_view(), name='gerarpedidovenda'),
    #Copiar orcamento/pedido cancelado ou baixado
    url(r'copiarvenda/(?P<pk>[0-9]+)/$', views.GerarCopiaVendaView.as_view(), name='copiarvenda'),
    #Cancelar Pedido/Orcamento de venda
    url(r'cancelarvenda/(?P<pk>[0-9]+)/$', views.CancelarVendaView.as_view(), name='cancelarvenda'),
]