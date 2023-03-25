from django.urls import re_path

from . import views

app_name = "cadastro"
urlpatterns = [
    # Empresa
    # cadastro/empresa/adicionar/
    re_path(
        r"empresa/adicionar/$",
        views.AdicionarEmpresaView.as_view(),
        name="addempresaview",
    ),
    # cadastro/empresa/listaempresas
    re_path(
        r"empresa/listaempresas/$",
        views.EmpresasListView.as_view(),
        name="listaempresasview",
    ),
    # cadastro/empresa/editar/
    re_path(
        r"empresa/editar/(?P<pk>[0-9]+)/$",
        views.EditarEmpresaView.as_view(),
        name="editarempresaview",
    ),
    # Cliente
    # cadastro/cliente/adicionar/
    re_path(
        r"cliente/adicionar/$",
        views.AdicionarClienteView.as_view(),
        name="addclienteview",
    ),
    # cadastro/cliente/listaclientes
    re_path(
        r"cliente/listaclientes/$",
        views.ClientesListView.as_view(),
        name="listaclientesview",
    ),
    # cadastro/cliente/editar/
    re_path(
        r"cliente/editar/(?P<pk>[0-9]+)/$",
        views.EditarClienteView.as_view(),
        name="editarclienteview",
    ),
    # Fornecedor
    # cadastro/fornecedor/adicionar/
    re_path(
        r"fornecedor/adicionar/$",
        views.AdicionarFornecedorView.as_view(),
        name="addfornecedorview",
    ),
    # cadastro/fornecedor/listafornecedores
    re_path(
        r"fornecedor/listafornecedores/$",
        views.FornecedoresListView.as_view(),
        name="listafornecedoresview",
    ),
    # cadastro/fornecedor/editar/
    re_path(
        r"fornecedor/editar/(?P<pk>[0-9]+)/$",
        views.EditarFornecedorView.as_view(),
        name="editarfornecedorview",
    ),
    # Transportadora
    # cadastro/transportadora/adicionar/
    re_path(
        r"transportadora/adicionar/$",
        views.AdicionarTransportadoraView.as_view(),
        name="addtransportadoraview",
    ),
    # cadastro/transportadora/listatransportadoras
    re_path(
        r"transportadora/listatransportadoras/$",
        views.TransportadorasListView.as_view(),
        name="listatransportadorasview",
    ),
    # cadastro/transportadora/editar/
    re_path(
        r"transportadora/editar/(?P<pk>[0-9]+)/$",
        views.EditarTransportadoraView.as_view(),
        name="editartransportadoraview",
    ),
    # Produto
    # cadastro/produto/adicionar/
    re_path(
        r"produto/adicionar/$",
        views.AdicionarProdutoView.as_view(),
        name="addprodutoview",
    ),
    # cadastro/produto/listaprodutos
    re_path(
        r"produto/listaprodutos/$",
        views.ProdutosListView.as_view(),
        name="listaprodutosview",
    ),
    # cadastro/produto/listaprodutos/baixoestoque
    re_path(
        r"produto/listaprodutos/baixoestoque/$",
        views.ProdutosBaixoEstoqueListView.as_view(),
        name="listaprodutosbaixoestoqueview",
    ),
    # cadastro/produto/editar/
    re_path(
        r"produto/editar/(?P<pk>[0-9]+)/$",
        views.EditarProdutoView.as_view(),
        name="editarprodutoview",
    ),
    # Outros
    # Categorias
    # cadastro/outros/adicionarcategoria/
    re_path(
        r"outros/adicionarcategoria/$",
        views.AdicionarCategoriaView.as_view(),
        name="addcategoriaview",
    ),
    # cadastro/outros/listacategorias/
    re_path(
        r"outros/listacategorias/$",
        views.CategoriasListView.as_view(),
        name="listacategoriasview",
    ),
    # cadastro/outros/editarcategoria/
    re_path(
        r"outros/editarcategoria/(?P<pk>[0-9]+)/$",
        views.EditarCategoriaView.as_view(),
        name="editarcategoriaview",
    ),
    # Unidades
    # cadastro/outros/adicionarunidade/
    re_path(
        r"outros/adicionarunidade/$",
        views.AdicionarUnidadeView.as_view(),
        name="addunidadeview",
    ),
    # cadastro/outros/listaunidades/
    re_path(
        r"outros/listaunidades/$",
        views.UnidadesListView.as_view(),
        name="listaunidadesview",
    ),
    # cadastro/outros/editarcunidade/
    re_path(
        r"outros/editarunidade/(?P<pk>[0-9]+)/$",
        views.EditarUnidadeView.as_view(),
        name="editarunidadeview",
    ),
    # Marcas
    # cadastro/outros/adicionarmarca/
    re_path(
        r"outros/adicionarmarca/$",
        views.AdicionarMarcaView.as_view(),
        name="addmarcaview",
    ),
    # cadastro/outros/listamarcas/
    re_path(
        r"outros/listamarcas/$", views.MarcasListView.as_view(), name="listamarcasview"
    ),
    # cadastro/outros/editarmarca/
    re_path(
        r"outros/editarmarca/(?P<pk>[0-9]+)/$",
        views.EditarMarcaView.as_view(),
        name="editarmarcaview",
    ),
    # Informacoes de dada empresa (Ajax request)
    re_path(r"infoempresa/$", views.InfoEmpresa.as_view(), name="infoempresa"),
    re_path(r"infofornecedor/$", views.InfoFornecedor.as_view(), name="infofornecedor"),
    re_path(r"infocliente/$", views.InfoCliente.as_view(), name="infocliente"),
    re_path(
        r"infotransportadora/$",
        views.InfoTransportadora.as_view(),
        name="infotransportadora",
    ),
    re_path(r"infoproduto/$", views.InfoProduto.as_view(), name="infoproduto"),
]
