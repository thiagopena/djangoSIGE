# -*- coding: utf-8 -*-

from django.urls import re_path as url
from . import views

app_name = 'djangosige.apps.estoque'
urlpatterns = [
    # Consulta de estoque
    # estoque/consultaestoque/
    url(r'consultaestoque/$', views.ConsultaEstoqueView.as_view(),
        name='consultaestoqueview'),

    # Local de estoque
    # estoque/local/adicionar/
    url(r'local/saida/adicionar/$',
        views.AdicionarLocalEstoqueView.as_view(), name='addlocalview'),
    # estoque/local/listalocal
    url(r'local/listalocal/$', views.LocalEstoqueListView.as_view(),
        name='listalocalview'),
    # estoque/local/editar/
    url(r'local/editar/(?P<pk>[0-9]+)/$',
        views.EditarLocalEstoqueView.as_view(), name='editarlocalview'),

    # Movimento de estoque
    # Lista todos movimentos
    url(r'movimentos/$', views.MovimentoEstoqueListView.as_view(),
        name='listamovimentoestoqueview'),

    # EntradaEstoque
    # estoque/movimento/adicionarentrada/
    url(r'movimento/adicionarentrada/$',
        views.AdicionarEntradaEstoqueView.as_view(), name='addentradaestoqueview'),
    # estoque/movimento/listaentradas/
    url(r'movimento/listaentradas/$', views.EntradaEstoqueListView.as_view(),
        name='listaentradasestoqueview'),
    # estoque/movimento/editarentrada/
    url(r'movimento/editarentrada/(?P<pk>[0-9]+)/$', views.DetalharEntradaEstoqueView.as_view(
    ), name='detalharentradaestoqueview'),

    # SaidaEstoque
    # estoque/movimento/adicionarsaida/
    url(r'movimento/adicionarsaida/$',
        views.AdicionarSaidaEstoqueView.as_view(), name='addsaidaestoqueview'),
    # estoque/movimento/listasaidas/
    url(r'movimento/listasaidas/$', views.SaidaEstoqueListView.as_view(),
        name='listasaidasestoqueview'),
    # estoque/movimento/editarsaida/
    url(r'movimento/editarsaida/(?P<pk>[0-9]+)/$',
        views.DetalharSaidaEstoqueView.as_view(), name='detalharsaidaestoqueview'),

    # TransferenciaEstoque
    # estoque/movimento/adicionartransferencia/
    url(r'movimento/adicionartransferencia/$',
        views.AdicionarTransferenciaEstoqueView.as_view(), name='addtransferenciaestoqueview'),
    # estoque/movimento/listatransferencias/
    url(r'movimento/listatransferencias/$', views.TransferenciaEstoqueListView.as_view(),
        name='listatransferenciasestoqueview'),
    # estoque/movimento/editartransferencia/
    url(r'movimento/editartransferencia/(?P<pk>[0-9]+)/$', views.DetalharTransferenciaEstoqueView.as_view(
    ), name='detalhartransferenciaestoqueview'),
]
