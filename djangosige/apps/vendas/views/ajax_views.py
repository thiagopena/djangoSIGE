# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse

import json

from djangosige.apps.vendas.models import PedidoVenda


class InfoVenda(View):

    def post(self, request, *args, **kwargs):
        venda = PedidoVenda.objects.get(pk=request.POST['vendaId'])
        itens_venda = venda.itens_venda.all()
        pagamentos = venda.parcela_pagamento.all()
        data = []

        pedido_dict = {}
        pedido_dict['model'] = 'vendas.pedidovenda'
        pedido_dict['pk'] = venda.id
        pedido_fields_dict = {}
        pedido_fields_dict['dest'] = venda.cliente.id
        pedido_fields_dict['local'] = venda.get_local_orig_id()
        pedido_fields_dict['status'] = venda.get_status_display()
        pedido_fields_dict['desconto'] = venda.format_desconto()
        pedido_fields_dict['frete'] = venda.format_frete()
        pedido_fields_dict['despesas'] = venda.format_despesas()
        pedido_fields_dict['seguro'] = venda.format_seguro()
        pedido_fields_dict['impostos'] = venda.format_impostos()
        pedido_fields_dict['valor_total'] = venda.format_valor_total()
        pedido_fields_dict['total_sem_desconto'] = venda.format_total_sem_desconto(
        )
        pedido_fields_dict['ind_final'] = venda.ind_final
        pedido_fields_dict['forma_pag'] = venda.get_forma_pagamento()
        pedido_fields_dict['n_itens'] = str(len(itens_venda))
        pedido_fields_dict[
            'valor_total_produtos'] = venda.format_total_produtos()

        if venda.cond_pagamento:
            pedido_fields_dict['n_parcelas'] = venda.cond_pagamento.n_parcelas
        else:
            pedido_fields_dict['n_parcelas'] = 1

        pedido_dict['fields'] = pedido_fields_dict

        data.append(pedido_dict)

        for item in itens_venda:
            itens_venda_dict = {}
            itens_venda_dict['model'] = 'vendas.itensvenda'
            itens_venda_dict['pk'] = item.id
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
            itens_hidden_fields_dict['cfop'] = item.produto.get_cfop_padrao()
            itens_hidden_fields_dict['ncm'] = item.produto.ncm
            itens_fields_dict['quantidade'] = item.format_quantidade()
            itens_fields_dict['valor_unit'] = item.format_valor_unit()
            itens_fields_dict['desconto'] = item.format_desconto()
            itens_hidden_fields_dict['frete'] = item.format_valor_attr(
                'valor_rateio_frete')
            itens_hidden_fields_dict['despesas'] = item.format_valor_attr(
                'valor_rateio_despesas')
            itens_hidden_fields_dict['seguro'] = item.format_valor_attr(
                'valor_rateio_seguro')
            itens_hidden_fields_dict['subtotal'] = item.format_valor_attr(
                'subtotal')

            itens_fields_dict['impostos'] = item.format_total_impostos()
            itens_fields_dict['total'] = item.format_total_com_imposto()
            itens_fields_dict['vprod'] = item.format_vprod()

            itens_hidden_fields_dict['vicms'] = item.format_valor_attr('vicms')
            itens_hidden_fields_dict['vipi'] = item.format_valor_attr('vipi')
            itens_hidden_fields_dict['vicms_st'] = item.format_valor_attr(
                'vicms_st')
            itens_hidden_fields_dict['vfcp'] = item.format_valor_attr('vfcp')
            itens_hidden_fields_dict['vicmsufdest'] = item.format_valor_attr(
                'vicmsufdest')
            itens_hidden_fields_dict['vicmsufremet'] = item.format_valor_attr(
                'vicmsufremet')
            itens_hidden_fields_dict['aliq_pis'] = item.get_aliquota_pis()
            itens_hidden_fields_dict['aliq_cofins'] = item.get_aliquota_cofins(
            )
            itens_hidden_fields_dict['mot_des_icms'] = item.get_mot_deson_icms(
            )

            itens_editable_fields_dict['editable_field_vq_bcpis'] = item.format_valor_attr(
                'vq_bcpis')
            itens_editable_fields_dict['editable_field_vq_bccofins'] = item.format_valor_attr(
                'vq_bccofins')
            itens_editable_fields_dict['editable_field_vpis'] = item.format_valor_attr(
                'vpis')
            itens_editable_fields_dict['editable_field_vcofins'] = item.format_valor_attr(
                'vcofins')
            itens_editable_fields_dict['editable_field_vicms_deson'] = item.format_valor_attr(
                'vicms_deson')
            itens_editable_fields_dict[
                'editable_field_inf_ad_prod'] = item.inf_ad_prod

            itens_venda_dict['fields'] = itens_fields_dict
            itens_venda_dict['hidden_fields'] = itens_hidden_fields_dict
            itens_venda_dict['editable_fields'] = itens_editable_fields_dict

            data.append(itens_venda_dict)

        for pagamento in pagamentos:
            pagamento_dict = {}
            pagamento_dict['model'] = 'vendas.pagamento'
            pagamento_dict['pk'] = pagamento.id
            pagamento_fields_dict = {}
            pagamento_fields_dict['id'] = pagamento.id
            pagamento_fields_dict['vencimento'] = pagamento.format_vencimento
            pagamento_fields_dict[
                'valor_parcela'] = pagamento.format_valor_parcela

            pagamento_dict['fields'] = pagamento_fields_dict

            data.append(pagamento_dict)

        return HttpResponse(json.dumps(data), content_type='application/json')
