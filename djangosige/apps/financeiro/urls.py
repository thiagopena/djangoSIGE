from django.urls import re_path

from . import views

app_name = "financeiro"
urlpatterns = [
    # Lancamentos
    # Gerar lancamento
    re_path(
        r"gerarlancamento/$",
        views.GerarLancamentoView.as_view(),
        name="gerarlancamento",
    ),
    # Lista todos lancamentos
    re_path(
        r"lancamentos/$", views.LancamentoListView.as_view(), name="listalancamentoview"
    ),
    # Contas a pagar
    # financeiro/contapagar/adicionar/
    re_path(
        r"contapagar/adicionar/$",
        views.AdicionarContaPagarView.as_view(),
        name="addcontapagarview",
    ),
    # financeiro/contapagar/listacontapagar
    re_path(
        r"contapagar/listacontapagar/$",
        views.ContaPagarListView.as_view(),
        name="listacontapagarview",
    ),
    # financeiro/contapagar/editar/
    re_path(
        r"contapagar/editar/(?P<pk>[0-9]+)/$",
        views.EditarContaPagarView.as_view(),
        name="editarcontapagarview",
    ),
    # financeiro/contapagar/listacontapagar/atrasadas/
    re_path(
        r"contapagar/listacontapagar/atrasadas/$",
        views.ContaPagarAtrasadasListView.as_view(),
        name="listacontapagaratrasadasview",
    ),
    # financeiro/contapagar/listacontapagar/hoje/
    re_path(
        r"contapagar/listacontapagar/hoje/$",
        views.ContaPagarHojeListView.as_view(),
        name="listacontapagarhojeview",
    ),
    # Contas a receber
    # financeiro/contareceber/adicionar/
    re_path(
        r"contareceber/adicionar/$",
        views.AdicionarContaReceberView.as_view(),
        name="addcontareceberview",
    ),
    # financeiro/contareceber/listacontapagar
    re_path(
        r"contareceber/listacontareceber/$",
        views.ContaReceberListView.as_view(),
        name="listacontareceberview",
    ),
    # financeiro/contareceber/editar/
    re_path(
        r"contareceber/editar/(?P<pk>[0-9]+)/$",
        views.EditarContaReceberView.as_view(),
        name="editarcontareceberview",
    ),
    # financeiro/contareceber/listacontapagar/atrasadas/
    re_path(
        r"contareceber/listacontareceber/atrasadas/$",
        views.ContaReceberAtrasadasListView.as_view(),
        name="listacontareceberatrasadasview",
    ),
    # financeiro/contareceber/listacontapagar/hoje/
    re_path(
        r"contareceber/listacontareceber/hoje/$",
        views.ContaReceberHojeListView.as_view(),
        name="listacontareceberhojeview",
    ),
    # Pagamentos
    # financeiro/pagamento/adicionar/
    re_path(
        r"pagamento/adicionar/$",
        views.AdicionarSaidaView.as_view(),
        name="addpagamentoview",
    ),
    # financeiro/pagamento/listacontapagar
    re_path(
        r"pagamento/listapagamento/$",
        views.SaidaListView.as_view(),
        name="listapagamentosview",
    ),
    # financeiro/pagamento/editar/
    re_path(
        r"pagamento/editar/(?P<pk>[0-9]+)/$",
        views.EditarSaidaView.as_view(),
        name="editarpagamentoview",
    ),
    # Recebimentos
    # financeiro/recebimento/adicionar/
    re_path(
        r"recebimento/adicionar/$",
        views.AdicionarEntradaView.as_view(),
        name="addrecebimentoview",
    ),
    # financeiro/recebimento/listarecebimento
    re_path(
        r"recebimento/listarecebimento/$",
        views.EntradaListView.as_view(),
        name="listarecebimentosview",
    ),
    # financeiro/recebimento/editar/
    re_path(
        r"recebimento/editar/(?P<pk>[0-9]+)/$",
        views.EditarEntradaView.as_view(),
        name="editarrecebimentoview",
    ),
    # Faturar Pedido de venda
    re_path(
        r"faturarpedidovenda/(?P<pk>[0-9]+)/$",
        views.FaturarPedidoVendaView.as_view(),
        name="faturarpedidovenda",
    ),
    # Faturar Pedido de compra
    re_path(
        r"faturarpedidocompra/(?P<pk>[0-9]+)/$",
        views.FaturarPedidoCompraView.as_view(),
        name="faturarpedidocompra",
    ),
    # Plano de contas
    # financeiro/planodecontas
    re_path(
        r"planodecontas/$", views.PlanoContasView.as_view(), name="planocontasview"
    ),
    # financeiro/planodecontas/adicionargrupo/
    re_path(
        r"planodecontas/adicionargrupo/$",
        views.AdicionarGrupoPlanoContasView.as_view(),
        name="addgrupoview",
    ),
    # financeiro/planodecontas/editargrupo/
    re_path(
        r"planodecontas/editargrupo/(?P<pk>[0-9]+)/$",
        views.EditarGrupoPlanoContasView.as_view(),
        name="editargrupoview",
    ),
    # Fluxo de caixa
    # financeiro/fluxodecaixa
    re_path(r"fluxodecaixa/$", views.FluxoCaixaView.as_view(), name="fluxodecaixaview"),
]
