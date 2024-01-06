# -*- coding: utf-8 -*-

from .empresa import AdicionarEmpresaView, EmpresasListView, EditarEmpresaView
from .cliente import AdicionarClienteView, ClientesListView, EditarClienteView
from .fornecedor import AdicionarFornecedorView, FornecedoresListView, EditarFornecedorView
from .transportadora import AdicionarTransportadoraView, TransportadorasListView, EditarTransportadoraView
from .produto import (AdicionarProdutoView, ProdutosListView, ProdutosBaixoEstoqueListView, EditarProdutoView,
                      AdicionarCategoriaView, CategoriasListView, EditarCategoriaView,
                      AdicionarUnidadeView, UnidadesListView, EditarUnidadeView,
                      AdicionarMarcaView, MarcasListView, EditarMarcaView)
from .ajax_views import InfoCliente, InfoFornecedor, InfoEmpresa, InfoTransportadora, InfoProduto
