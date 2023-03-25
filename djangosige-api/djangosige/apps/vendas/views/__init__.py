from .ajax_views import InfoVenda
from .pagamento import *
from .vendas import (
    AdicionarOrcamentoVendaView,
    AdicionarPedidoVendaView,
    CancelarOrcamentoVendaView,
    CancelarPedidoVendaView,
    EditarOrcamentoVendaView,
    EditarPedidoVendaView,
    GerarCopiaOrcamentoVendaView,
    GerarCopiaPedidoVendaView,
    GerarPDFOrcamentoVenda,
    GerarPDFPedidoVenda,
    GerarPedidoVendaView,
    OrcamentoVendaListView,
    OrcamentoVendaVencidosListView,
    OrcamentoVendaVencimentoHojeListView,
    PedidoVendaAtrasadosListView,
    PedidoVendaEntregaHojeListView,
    PedidoVendaListView,
)
