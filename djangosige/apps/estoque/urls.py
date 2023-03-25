from django.urls import re_path

from . import views

app_name = "estoque"
urlpatterns = [
    # Consulta de estoque
    # estoque/consultaestoque/
    re_path(
        r"consultaestoque/$",
        views.ConsultaEstoqueView.as_view(),
        name="consultaestoqueview",
    ),
    # Local de estoque
    # estoque/local/adicionar/
    re_path(
        r"local/saida/adicionar/$",
        views.AdicionarLocalEstoqueView.as_view(),
        name="addlocalview",
    ),
    # estoque/local/listalocal
    re_path(
        r"local/listalocal/$",
        views.LocalEstoqueListView.as_view(),
        name="listalocalview",
    ),
    # estoque/local/editar/
    re_path(
        r"local/editar/(?P<pk>[0-9]+)/$",
        views.EditarLocalEstoqueView.as_view(),
        name="editarlocalview",
    ),
    # Movimento de estoque
    # Lista todos movimentos
    re_path(
        r"movimentos/$",
        views.MovimentoEstoqueListView.as_view(),
        name="listamovimentoestoqueview",
    ),
    # EntradaEstoque
    # estoque/movimento/adicionarentrada/
    re_path(
        r"movimento/adicionarentrada/$",
        views.AdicionarEntradaEstoqueView.as_view(),
        name="addentradaestoqueview",
    ),
    # estoque/movimento/listaentradas/
    re_path(
        r"movimento/listaentradas/$",
        views.EntradaEstoqueListView.as_view(),
        name="listaentradasestoqueview",
    ),
    # estoque/movimento/editarentrada/
    re_path(
        r"movimento/editarentrada/(?P<pk>[0-9]+)/$",
        views.DetalharEntradaEstoqueView.as_view(),
        name="detalharentradaestoqueview",
    ),
    # SaidaEstoque
    # estoque/movimento/adicionarsaida/
    re_path(
        r"movimento/adicionarsaida/$",
        views.AdicionarSaidaEstoqueView.as_view(),
        name="addsaidaestoqueview",
    ),
    # estoque/movimento/listasaidas/
    re_path(
        r"movimento/listasaidas/$",
        views.SaidaEstoqueListView.as_view(),
        name="listasaidasestoqueview",
    ),
    # estoque/movimento/editarsaida/
    re_path(
        r"movimento/editarsaida/(?P<pk>[0-9]+)/$",
        views.DetalharSaidaEstoqueView.as_view(),
        name="detalharsaidaestoqueview",
    ),
    # TransferenciaEstoque
    # estoque/movimento/adicionartransferencia/
    re_path(
        r"movimento/adicionartransferencia/$",
        views.AdicionarTransferenciaEstoqueView.as_view(),
        name="addtransferenciaestoqueview",
    ),
    # estoque/movimento/listatransferencias/
    re_path(
        r"movimento/listatransferencias/$",
        views.TransferenciaEstoqueListView.as_view(),
        name="listatransferenciasestoqueview",
    ),
    # estoque/movimento/editartransferencia/
    re_path(
        r"movimento/editartransferencia/(?P<pk>[0-9]+)/$",
        views.DetalharTransferenciaEstoqueView.as_view(),
        name="detalhartransferenciaestoqueview",
    ),
]
