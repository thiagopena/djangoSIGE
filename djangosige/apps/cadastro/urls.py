# -*- coding: utf-8 -*-

from django.urls import re_path as url
from . import views

app_name = 'djangosige.apps.cadastro'
urlpatterns = [
    # Empresa
    # cadastro/empresa/adicionar/
    url(r'empresa/adicionar/$',
        views.AdicionarEmpresaView.as_view(), name='addempresaview'),
    # cadastro/empresa/listaempresas
    url(r'empresa/listaempresas/$',
        views.EmpresasListView.as_view(), name='listaempresasview'),
    # cadastro/empresa/editar/
    url(r'empresa/editar/(?P<pk>[0-9]+)/$',
        views.EditarEmpresaView.as_view(), name='editarempresaview'),

    # Cliente
    # cadastro/cliente/adicionar/
    url(r'cliente/adicionar/$',
        views.AdicionarClienteView.as_view(), name='addclienteview'),
    # cadastro/cliente/listaclientes
    url(r'cliente/listaclientes/$',
        views.ClientesListView.as_view(), name='listaclientesview'),
    # cadastro/cliente/editar/
    url(r'cliente/editar/(?P<pk>[0-9]+)/$',
        views.EditarClienteView.as_view(), name='editarclienteview'),

    # Fornecedor
    # cadastro/fornecedor/adicionar/
    url(r'fornecedor/adicionar/$',
        views.AdicionarFornecedorView.as_view(), name='addfornecedorview'),
    # cadastro/fornecedor/listafornecedores
    url(r'fornecedor/listafornecedores/$',
        views.FornecedoresListView.as_view(), name='listafornecedoresview'),
    # cadastro/fornecedor/editar/
    url(r'fornecedor/editar/(?P<pk>[0-9]+)/$',
        views.EditarFornecedorView.as_view(), name='editarfornecedorview'),

    # Transportadora
    # cadastro/transportadora/adicionar/
    url(r'transportadora/adicionar/$',
        views.AdicionarTransportadoraView.as_view(), name='addtransportadoraview'),
    # cadastro/transportadora/listatransportadoras
    url(r'transportadora/listatransportadoras/$',
        views.TransportadorasListView.as_view(), name='listatransportadorasview'),
    # cadastro/transportadora/editar/
    url(r'transportadora/editar/(?P<pk>[0-9]+)/$',
        views.EditarTransportadoraView.as_view(), name='editartransportadoraview'),

    # Produto
    # cadastro/produto/adicionar/
    url(r'produto/adicionar/$',
        views.AdicionarProdutoView.as_view(), name='addprodutoview'),
    # cadastro/produto/listaprodutos
    url(r'produto/listaprodutos/$',
        views.ProdutosListView.as_view(), name='listaprodutosview'),
    # cadastro/produto/listaprodutos/baixoestoque
    url(r'produto/listaprodutos/baixoestoque/$',
        views.ProdutosBaixoEstoqueListView.as_view(), name='listaprodutosbaixoestoqueview'),
    # cadastro/produto/editar/
    url(r'produto/editar/(?P<pk>[0-9]+)/$',
        views.EditarProdutoView.as_view(), name='editarprodutoview'),

    # Outros
    # Categorias
    # cadastro/outros/adicionarcategoria/
    url(r'outros/adicionarcategoria/$',
        views.AdicionarCategoriaView.as_view(), name='addcategoriaview'),
    # cadastro/outros/listacategorias/
    url(r'outros/listacategorias/$',
        views.CategoriasListView.as_view(), name='listacategoriasview'),
    # cadastro/outros/editarcategoria/
    url(r'outros/editarcategoria/(?P<pk>[0-9]+)/$',
        views.EditarCategoriaView.as_view(), name='editarcategoriaview'),

    # Unidades
    # cadastro/outros/adicionarunidade/
    url(r'outros/adicionarunidade/$',
        views.AdicionarUnidadeView.as_view(), name='addunidadeview'),
    # cadastro/outros/listaunidades/
    url(r'outros/listaunidades/$',
        views.UnidadesListView.as_view(), name='listaunidadesview'),
    # cadastro/outros/editarcunidade/
    url(r'outros/editarunidade/(?P<pk>[0-9]+)/$',
        views.EditarUnidadeView.as_view(), name='editarunidadeview'),

    # Marcas
    # cadastro/outros/adicionarmarca/
    url(r'outros/adicionarmarca/$',
        views.AdicionarMarcaView.as_view(), name='addmarcaview'),
    # cadastro/outros/listamarcas/
    url(r'outros/listamarcas/$',
        views.MarcasListView.as_view(), name='listamarcasview'),
    # cadastro/outros/editarmarca/
    url(r'outros/editarmarca/(?P<pk>[0-9]+)/$',
        views.EditarMarcaView.as_view(), name='editarmarcaview'),

    # Informacoes de dada empresa (Ajax request)
    url(r'infoempresa/$', views.InfoEmpresa.as_view(), name='infoempresa'),
    url(r'infofornecedor/$', views.InfoFornecedor.as_view(), name='infofornecedor'),
    url(r'infocliente/$', views.InfoCliente.as_view(), name='infocliente'),
    url(r'infotransportadora/$', views.InfoTransportadora.as_view(),
        name='infotransportadora'),
    url(r'infoproduto/$', views.InfoProduto.as_view(), name='infoproduto'),
]
