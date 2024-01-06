# -*- coding: utf-8 -*-

from .ajax_views import InfoCompra
from .compras import (
    AdicionarOrcamentoCompraView,
    AdicionarPedidoCompraView,
    CancelarOrcamentoCompraView,
    CancelarPedidoCompraView,
    EditarOrcamentoCompraView,
    EditarPedidoCompraView,
    GerarCopiaOrcamentoCompraView,
    GerarCopiaPedidoCompraView,
    GerarPDFOrcamentoCompra,
    GerarPDFPedidoCompra,
    GerarPedidoCompraView,
    OrcamentoCompraListView,
    OrcamentoCompraVencidosListView,
    OrcamentoCompraVencimentoHojeListView,
    PedidoCompraAtrasadosListView,
    PedidoCompraEntregaHojeListView,
    PedidoCompraListView,
    ReceberPedidoCompraView,
)
