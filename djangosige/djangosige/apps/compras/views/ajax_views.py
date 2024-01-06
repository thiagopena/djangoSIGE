# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse

import json

from djangosige.apps.compras.models import PedidoCompra


class InfoCompra(View):

    def post(self, request, *args, **kwargs):
        compra = PedidoCompra.objects.get(pk=request.POST['compraId'])
        itens_compra = compra.itens_compra.all()
        pagamentos = compra.parcela_pagamento.all()
        data = []

        pedido_dict = {}
        pedido_dict['model'] = 'compras.pedidocompra'
        pedido_dict['pk'] = compra.id
        pedido_fields_dict = {}
        pedido_fields_dict['emit'] = compra.fornecedor.id
        pedido_fields_dict['local'] = compra.get_local_dest_id()
        pedido_fields_dict['status'] = compra.get_status_display()
        pedido_fields_dict['desconto'] = compra.format_desconto()
        pedido_fields_dict['frete'] = compra.format_frete()
        pedido_fields_dict['despesas'] = compra.format_despesas()
        pedido_fields_dict['seguro'] = compra.format_seguro()
        pedido_fields_dict['total_icms'] = compra.format_vicms()
        pedido_fields_dict['total_ipi'] = compra.format_vipi()
        pedido_fields_dict['valor_total'] = compra.format_valor_total()
        pedido_fields_dict['total_sem_desconto'] = compra.format_total_sem_desconto(
        )
        pedido_fields_dict['forma_pag'] = compra.get_forma_pagamento()
        pedido_fields_dict['n_itens'] = str(len(itens_compra))
        pedido_fields_dict['valor_total_produtos'] = compra.format_total_produtos(
        )

        if compra.cond_pagamento:
            pedido_fields_dict['n_parcelas'] = compra.cond_pagamento.n_parcelas
        else:
            pedido_fields_dict['n_parcelas'] = 1

        pedido_dict['fields'] = pedido_fields_dict

        data.append(pedido_dict)

        for item in itens_compra:
            itens_compra_dict = {}
            itens_compra_dict['model'] = 'compras.itenscompra'
            itens_compra_dict['pk'] = item.id
            itens_fields_dict = {}
            itens_hidden_fields_dict = {}
            itens_editable_fields_dict = {}
            itens_fields_dict['produto_id'] = item.produto.id
            itens_fields_dict[
                'controlar_estoque'] = item.produto.controlar_estoque
            itens_fields_dict['produto'] = item.produto.descricao
            itens_hidden_fields_dict['codigo'] = item.produto.codigo
            itens_hidden_fields_dict['unidade'] = item.produto.get_sigla_unidade(
            )
            itens_hidden_fields_dict['ncm'] = item.produto.ncm
            itens_fields_dict['quantidade'] = item.format_quantidade()
            itens_fields_dict['valor_unit'] = item.format_valor_unit()
            itens_fields_dict['desconto'] = item.format_desconto()
            itens_hidden_fields_dict['subtotal'] = item.format_valor_attr(
                'subtotal')

            itens_fields_dict['impostos'] = item.format_total_impostos()
            itens_fields_dict['total'] = item.format_total_com_imposto()
            itens_fields_dict['vprod'] = item.format_vprod()

            itens_hidden_fields_dict['vicms'] = item.format_valor_attr('vicms')
            itens_hidden_fields_dict['vipi'] = item.format_valor_attr('vipi')

            itens_editable_fields_dict[
                'editable_field_inf_ad_prod'] = item.inf_ad_prod

            itens_compra_dict['fields'] = itens_fields_dict
            itens_compra_dict['hidden_fields'] = itens_hidden_fields_dict
            itens_compra_dict['editable_fields'] = itens_editable_fields_dict

            data.append(itens_compra_dict)

        for pagamento in pagamentos:
            pagamento_dict = {}
            pagamento_dict['model'] = 'compras.pagamento'
            pagamento_dict['pk'] = pagamento.id
            pagamento_fields_dict = {}
            pagamento_fields_dict['id'] = pagamento.id
            pagamento_fields_dict['vencimento'] = pagamento.format_vencimento
            pagamento_fields_dict[
                'valor_parcela'] = pagamento.format_valor_parcela

            pagamento_dict['fields'] = pagamento_fields_dict

            data.append(pagamento_dict)

        return HttpResponse(json.dumps(data), content_type='application/json')
