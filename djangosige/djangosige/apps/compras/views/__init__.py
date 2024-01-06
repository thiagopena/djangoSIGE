# -*- coding: utf-8 -*-

from .compras import (AdicionarOrcamentoCompraView, AdicionarPedidoCompraView, OrcamentoCompraListView,
                      OrcamentoCompraVencidosListView, OrcamentoCompraVencimentoHojeListView, PedidoCompraListView,
                      PedidoCompraAtrasadosListView, PedidoCompraEntregaHojeListView, EditarOrcamentoCompraView,
                      EditarPedidoCompraView, GerarPedidoCompraView, CancelarOrcamentoCompraView,
                      CancelarPedidoCompraView, GerarCopiaOrcamentoCompraView, GerarCopiaPedidoCompraView,
                      ReceberPedidoCompraView, GerarPDFOrcamentoCompra, GerarPDFPedidoCompra)
from .ajax_views import InfoCompra
