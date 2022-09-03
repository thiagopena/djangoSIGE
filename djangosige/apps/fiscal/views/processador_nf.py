# -*- coding: utf-8 -*-

from djangosige.apps.fiscal.models import NotaFiscalSaida, NotaFiscalEntrada, ConfiguracaoNotaFiscal, AutXML, \
    ErrosValidacaoNotaFiscal, RespostaSefazNotaFiscal, NaturezaOperacao, GrupoFiscal, \
    ICMS, ICMSUFDest, ICMSSN, IPI, PIS, COFINS
from djangosige.configs.settings import MEDIA_ROOT
from djangosige.apps.cadastro.models import COD_UF, PessoaJuridica, PessoaFisica, Fornecedor, Cliente, Empresa, Transportadora, Endereco, Telefone, Produto, Unidade
from djangosige.apps.compras.models import PedidoCompra, ItensCompra
from djangosige.apps.vendas.models import PedidoVenda, ItensVenda

from djangosige.apps.vendas.models import Pagamento as PagamentoVenda

from pysignfe.nf_e import nf_e
from pysignfe.nfe.manual_700.nfe_400 import NFe as NFe_400
from pysignfe.nfe.manual_700.nfe_400 import Det as Det_400
from pysignfe.nfe.manual_700.nfe_400 import autXML as autXML_400
from pysignfe.nfe.manual_700.nfe_400 import Dup as Dup_400

from ssl import SSLError


class ProcessadorNotaFiscal(object):

    def __init__(self):
        self.conf_nfe = None
        self.nova_nfe = None
        self.processo = None
        self.info_certificado = {}
        self.message = ''
        self.erro = False

    def salvar_mensagem(self, message, erro=False):
        self.erro = erro
        self.message = message
        return erro

    def montar_nota(self, nota_obj, versao='4.00'):
        if versao == '4.00':
            nfe = NFe_400()

        nfe.infNFe.ide.natOp.valor = nota_obj.natop
        nfe.infNFe.ide.indPag.valor = nota_obj.indpag
        nfe.infNFe.ide.serie.valor = nota_obj.serie
        nfe.infNFe.ide.nNF.valor = nota_obj.n_nf_saida

        if nota_obj.dhemi:
            nfe.infNFe.ide.dhEmi.valor = nota_obj.dhemi.replace(tzinfo=None)
        if nota_obj.dhsaient:
            nfe.infNFe.ide.dhSaiEnt.valor = nota_obj.dhsaient.replace(
                tzinfo=None)

        nfe.infNFe.ide.tpNF.valor = nota_obj.tpnf
        nfe.infNFe.ide.idDest.valor = nota_obj.iddest
        nfe.infNFe.ide.tpImp.valor = nota_obj.tp_imp
        nfe.infNFe.ide.finNFe.valor = nota_obj.fin_nfe
        nfe.infNFe.ide.indFinal.valor = nota_obj.ind_final
        nfe.infNFe.ide.indPres.valor = nota_obj.ind_pres
        nfe.infNFe.ide.procEmi.valor = 0

        # Identificação do emitente
        if nota_obj.emit_saida:
            nfe.infNFe.emit.CNPJ.valor = nota_obj.emit_saida.cpf_cnpj_apenas_digitos
            nfe.infNFe.emit.xNome.valor = nota_obj.emit_saida.nome_razao_social
            nfe.infNFe.emit.xFant.valor = nota_obj.emit_saida.pessoa_jur_info.nome_fantasia
            nfe.infNFe.emit.IE.valor = nota_obj.emit_saida.pessoa_jur_info.inscricao_estadual
            nfe.infNFe.emit.IEST.valor = nota_obj.emit_saida.iest

            if nota_obj.emit_saida.pessoa_jur_info.sit_fiscal == 'SN':
                nfe.infNFe.emit.CRT.valor = '1'
            elif nota_obj.emit_saida.pessoa_jur_info.sit_fiscal == 'SE':
                nfe.infNFe.emit.CRT.valor = '2'
            elif nota_obj.emit_saida.pessoa_jur_info.sit_fiscal in ('LR', 'LP'):
                nfe.infNFe.emit.CRT.valor = '3'

            if nota_obj.emit_saida.endereco_padrao:
                nfe.infNFe.emit.enderEmit.xLgr.valor = nota_obj.emit_saida.endereco_padrao.logradouro
                nfe.infNFe.emit.enderEmit.nro.valor = nota_obj.emit_saida.endereco_padrao.numero
                nfe.infNFe.emit.enderEmit.xCpl.valor = nota_obj.emit_saida.endereco_padrao.complemento
                nfe.infNFe.emit.enderEmit.xBairro.valor = nota_obj.emit_saida.endereco_padrao.bairro
                nfe.infNFe.emit.enderEmit.cMun.valor = nota_obj.emit_saida.endereco_padrao.cmun
                nfe.infNFe.ide.cMunFG.valor = nota_obj.emit_saida.endereco_padrao.cmun
                nfe.infNFe.emit.enderEmit.xMun.valor = nota_obj.emit_saida.endereco_padrao.municipio
                nfe.infNFe.emit.enderEmit.UF.valor = nota_obj.emit_saida.endereco_padrao.uf
                nfe.infNFe.emit.enderEmit.CEP.valor = nota_obj.emit_saida.endereco_padrao.cep
                nfe.infNFe.emit.enderEmit.cPais.valor = nota_obj.emit_saida.endereco_padrao.cpais
                nfe.infNFe.emit.enderEmit.xPais.valor = nota_obj.emit_saida.endereco_padrao.pais

            if nota_obj.emit_saida.telefone_padrao:
                nfe.infNFe.emit.enderEmit.fone.valor = nota_obj.emit_saida.telefone_padrao.get_telefone_apenas_digitos()

        # Identificação do destinatario
        if nota_obj.dest_saida:
            if nota_obj.dest_saida.id_estrangeiro:
                nfe.infNFe.dest.idEstrangeiro.valor = nota_obj.dest_saida.id_estrangeiro
            elif nota_obj.dest_saida.tipo_pessoa == 'PF':
                nfe.infNFe.dest.CPF.valor = nota_obj.dest_saida.cpf_cnpj_apenas_digitos
            elif nota_obj.dest_saida.tipo_pessoa == 'PJ':
                nfe.infNFe.dest.CNPJ.valor = nota_obj.dest_saida.cpf_cnpj_apenas_digitos
                nfe.infNFe.dest.IE.valor = nota_obj.dest_saida.inscricao_estadual
                nfe.infNFe.dest.ISUF.valor = nota_obj.dest_saida.pessoa_jur_info.suframa

            nfe.infNFe.dest.xNome.valor = nota_obj.dest_saida.nome_razao_social
            nfe.infNFe.dest.indIEDest.valor = nota_obj.dest_saida.indicador_ie

            if nota_obj.dest_saida.endereco_padrao:
                nfe.infNFe.dest.enderDest.xLgr.valor = nota_obj.dest_saida.endereco_padrao.logradouro
                nfe.infNFe.dest.enderDest.nro.valor = nota_obj.dest_saida.endereco_padrao.numero
                nfe.infNFe.dest.enderDest.xCpl.valor = nota_obj.dest_saida.endereco_padrao.complemento
                nfe.infNFe.dest.enderDest.xBairro.valor = nota_obj.dest_saida.endereco_padrao.bairro
                nfe.infNFe.dest.enderDest.cMun.valor = nota_obj.dest_saida.endereco_padrao.cmun
                nfe.infNFe.dest.enderDest.xMun.valor = nota_obj.dest_saida.endereco_padrao.municipio
                nfe.infNFe.dest.enderDest.UF.valor = nota_obj.dest_saida.endereco_padrao.uf
                nfe.infNFe.dest.enderDest.CEP.valor = nota_obj.dest_saida.endereco_padrao.cep
                nfe.infNFe.dest.enderDest.cPais.valor = nota_obj.dest_saida.endereco_padrao.cpais
                nfe.infNFe.dest.enderDest.xPais.valor = nota_obj.dest_saida.endereco_padrao.pais

            if nota_obj.dest_saida.telefone_padrao:
                nfe.infNFe.dest.enderDest.fone.valor = nota_obj.dest_saida.telefone_padrao.get_telefone_apenas_digitos()

        # Autorização para obter XML
        for aut in AutXML.objects.filter(nfe=nota_obj):
            a = autXML_400()
            if len(aut.get_cpf_cnpj_apenas_digitos()) <= 11:
                a.CPF.valor = aut.get_cpf_cnpj_apenas_digitos()
            else:
                a.CNPJ.valor = aut.get_cpf_cnpj_apenas_digitos()

            nfe.infNFe.autXML.append(a)

        # Detalhamento dos produtos e servicos
        if nota_obj.venda:
            for index, item in enumerate(nota_obj.venda.itens_venda.all(), 1):
                det = Det_400()
                det.nItem.valor = index
                det.infAdProd.valor = item.inf_ad_prod

                det.prod.CEST.valor = item.produto.cest
                det.prod.cProd.valor = item.produto.codigo
                det.prod.cEAN.valor = item.produto.codigo_barras
                det.prod.xProd.valor = item.produto.descricao
                if item.produto.ncm:
                    det.prod.NCM.valor = item.produto.ncm[0:8]

                    if len(item.produto.ncm) > 8:
                        det.prod.EXTIPI.valor = item.produto.ncm[8:]

                det.prod.CFOP.valor = item.produto.get_cfop_padrao()
                det.prod.uCom.valor = item.produto.get_sigla_unidade()
                det.prod.qCom.valor = item.quantidade
                det.prod.vUnCom.valor = item.valor_unit
                det.prod.vProd.valor = item.vprod
                det.prod.uTrib.valor = det.prod.uCom.valor
                det.prod.qTrib.valor = det.prod.qCom.valor
                det.prod.vUnTrib.valor = det.prod.vUnCom.valor
                det.prod.vFrete.valor = item.valor_rateio_frete
                det.prod.vSeg.valor = item.valor_rateio_seguro
                det.prod.vDesc.valor = item.get_valor_desconto()
                det.prod.vOutro.valor = item.valor_rateio_despesas

                # Impostos
                if item.produto.grupo_fiscal:
                    # Simples Nacional
                    if item.produto.grupo_fiscal.regime_trib == '1':
                        det.imposto.ICMS.regime_tributario = 1
                        # ICMS
                        if item.produto.grupo_fiscal.icms_sn_padrao:
                            icms_sn_obj = item.produto.grupo_fiscal.icms_sn_padrao.get()

                            det.imposto.ICMS.orig.valor = item.produto.origem
                            det.imposto.ICMS.CSOSN.valor = icms_sn_obj.csosn
                            det.imposto.ICMS.modBC.valor = icms_sn_obj.mod_bc
                            det.imposto.ICMS.vBC.valor = item.vbc_icms
                            det.imposto.ICMS.pRedBC.valor = icms_sn_obj.p_red_bc
                            det.imposto.ICMS.pICMS.valor = item.p_icms
                            det.imposto.ICMS.vICMS.valor = item.vicms
                            det.imposto.ICMS.modBCST.valor = icms_sn_obj.mod_bcst
                            det.imposto.ICMS.pMVAST.valor = icms_sn_obj.p_mvast
                            det.imposto.ICMS.pRedBCST.valor = icms_sn_obj.p_red_bcst
                            det.imposto.ICMS.vBCST.valor = item.vbc_icms_st
                            det.imposto.ICMS.pICMSST.valor = item.p_icmsst
                            det.imposto.ICMS.vICMSST.valor = item.vicms_st
                            det.imposto.ICMS.pCredSN.valor = icms_sn_obj.p_cred_sn
                            det.imposto.ICMS.vCredICMSSN.valor = item.vicms_cred_sn
                        else:
                            det.imposto.ICMS.CSOSN.valor = '400'

                    # Regime normal
                    elif item.produto.grupo_fiscal.regime_trib == '0':
                        det.imposto.ICMS.regime_tributario = False
                        # ICMS
                        if item.produto.grupo_fiscal.icms_padrao:
                            icms_obj = item.produto.grupo_fiscal.icms_padrao.get()

                            det.imposto.ICMS.orig.valor = item.produto.origem
                            det.imposto.ICMS.CST.valor = icms_obj.cst.replace(
                                'r', '').replace('p', '')
                            det.imposto.ICMS.modBC.valor = icms_obj.mod_bc
                            det.imposto.ICMS.vBC.valor = item.vbc_icms
                            det.imposto.ICMS.pRedBC.valor = icms_obj.p_red_bc
                            det.imposto.ICMS.pICMS.valor = item.p_icms
                            det.imposto.ICMS.vICMS.valor = item.vicms
                            det.imposto.ICMS.modBCST.valor = icms_obj.mod_bcst
                            det.imposto.ICMS.pMVAST.valor = icms_obj.p_mvast
                            det.imposto.ICMS.pRedBCST.valor = icms_obj.p_red_bcst
                            det.imposto.ICMS.vBCST.valor = item.vbc_icms_st
                            det.imposto.ICMS.pICMSST.valor = item.p_icmsst
                            det.imposto.ICMS.vICMSST.valor = item.vicms_st

                            if item.vicms_deson and icms_obj.mot_des_icms:
                                det.imposto.ICMS.vICMSDeson.valor = item.vicms_deson
                                det.imposto.ICMS.motDesICMS.valor = icms_obj.mot_des_icms

                            # Partilha ICMSPart
                            if icms_obj.cst in ('10p', '90p'):
                                det.imposto.ICMS.partilha = True
                                det.imposto.ICMS.UFST.valor = icms_obj.ufst
                                det.imposto.ICMS.pBCOp.valor = icms_obj.p_bc_op

                    # ICMSUFDest (vendas interestaduais para consumidor final
                    # nao contribuinte)
                    icms_dest = item.produto.grupo_fiscal.icms_dest_padrao.get()
                    if icms_dest.p_fcp_dest or icms_dest.p_icms_dest or icms_dest.p_icms_inter or icms_dest.p_icms_inter_part:
                        det.imposto.ICMSUFDest.vBCUFDest.valor = item.vbc_uf_dest
                        det.imposto.ICMSUFDest.pFCPUFDest.valor = icms_dest.p_fcp_dest
                        det.imposto.ICMSUFDest.pICMSUFDest.valor = icms_dest.p_icms_dest
                        det.imposto.ICMSUFDest.pICMSInter.valor = icms_dest.p_icms_inter
                        det.imposto.ICMSUFDest.pICMSInterPart.valor = icms_dest.p_icms_inter_part
                        det.imposto.ICMSUFDest.vFCPUFDest.valor = item.vfcp
                        det.imposto.ICMSUFDest.vICMSUFDest.valor = item.vicmsufdest
                        det.imposto.ICMSUFDest.vICMSUFRemet.valor = item.vicmsufremet

                    # IPI
                    ipi_obj = item.produto.grupo_fiscal.ipi_padrao.get()
                    if ipi_obj.cst:
                        det.imposto.IPI.CST.valor = ipi_obj.cst
                        det.imposto.IPI.clEnq.valor = ipi_obj.cl_enq
                        det.imposto.IPI.CNPJProd.valor = ipi_obj.get_cnpj_prod_apenas_digitos()
                        det.imposto.IPI.cEnq.valor = ipi_obj.c_enq

                        if ipi_obj.tipo_ipi == '1':
                            det.imposto.IPI.qUnid.valor = item.quantidade
                            det.imposto.IPI.vUnid.valor = ipi_obj.valor_fixo
                        elif ipi_obj.tipo_ipi == '2':
                            det.imposto.IPI.vBC.valor = item.vbc_ipi
                            det.imposto.IPI.pIPI.valor = item.p_ipi

                        det.imposto.IPI.vIPI.valor = item.vipi
                    else:
                        det.imposto.IPI.CST.valor = '99'

                    # PIS
                    pis_obj = item.produto.grupo_fiscal.pis_padrao.get()
                    if pis_obj.cst:
                        det.imposto.PIS.CST.valor = pis_obj.cst

                        if pis_obj.valiq_pis:
                            det.imposto.PIS.qBCProd.valor = item.vq_bcpis
                            det.imposto.PIS.vAliqProd.valor = pis_obj.valiq_pis
                        elif pis_obj.p_pis:
                            det.imposto.PIS.vBC.valor = item.vq_bcpis
                            det.imposto.PIS.pPIS.valor = pis_obj.p_pis

                        det.imposto.PIS.vPIS.valor = item.vpis

                    else:
                        det.imposto.PIS.CST.valor = '99'

                    # COFINS
                    cofins_obj = item.produto.grupo_fiscal.cofins_padrao.get()
                    if cofins_obj.cst:
                        det.imposto.COFINS.CST.valor = cofins_obj.cst

                        if cofins_obj.valiq_cofins:
                            det.imposto.COFINS.qBCProd.valor = item.vq_bccofins
                            det.imposto.COFINS.vAliqProd.valor = cofins_obj.valiq_cofins
                        elif cofins_obj.p_cofins:
                            det.imposto.COFINS.vBC.valor = item.vq_bccofins
                            det.imposto.COFINS.pCOFINS.valor = cofins_obj.p_cofins

                        det.imposto.COFINS.vCOFINS.valor = item.vcofins

                    else:
                        det.imposto.COFINS.CST.valor = '99'

                # Incluir detalhes na nfe
                nfe.infNFe.det.append(det)

        # Totais
        nfe.infNFe.total.ICMSTot.vBC.valor = nota_obj.venda.get_valor_total_attr(
            'vbc_icms')
        nfe.infNFe.total.ICMSTot.vICMS.valor = nota_obj.venda.get_valor_total_attr(
            'vicms')
        nfe.infNFe.total.ICMSTot.vBCST.valor = nota_obj.venda.get_valor_total_attr(
            'vbc_icms_st')
        nfe.infNFe.total.ICMSTot.vST.valor = nota_obj.venda.get_valor_total_attr(
            'vicms_st')
        nfe.infNFe.total.ICMSTot.vProd.valor = nota_obj.venda.get_valor_total_attr(
            'vprod')
        nfe.infNFe.total.ICMSTot.vFrete.valor = nota_obj.venda.frete
        nfe.infNFe.total.ICMSTot.vSeg.valor = nota_obj.venda.seguro
        nfe.infNFe.total.ICMSTot.vDesc.valor = nota_obj.venda.get_valor_desconto_total()
        nfe.infNFe.total.ICMSTot.vIPI.valor = nota_obj.venda.get_valor_total_attr(
            'vipi')
        nfe.infNFe.total.ICMSTot.vPIS.valor = nota_obj.venda.get_valor_total_attr(
            'vpis')
        nfe.infNFe.total.ICMSTot.vCOFINS.valor = nota_obj.venda.get_valor_total_attr(
            'vcofins')
        nfe.infNFe.total.ICMSTot.vOutro.valor = nota_obj.venda.despesas
        nfe.infNFe.total.ICMSTot.vICMSDeson.valor = nota_obj.venda.get_valor_total_attr(
            'vicms_deson')
        nfe.calcula_total_nfe()

        # Transporte
        nfe.infNFe.transp.modFrete.valor = nota_obj.venda.mod_frete
        if nota_obj.venda.transportadora:
            if nota_obj.venda.transportadora.tipo_pessoa == 'PJ':
                nfe.infNFe.transp.transporta.CNPJ.valor = nota_obj.venda.transportadora.cpf_cnpj_apenas_digitos
                nfe.infNFe.transp.transporta.IE.valor = nota_obj.venda.transportadora.pessoa_jur_info.inscricao_estadual
            elif nota_obj.venda.transportadora.tipo_pessoa == 'PF':
                nfe.infNFe.transp.transporta.CPF.valor = nota_obj.venda.transportadora.cpf_cnpj_apenas_digitos

            nfe.infNFe.transp.transporta.xNome.valor = nota_obj.venda.transportadora.nome_razao_social
            nfe.infNFe.transp.transporta.xEnder.valor = nota_obj.venda.transportadora.endereco_padrao.logradouro
            nfe.infNFe.transp.transporta.xMun.valor = nota_obj.venda.transportadora.endereco_padrao.municipio
            nfe.infNFe.transp.transporta.UF.valor = nota_obj.venda.transportadora.endereco_padrao.uf

        if nota_obj.venda.veiculo:
            nfe.infNFe.transp.veicTransp.placa.valor = nota_obj.venda.veiculo.placa
            nfe.infNFe.transp.veicTransp.UF.valor = nota_obj.venda.veiculo.uf

        # Cobranca
        if nota_obj.grupo_cobr:
            nfe.infNFe.cobr.fat.nFat.valor = nota_obj.n_fat
            nfe.infNFe.cobr.fat.vOrig.valor = nota_obj.v_orig
            nfe.infNFe.cobr.fat.vDesc.valor = nota_obj.v_desc
            nfe.infNFe.cobr.fat.vLiq.valor = nota_obj.v_liq

            for pagamento in nota_obj.venda.parcela_pagamento.all():
                d = Dup_400()
                d.nDup.valor = str(pagamento.id)
                d.dVenc.valor = pagamento.vencimento
                d.vDup.valor = pagamento.valor_parcela

                nfe.infNFe.cobr.dup.append(d)

        # Pagamento(NFC-e)
        if nota_obj.mod == '65':
            nfe.infNFe.Pag.tPag.valor = nota_obj.venda.get_forma_pagamento()
            nfe.infNFe.Pag.vPag.valor = nota_obj.venda.valor_total

        # Informacoes adicionais
        nfe.infNFe.infAdic.infAdFisco.valor = nota_obj.inf_ad_fisco
        nfe.infNFe.infAdic.infCpl.valor = nota_obj.inf_cpl

        nfe.gera_nova_chave()

        return nfe

    def importar_xml(self, request):
        if request.POST.get('fornecedor') == 'on':
            self.importar_xml_fornecedor(request)
        else:
            self.importar_xml_cliente(request)

    def importar_xml_cliente(self, request):
        nfe = NFe_400()
        nota_saida = NotaFiscalSaida()
        venda = PedidoVenda()

        xml_nfe = request.FILES['arquivo_xml'].read().decode("utf-8")

        nfe.xml = xml_nfe

        if NotaFiscalSaida.objects.filter(n_nf_saida=str(nfe.infNFe.ide.nNF.valor)).count():
            raise ValueError(
                'Nota com esta numeração já existe na base de dados.')

        nota_saida.n_nf_saida = str(nfe.infNFe.ide.nNF.valor)
        nota_saida.chave = str(nfe.infNFe.Id.valor[-44:])
        nota_saida.natop = nfe.infNFe.ide.natOp.valor
        nota_saida.indpag = str(nfe.infNFe.ide.indPag.valor)
        nota_saida.mod = str(nfe.infNFe.ide.mod.valor)
        nota_saida.serie = str(nfe.infNFe.ide.serie.valor)
        nota_saida.dhemi = nfe.infNFe.ide.dhEmi.valor
        nota_saida.dhsaient = nfe.infNFe.ide.dhSaiEnt.valor
        nota_saida.iddest = str(nfe.infNFe.ide.idDest.valor)
        nota_saida.tp_imp = str(nfe.infNFe.ide.tpImp.valor)
        nota_saida.tp_emis = str(nfe.infNFe.ide.tpEmis.valor)
        nota_saida.tp_amb = str(nfe.infNFe.ide.tpAmb.valor)
        nota_saida.fin_nfe = str(nfe.infNFe.ide.finNFe.valor)
        nota_saida.ind_final = str(nfe.infNFe.ide.indFinal.valor)
        nota_saida.ind_pres = str(nfe.infNFe.ide.indPres.valor)
        nota_saida.tpnf = str(nfe.infNFe.ide.tpNF.valor)
        nota_saida.inf_ad_fisco = str(nfe.infNFe.infAdic.infAdFisco.valor)
        nota_saida.inf_cpl = str(nfe.infNFe.infAdic.infCpl.valor)
        nota_saida.status_nfe = u'3'  # Em digitação

        if nfe.infNFe.cobr.fat.nFat.valor:
            nota_saida.n_fat = str(nfe.infNFe.cobr.fat.nFat.valor)
            nota_saida.v_orig = nfe.infNFe.cobr.fat.vOrig.valor
            nota_saida.v_desc = nfe.infNFe.cobr.fat.vDesc.valor
            nota_saida.v_liq = nfe.infNFe.cobr.fat.vLiq.valor

        # Cliente (destinatario)
        clientes = []

        if nfe.infNFe.dest.CNPJ.valor:
            clientes = [c for c in Cliente.objects.filter(
                tipo_pessoa='PJ') if c.cpf_cnpj_apenas_digitos == nfe.infNFe.dest.CNPJ.valor]
        elif nfe.infNFe.dest.CPF.valor:
            clientes = [c for c in Cliente.objects.filter(
                tipo_pessoa='PF') if c.cpf_cnpj_apenas_digitos == nfe.infNFe.dest.CPF.valor]

        if len(clientes):
            nota_saida.dest_saida = clientes[0]
            venda.cliente = clientes[0]
        else:
            cliente = Cliente()
            cliente.nome_razao_social = nfe.infNFe.dest.xNome.valor
            cliente.indicador_ie = str(nfe.infNFe.dest.indIEDest.valor)
            cliente.criado_por = request.user

            if nfe.infNFe.dest.CNPJ.valor:
                info_cliente = PessoaJuridica()
                cliente.tipo_pessoa = 'PJ'
                info_cliente.cnpj = str(nfe.infNFe.dest.CNPJ.valor)
                info_cliente.suframa = str(nfe.infNFe.dest.ISUF.valor)
                info_cliente.inscricao_estadual = str(nfe.infNFe.dest.IE.valor)
            elif nfe.infNFe.dest.CPF.valor:
                info_cliente = PessoaFisica()
                cliente.tipo_pessoa = 'PF'
                info_cliente.cpf = str(nfe.infNFe.dest.CPF.valor)
            elif nfe.infNFe.dest.idEstrangeiro.valor:
                info_cliente = PessoaJuridica()
                cliente.id_estrangeiro = str(
                    nfe.infNFe.dest.idEstrangeiro.valor)

            ender_cliente = Endereco()
            tel_cliente = Telefone()

            ender_cliente.logradouro = nfe.infNFe.dest.enderDest.xLgr.valor
            ender_cliente.numero = str(nfe.infNFe.dest.enderDest.nro.valor)
            ender_cliente.bairro = nfe.infNFe.dest.enderDest.xBairro.valor
            ender_cliente.complemento = nfe.infNFe.dest.enderDest.xCpl.valor
            ender_cliente.pais = nfe.infNFe.dest.enderDest.xPais.valor
            ender_cliente.cpais = str(nfe.infNFe.dest.enderDest.cPais.valor)
            ender_cliente.municipio = str(
                nfe.infNFe.dest.enderDest.xMun.valor).title()
            ender_cliente.cmun = str(nfe.infNFe.dest.enderDest.cMun.valor)
            ender_cliente.cep = str(nfe.infNFe.dest.enderDest.CEP.valor)
            ender_cliente.uf = nfe.infNFe.dest.enderDest.UF.valor

            tel_cliente.telefone = str(nfe.infNFe.dest.enderDest.fone.valor)

            cliente.save()
            info_cliente.pessoa_id = cliente
            info_cliente.save()
            ender_cliente.pessoa_end = cliente
            ender_cliente.save()
            cliente.endereco_padrao = ender_cliente
            tel_cliente.pessoa_tel = cliente
            tel_cliente.save()
            cliente.telefone_padrao = tel_cliente
            cliente.save()

            nota_saida.dest_saida = cliente
            venda.cliente = cliente

        # Empresa (emitente)
        empresas = []

        if nfe.infNFe.emit.CNPJ.valor:
            empresas = [e for e in Empresa.objects.filter(
                tipo_pessoa='PJ') if e.cpf_cnpj_apenas_digitos == nfe.infNFe.emit.CNPJ.valor]
        elif nfe.infNFe.emit.CPF.valor:
            empresas = [e for e in Empresa.objects.filter(
                tipo_pessoa='PF') if e.cpf_cnpj_apenas_digitos == nfe.infNFe.emit.CPF.valor]

        if len(empresas):
            nota_saida.emit_saida = empresas[0]
        elif nfe.infNFe.emit.CNPJ.valor:
            empresa = Empresa()
            empresa.nome_razao_social = nfe.infNFe.emit.xNome.valor
            empresa.iest = nfe.infNFe.emit.IEST.valor
            empresa.cnae = nfe.infNFe.emit.CNAE.valor
            empresa.criado_por = request.user

            info_empresa = PessoaJuridica()
            empresa.tipo_pessoa = 'PJ'
            info_empresa.cnpj = str(nfe.infNFe.emit.CNPJ.valor)
            info_empresa.nome_fantasia = str(nfe.infNFe.emit.xFant.valor)
            info_empresa.inscricao_estadual = str(nfe.infNFe.emit.IE.valor)
            info_empresa.inscricao_municipal = str(nfe.infNFe.emit.IM.valor)

            ender_empresa = Endereco()
            tel_empresa = Telefone()

            ender_empresa.logradouro = nfe.infNFe.emit.enderEmit.xLgr.valor
            ender_empresa.numero = str(nfe.infNFe.emit.enderEmit.nro.valor)
            ender_empresa.bairro = nfe.infNFe.emit.enderEmit.xBairro.valor
            ender_empresa.complemento = nfe.infNFe.emit.enderEmit.xCpl.valor
            ender_empresa.pais = nfe.infNFe.emit.enderEmit.xPais.valor
            ender_empresa.cpais = str(nfe.infNFe.emit.enderEmit.cPais.valor)
            ender_empresa.municipio = str(
                nfe.infNFe.emit.enderEmit.xMun.valor).title()
            ender_empresa.cmun = str(nfe.infNFe.emit.enderEmit.cMun.valor)
            ender_empresa.cep = str(nfe.infNFe.emit.enderEmit.CEP.valor)
            ender_empresa.uf = nfe.infNFe.emit.enderEmit.UF.valor

            tel_empresa.telefone = str(nfe.infNFe.emit.enderEmit.fone.valor)

            empresa.save()
            info_empresa.pessoa_id = empresa
            info_empresa.save()
            ender_empresa.pessoa_end = empresa
            ender_empresa.save()
            empresa.endereco_padrao = ender_empresa
            tel_empresa.pessoa_tel = empresa
            tel_empresa.save()
            empresa.telefone_padrao = tel_empresa
            empresa.save()

            nota_saida.emit_saida = empresa

        # Venda
        if str(nfe.infNFe.ide.mod.valor) == '55':
            venda.ind_final = False
        elif str(nfe.infNFe.ide.mod.valor) == '65':
            venda.ind_final = True

        # Transportadora
        if nfe.infNFe.transp.transporta.CNPJ.valor or nfe.infNFe.transp.transporta.CPF.valor:
            transportadoras = []
            if nfe.infNFe.transp.transporta.CNPJ.valor:
                transportadoras = [t for t in Transportadora.objects.filter(
                    tipo_pessoa='PJ') if t.cpf_cnpj_apenas_digitos == nfe.infNFe.transp.transporta.CNPJ.valor]
            elif nfe.infNFe.transp.transporta.CPF.valor:
                transportadoras = [t for t in Transportadora.objects.filter(
                    tipo_pessoa='PF') if t.cpf_cnpj_apenas_digitos == nfe.infNFe.transp.transporta.CPF.valor]

            if len(transportadoras):
                venda.transportadora = transportadoras[0]
            else:
                transporta = Transportadora()
                transporta.nome_razao_social = nfe.infNFe.transp.transporta.xNome.valor

                if nfe.infNFe.transp.transporta.CNPJ.valor:
                    info_transporta = PessoaJuridica()
                    transporta.tipo_pessoa = 'PJ'
                    info_transporta.cnpj = str(
                        nfe.infNFe.transp.transporta.CNPJ.valor)
                    info_transporta.inscricao_estadual = str(
                        nfe.infNFe.transp.transporta.IE.valor)
                elif nfe.infNFe.transp.transporta.CPF.valor:
                    info_transporta = PessoaFisica()
                    transporta.tipo_pessoa = 'PF'
                    info_transporta.cpf = str(
                        nfe.infNFe.transp.transporta.CPF.valor)

                ender_transporta = Endereco()
                ender_transporta.logradouro = nfe.infNFe.transp.transporta.xEnder.valor
                ender_transporta.municipio = nfe.infNFe.transp.transporta.xMun.valor
                ender_transporta.uf = nfe.infNFe.transp.transporta.UF.valor

                transporta.save()
                info_transporta.pessoa_id = transporta
                info_transporta.save()
                ender_transporta.pessoa_end = transporta
                ender_transporta.save()
                transporta.endereco_padrao = ender_transporta
                transporta.save()

                venda.transportadora = transporta

        venda.mod_frete = str(nfe.infNFe.transp.modFrete.valor)
        venda.valor_total = nfe.infNFe.total.ICMSTot.vNF.valor
        venda.tipo_desconto = u'0'
        venda.desconto = nfe.infNFe.total.ICMSTot.vDesc.valor
        venda.despesas = nfe.infNFe.total.ICMSTot.vOutro.valor
        venda.frete = nfe.infNFe.total.ICMSTot.vFrete.valor
        venda.seguro = nfe.infNFe.total.ICMSTot.vSeg.valor
        venda.impostos = 0
        venda.status = u'3'  # Importado
        venda.save()

        # ItensVenda/Produto/NaturezaOperacao/Unidade
        for det in nfe.infNFe.det:
            itens_venda = ItensVenda()
            itens_venda.venda_id = venda
            produtos = Produto.objects.filter(descricao=det.prod.xProd.valor)

            # Produto
            if len(produtos):
                produto = produtos[0]
                if not produto.venda:
                    produto.venda = det.prod.vUnCom.valor
            else:
                produto = Produto()
                produto.descricao = str(det.prod.xProd.valor)
                produto.codigo = str(det.prod.cProd.valor)[0:15]
                produto.codigo_barras = str(det.prod.cEAN.valor)
                produto.cest = str(det.prod.CEST.valor)
                produto.origem = str(det.imposto.ICMS.orig.valor)
                produto.controlar_estoque = False
                if det.prod.EXTIPI.valor:
                    produto.ncm = str(det.prod.NCM.valor) + \
                        str(det.prod.EXTIPI.valor)
                else:
                    produto.ncm = str(det.prod.NCM.valor)
                produto.venda = det.prod.vUnCom.valor
                produto.inf_adicionais = det.infAdProd.valor

                # Natureza Operacao
                nat_ops = NaturezaOperacao.objects.filter(
                    cfop=str(det.prod.CFOP.valor))
                if len(nat_ops):
                    nat_op = nat_ops[0]
                else:
                    nat_op = NaturezaOperacao()
                    nat_op.cfop = str(det.prod.CFOP.valor)
                    nat_op.set_values_by_cfop()
                    nat_op.save()

                produto.cfop_padrao = nat_op

                # Grupo Fiscal
                grupo_fiscal = GrupoFiscal()
                grupo_fiscal.descricao = 'Produto: ' + \
                    str(det.prod.xProd.valor) + ' (Importado por XML)'
                if det.imposto.ICMS.regime_tributario != 1:
                    grupo_fiscal.regime_trib = '0'  # Normal
                    grupo_fiscal.save()
                    # ICMS
                    grupo_icms = ICMS()
                    grupo_icms.grupo_fiscal = grupo_fiscal
                    grupo_icms.cst = str(det.imposto.ICMS.CST.valor)
                    grupo_icms.mod_bc = str(det.imposto.ICMS.modBC.valor)
                    grupo_icms.p_icms = det.imposto.ICMS.pICMS.valor
                    grupo_icms.p_red_bc = det.imposto.ICMS.pRedBC.valor
                    grupo_icms.mod_bcst = str(det.imposto.ICMS.modBCST.valor)
                    grupo_icms.p_mvast = det.imposto.ICMS.pMVAST.valor
                    grupo_icms.p_red_bcst = det.imposto.ICMS.pRedBCST.valor
                    grupo_icms.p_icmsst = det.imposto.ICMS.pICMSST.valor
                    grupo_icms.mot_des_icms = str(
                        det.imposto.ICMS.motDesICMS.valor)
                    grupo_icms.p_dif = det.imposto.ICMS.pDif.valor
                    grupo_icms.p_bc_op = det.imposto.ICMS.pBCOp.valor
                    grupo_icms.ufst = str(det.imposto.ICMS.UFST.valor)
                    grupo_icms.save()
                else:
                    grupo_fiscal.regime_trib = '1'  # Simples
                    grupo_fiscal.save()
                    # ICMSSN
                    grupo_icmssn = ICMSSN()
                    grupo_icmssn.grupo_fiscal = grupo_fiscal
                    grupo_icmssn.csosn = str(det.imposto.ICMS.CSOSN.valor)
                    grupo_icmssn.p_cred_sn = det.imposto.ICMS.pCredSN.valor
                    grupo_icmssn.mod_bc = str(det.imposto.ICMS.modBC.valor)
                    grupo_icmssn.p_icms = det.imposto.ICMS.pICMS.valor
                    grupo_icmssn.p_red_bc = det.imposto.ICMS.pRedBC.valor
                    grupo_icmssn.mod_bcst = str(det.imposto.ICMS.modBCST.valor)
                    grupo_icmssn.p_mvast = det.imposto.ICMS.pMVAST.valor
                    grupo_icmssn.p_red_bcst = det.imposto.ICMS.pRedBCST.valor
                    grupo_icmssn.p_icmsst = det.imposto.ICMS.pICMSST.valor
                    grupo_icmssn.save()

                # ICMSUFDest
                grupo_icmsufdest = ICMSUFDest()
                grupo_icmsufdest.grupo_fiscal = grupo_fiscal
                if det.imposto.ICMSUFDest.xml:
                    grupo_icmsufdest.p_fcp_dest = det.imposto.ICMSUFDest.pFCPUFDest.valor
                    grupo_icmsufdest.p_icms_dest = det.imposto.ICMSUFDest.pICMSUFDest.valor
                    grupo_icmsufdest.p_icms_inter = det.imposto.ICMSUFDest.pICMSInter.valor
                    grupo_icmsufdest.p_icms_inter_part = det.imposto.ICMSUFDest.pICMSInterPart.valor

                grupo_icmsufdest.save()

                # IPI
                grupo_ipi = IPI()
                grupo_ipi.grupo_fiscal = grupo_fiscal
                if det.imposto.IPI.xml:
                    grupo_ipi.cst = str(det.imposto.IPI.CST.valor)
                    grupo_ipi.cl_enq = str(det.imposto.IPI.clEnq.valor)
                    grupo_ipi.c_enq = str(det.imposto.IPI.cEnq.valor)
                    grupo_ipi.cnpj_prod = str(det.imposto.IPI.CNPJProd.valor)

                    if det.imposto.IPI.qUnid.valor or det.imposto.IPI.vUnid.valor:
                        grupo_ipi.tipo_ipi = u'1'
                        grupo_ipi.valor_fixo = det.imposto.IPI.vUnid.valor
                    elif det.imposto.IPI.vBC.valor or det.imposto.IPI.pIPI.valor:
                        grupo_ipi.tipo_ipi = u'2'
                        grupo_ipi.p_ipi = det.imposto.IPI.pIPI.valor
                    else:
                        grupo_ipi.tipo_ipi = u'0'

                grupo_ipi.save()

                # PIS
                grupo_pis = PIS()
                grupo_pis.grupo_fiscal = grupo_fiscal
                if det.imposto.PIS.CST.valor:
                    grupo_pis.cst = det.imposto.PIS.CST.valor
                    grupo_pis.p_pis = det.imposto.PIS.pPIS.valor
                    grupo_pis.valiq_pis = det.imposto.PIS.vAliqProd.valor

                grupo_pis.save()

                # COFINS
                grupo_cofins = COFINS()
                grupo_cofins.grupo_fiscal = grupo_fiscal
                if det.imposto.COFINS.CST.valor:
                    grupo_cofins.cst = det.imposto.COFINS.CST.valor
                    grupo_cofins.p_cofins = det.imposto.COFINS.pCOFINS.valor
                    grupo_cofins.valiq_cofins = det.imposto.COFINS.vAliqProd.valor

                grupo_cofins.save()

                produto.grupo_fiscal = grupo_fiscal

                # Unidade
                unidades = Unidade.objects.filter(
                    sigla_unidade=det.prod.uCom.valor)
                if len(unidades):
                    unidade = unidades[0]
                else:
                    unidade = Unidade()
                    if len(det.prod.uCom.valor) > 3:
                        unidade.unidade_desc = det.prod.uCom.valor
                        unidade.sigla_unidade = det.prod.uCom.valor[0:3]
                    else:
                        unidade.unidade_desc = det.prod.uCom.valor
                        unidade.sigla_unidade = det.prod.uCom.valor
                    unidade.save()

                produto.unidade = unidade
                produto.save()

            itens_venda.produto = produto
            itens_venda.quantidade = det.prod.qCom.valor
            itens_venda.valor_unit = det.prod.vUnCom.valor
            itens_venda.tipo_desconto = u'0'
            itens_venda.desconto = det.prod.vDesc.valor
            itens_venda.subtotal = det.prod.vProd.valor
            itens_venda.inf_ad_prod = det.infAdProd.valor

            # Rateio
            itens_venda.valor_rateio_frete = det.prod.vFrete.valor
            itens_venda.valor_rateio_despesas = det.prod.vOutro.valor
            itens_venda.valor_rateio_seguro = det.prod.vSeg.valor

            # Bases de calculo
            itens_venda.vbc_icms = det.imposto.ICMS.vBC.valor
            itens_venda.vbc_icms_st = det.imposto.ICMS.vBCST.valor
            itens_venda.vbc_ipi = det.imposto.IPI.vBC.valor

            # Valores e aliquotas
            itens_venda.vicms = det.imposto.ICMS.vICMS.valor
            itens_venda.vicms_st = det.imposto.ICMS.vICMSST.valor
            itens_venda.vipi = det.imposto.IPI.vIPI.valor

            if det.imposto.ICMSUFDest.xml:
                itens_venda.vicmsufdest = det.imposto.vICMSUFDest.valor
                itens_venda.vicmsufremet = det.imposto.vICMSUFRemet.valor
                itens_venda.vfcp = det.imposto.vFCPUFDest.valor

            itens_venda.vicms_deson = det.imposto.ICMS.vICMSDeson.valor
            itens_venda.p_icms = det.imposto.ICMS.pICMS.valor
            itens_venda.p_icmsst = det.imposto.ICMS.pICMSST.valor
            itens_venda.p_ipi = det.imposto.IPI.pIPI.valor

            # Valores do PIS e COFINS
            if det.imposto.PIS.vBC.valor:
                itens_venda.vq_bcpis = det.imposto.PIS.vBC.valor
            elif det.imposto.PIS.qBCProd.valor:
                itens_venda.vq_bcpis = det.imposto.PIS.qBCProd.valor

            if det.imposto.COFINS.vBC.valor:
                itens_venda.vq_bccofins = det.imposto.COFINS.vBC.valor
            elif det.imposto.COFINS.qBCProd.valor:
                itens_venda.vq_bccofins = det.imposto.COFINS.qBCProd.valor

            itens_venda.vpis = det.imposto.PIS.vPIS.valor
            itens_venda.vcofins = det.imposto.COFINS.vCOFINS.valor
            itens_venda.auto_calcular_impostos = False

            itens_venda.save()
            venda.impostos += itens_venda.get_total_impostos()

        venda.save()
        nota_saida.venda = venda
        nota_saida.save()

        # Informacoes de cobranca
        for i, d in enumerate(nfe.infNFe.cobr.dup, 1):
            pagamento = PagamentoVenda()
            pagamento.venda_id = venda
            pagamento.indice_parcela = i
            pagamento.vencimento = d.dVenc.valor
            pagamento.valor_parcela = d.vDup.valor
            pagamento.save()

    def importar_xml_fornecedor(self, request):
        nfe = NFe_400()
        nota_entrada = NotaFiscalEntrada()
        compra = PedidoCompra()

        xml_nfe = request.FILES['arquivo_xml'].read().decode("utf-8")

        nfe.xml = xml_nfe

        nota_entrada.n_nf_entrada = str(nfe.infNFe.ide.nNF.valor)
        nota_entrada.chave = str(nfe.infNFe.Id.valor[-44:])
        nota_entrada.natop = nfe.infNFe.ide.natOp.valor
        nota_entrada.indpag = str(nfe.infNFe.ide.indPag.valor)
        nota_entrada.mod = str(nfe.infNFe.ide.mod.valor)
        nota_entrada.serie = str(nfe.infNFe.ide.serie.valor)
        nota_entrada.dhemi = nfe.infNFe.ide.dhEmi.valor
        nota_entrada.dhsaient = nfe.infNFe.ide.dhSaiEnt.valor
        nota_entrada.iddest = str(nfe.infNFe.ide.idDest.valor)
        nota_entrada.tp_imp = str(nfe.infNFe.ide.tpImp.valor)
        nota_entrada.tp_emis = str(nfe.infNFe.ide.tpEmis.valor)
        nota_entrada.tp_amb = str(nfe.infNFe.ide.tpAmb.valor)
        nota_entrada.fin_nfe = str(nfe.infNFe.ide.finNFe.valor)
        nota_entrada.ind_final = str(nfe.infNFe.ide.indFinal.valor)
        nota_entrada.ind_pres = str(nfe.infNFe.ide.indPres.valor)
        nota_entrada.inf_ad_fisco = str(nfe.infNFe.infAdic.infAdFisco.valor)
        nota_entrada.inf_cpl = str(nfe.infNFe.infAdic.infCpl.valor)
        nota_entrada.status_nfe = u'9'  # Importada

        # Fornecedor (emitente)
        fornecedores = []

        if nfe.infNFe.emit.CNPJ.valor:
            fornecedores = [f for f in Fornecedor.objects.filter(
                tipo_pessoa='PJ') if f.cpf_cnpj_apenas_digitos == nfe.infNFe.emit.CNPJ.valor]
        elif nfe.infNFe.emit.CPF.valor:
            fornecedores = [f for f in Fornecedor.objects.filter(
                tipo_pessoa='PF') if f.cpf_cnpj_apenas_digitos == nfe.infNFe.emit.CPF.valor]

        if len(fornecedores):
            nota_entrada.emit_entrada = fornecedores[0]
            compra.fornecedor = fornecedores[0]
        else:
            fornecedor = Fornecedor()
            fornecedor.nome_razao_social = nfe.infNFe.emit.xNome.valor
            fornecedor.criado_por = request.user

            if nfe.infNFe.emit.CNPJ.valor:
                info_fornecedor = PessoaJuridica()
                fornecedor.tipo_pessoa = 'PJ'
                info_fornecedor.cnpj = str(nfe.infNFe.emit.CNPJ.valor)
                info_fornecedor.nome_fantasia = str(
                    nfe.infNFe.emit.xFant.valor)
                info_fornecedor.inscricao_estadual = str(
                    nfe.infNFe.emit.IE.valor)
            elif nfe.infNFe.emit.CPF.valor:
                info_fornecedor = PessoaFisica()
                fornecedor.tipo_pessoa = 'PF'
                info_fornecedor.cpf = str(nfe.infNFe.emit.CPF.valor)

            ender_fornecedor = Endereco()
            tel_fornecedor = Telefone()

            ender_fornecedor.logradouro = nfe.infNFe.emit.enderEmit.xLgr.valor
            ender_fornecedor.numero = str(nfe.infNFe.emit.enderEmit.nro.valor)
            ender_fornecedor.bairro = nfe.infNFe.emit.enderEmit.xBairro.valor
            ender_fornecedor.complemento = nfe.infNFe.emit.enderEmit.xCpl.valor
            ender_fornecedor.pais = nfe.infNFe.emit.enderEmit.xPais.valor
            ender_fornecedor.cpais = str(nfe.infNFe.emit.enderEmit.cPais.valor)
            ender_fornecedor.municipio = str(
                nfe.infNFe.emit.enderEmit.xMun.valor).title()
            ender_fornecedor.cmun = str(nfe.infNFe.emit.enderEmit.cMun.valor)
            ender_fornecedor.cep = str(nfe.infNFe.emit.enderEmit.CEP.valor)
            ender_fornecedor.uf = nfe.infNFe.emit.enderEmit.UF.valor

            tel_fornecedor.telefone = str(nfe.infNFe.emit.enderEmit.fone.valor)

            fornecedor.save()
            info_fornecedor.pessoa_id = fornecedor
            info_fornecedor.save()
            ender_fornecedor.pessoa_end = fornecedor
            ender_fornecedor.save()
            fornecedor.endereco_padrao = ender_fornecedor
            tel_fornecedor.pessoa_tel = fornecedor
            tel_fornecedor.save()
            fornecedor.telefone_padrao = tel_fornecedor
            fornecedor.save()

            nota_entrada.emit_entrada = fornecedor
            compra.fornecedor = fornecedor

        # Empresa (destinatario)
        empresas = []

        if nfe.infNFe.dest.CNPJ.valor:
            empresas = [e for e in Empresa.objects.filter(
                tipo_pessoa='PJ') if e.cpf_cnpj_apenas_digitos == nfe.infNFe.dest.CNPJ.valor]
            if len(empresas):
                nota_entrada.dest_entrada = fornecedores[0]
            else:
                empresa = Empresa()
                empresa.nome_razao_social = nfe.infNFe.dest.xNome.valor
                empresa.criado_por = request.user

                info_empresa = PessoaJuridica()
                empresa.tipo_pessoa = 'PJ'
                info_empresa.cnpj = str(nfe.infNFe.dest.CNPJ.valor)
                info_empresa.inscricao_estadual = str(nfe.infNFe.dest.IE.valor)

                ender_empresa = Endereco()
                tel_empresa = Telefone()

                ender_empresa.logradouro = nfe.infNFe.dest.enderDest.xLgr.valor
                ender_empresa.numero = str(nfe.infNFe.dest.enderDest.nro.valor)
                ender_empresa.bairro = nfe.infNFe.dest.enderDest.xBairro.valor
                ender_empresa.complemento = nfe.infNFe.dest.enderDest.xCpl.valor
                ender_empresa.pais = nfe.infNFe.dest.enderDest.xPais.valor
                ender_empresa.cpais = str(
                    nfe.infNFe.dest.enderDest.cPais.valor)
                ender_empresa.municipio = str(
                    nfe.infNFe.dest.enderDest.xMun.valor).title()
                ender_empresa.cmun = str(nfe.infNFe.dest.enderDest.cMun.valor)
                ender_empresa.cep = str(nfe.infNFe.dest.enderDest.CEP.valor)
                ender_empresa.uf = nfe.infNFe.dest.enderDest.UF.valor

                tel_empresa.telefone = str(
                    nfe.infNFe.dest.enderDest.fone.valor)

                empresa.save()
                info_empresa.pessoa_id = empresa
                info_empresa.save()
                ender_empresa.pessoa_end = empresa
                ender_empresa.save()
                empresa.endereco_padrao = ender_empresa
                tel_empresa.pessoa_tel = empresa
                tel_empresa.save()
                empresa.telefone_padrao = tel_empresa
                empresa.save()

                nota_entrada.dest_entrada = empresa

        # Compra
        compra.mod_frete = str(nfe.infNFe.transp.modFrete.valor)
        compra.valor_total = nfe.infNFe.total.ICMSTot.vNF.valor
        compra.tipo_desconto = u'0'
        compra.desconto = nfe.infNFe.total.ICMSTot.vDesc.valor
        compra.despesas = nfe.infNFe.total.ICMSTot.vOutro.valor
        compra.frete = nfe.infNFe.total.ICMSTot.vFrete.valor
        compra.seguro = nfe.infNFe.total.ICMSTot.vSeg.valor
        compra.total_icms = nfe.infNFe.total.ICMSTot.vICMS.valor
        compra.total_ipi = nfe.infNFe.total.ICMSTot.vIPI.valor
        compra.status = u'3'  # Importado
        compra.save()

        # ItensCompra/Produto/Unidade
        for det in nfe.infNFe.det:
            itens_compra = ItensCompra()
            itens_compra.compra_id = compra
            produtos = Produto.objects.filter(descricao=det.prod.xProd.valor)

            # Produto
            if len(produtos):
                produto = produtos[0]
                if not produto.custo:
                    produto.custo = det.prod.vUnCom.valor
            else:
                produto = Produto()
                produto.descricao = str(det.prod.xProd.valor)
                produto.codigo = str(det.prod.cProd.valor)[0:15]
                produto.codigo_barras = str(det.prod.cEAN.valor)
                produto.cest = str(det.prod.CEST.valor)
                produto.origem = str(det.imposto.ICMS.orig.valor)
                produto.controlar_estoque = False
                if det.prod.EXTIPI.valor:
                    produto.ncm = str(det.prod.NCM.valor) + \
                        str(det.prod.EXTIPI.valor)
                else:
                    produto.ncm = str(det.prod.NCM.valor)
                produto.custo = det.prod.vUnCom.valor
                produto.inf_adicionais = det.infAdProd.valor

                # Natureza Operacao
                nat_ops = NaturezaOperacao.objects.filter(
                    cfop=str(det.prod.CFOP.valor))
                if len(nat_ops):
                    nat_op = nat_ops[0]
                else:
                    nat_op = NaturezaOperacao()
                    nat_op.cfop = str(det.prod.CFOP.valor)
                    nat_op.set_values_by_cfop()
                    nat_op.save()

                produto.cfop_padrao = nat_op

                # Grupo Fiscal
                grupo_fiscal = GrupoFiscal()
                grupo_fiscal.descricao = 'Produto: ' + \
                    str(det.prod.xProd.valor) + ' (Importado por XML)'
                if det.imposto.ICMS.regime_tributario != 1:
                    grupo_fiscal.regime_trib = '0'  # Normal
                    grupo_fiscal.save()
                    # ICMS
                    grupo_icms = ICMS()
                    grupo_icms.grupo_fiscal = grupo_fiscal
                    grupo_icms.cst = str(det.imposto.ICMS.CST.valor)
                    grupo_icms.mod_bc = str(det.imposto.ICMS.modBC.valor)
                    grupo_icms.p_icms = det.imposto.ICMS.pICMS.valor
                    grupo_icms.p_red_bc = det.imposto.ICMS.pRedBC.valor
                    grupo_icms.mod_bcst = str(det.imposto.ICMS.modBCST.valor)
                    grupo_icms.p_mvast = det.imposto.ICMS.pMVAST.valor
                    grupo_icms.p_red_bcst = det.imposto.ICMS.pRedBCST.valor
                    grupo_icms.p_icmsst = det.imposto.ICMS.pICMSST.valor
                    grupo_icms.mot_des_icms = str(
                        det.imposto.ICMS.motDesICMS.valor)
                    grupo_icms.p_dif = det.imposto.ICMS.pDif.valor
                    grupo_icms.p_bc_op = det.imposto.ICMS.pBCOp.valor
                    grupo_icms.ufst = str(det.imposto.ICMS.UFST.valor)
                    grupo_icms.save()
                else:
                    grupo_fiscal.regime_trib = '1'  # Simples
                    grupo_fiscal.save()
                    # ICMSSN
                    grupo_icmssn = ICMSSN()
                    grupo_icmssn.grupo_fiscal = grupo_fiscal
                    grupo_icmssn.csosn = str(det.imposto.ICMS.CSOSN.valor)
                    grupo_icmssn.p_cred_sn = det.imposto.ICMS.pCredSN.valor
                    grupo_icmssn.mod_bc = str(det.imposto.ICMS.modBC.valor)
                    grupo_icmssn.p_icms = det.imposto.ICMS.pICMS.valor
                    grupo_icmssn.p_red_bc = det.imposto.ICMS.pRedBC.valor
                    grupo_icmssn.mod_bcst = str(det.imposto.ICMS.modBCST.valor)
                    grupo_icmssn.p_mvast = det.imposto.ICMS.pMVAST.valor
                    grupo_icmssn.p_red_bcst = det.imposto.ICMS.pRedBCST.valor
                    grupo_icmssn.p_icmsst = det.imposto.ICMS.pICMSST.valor
                    grupo_icmssn.save()

                # ICMSUFDest
                if det.imposto.ICMSUFDest.xml:
                    grupo_icmsufdest = ICMSUFDest()
                    grupo_icmsufdest.grupo_fiscal = grupo_fiscal
                    grupo_icmsufdest.p_fcp_dest = det.imposto.ICMSUFDest.pFCPUFDest.valor
                    grupo_icmsufdest.p_icms_dest = det.imposto.ICMSUFDest.pICMSUFDest.valor
                    grupo_icmsufdest.p_icms_inter = det.imposto.ICMSUFDest.pICMSInter.valor
                    grupo_icmsufdest.p_icms_inter_part = det.imposto.ICMSUFDest.pICMSInterPart.valor
                    grupo_icmsufdest.save()

                # IPI
                if det.imposto.IPI.xml:
                    grupo_ipi = IPI()
                    grupo_ipi.grupo_fiscal = grupo_fiscal
                    grupo_ipi.cst = str(det.imposto.IPI.CST.valor)
                    grupo_ipi.cl_enq = str(det.imposto.IPI.clEnq.valor)
                    grupo_ipi.c_enq = str(det.imposto.IPI.cEnq.valor)
                    grupo_ipi.cnpj_prod = str(det.imposto.IPI.CNPJProd.valor)

                    if det.imposto.IPI.qUnid.valor or det.imposto.IPI.vUnid.valor:
                        grupo_ipi.tipo_ipi = u'1'
                        grupo_ipi.valor_fixo = det.imposto.IPI.vUnid.valor
                    elif det.imposto.IPI.vBC.valor or det.imposto.IPI.pIPI.valor:
                        grupo_ipi.tipo_ipi = u'2'
                        grupo_ipi.p_ipi = det.imposto.IPI.pIPI.valor
                    else:
                        grupo_ipi.tipo_ipi = u'0'

                    grupo_ipi.save()

                # PIS
                if det.imposto.PIS.CST.valor:
                    grupo_pis = PIS()
                    grupo_pis.grupo_fiscal = grupo_fiscal
                    grupo_pis.cst = det.imposto.PIS.CST.valor
                    grupo_pis.p_pis = det.imposto.PIS.pPIS.valor
                    grupo_pis.valiq_pis = det.imposto.PIS.vAliqProd.valor
                    grupo_pis.save()

                # COFINS
                if det.imposto.COFINS.CST.valor:
                    grupo_cofins = COFINS()
                    grupo_cofins.grupo_fiscal = grupo_fiscal
                    grupo_cofins.cst = det.imposto.COFINS.CST.valor
                    grupo_cofins.p_cofins = det.imposto.COFINS.pCOFINS.valor
                    grupo_cofins.valiq_cofins = det.imposto.COFINS.vAliqProd.valor
                    grupo_cofins.save()

                produto.grupo_fiscal = grupo_fiscal

                # Unidade
                unidades = Unidade.objects.filter(
                    sigla_unidade=det.prod.uCom.valor)
                if len(unidades):
                    unidade = unidades[0]
                else:
                    unidade = Unidade()
                    if len(det.prod.uCom.valor) > 3:
                        unidade.unidade_desc = det.prod.uCom.valor
                        unidade.sigla_unidade = det.prod.uCom.valor[0:3]
                    else:
                        unidade.unidade_desc = det.prod.uCom.valor
                        unidade.sigla_unidade = det.prod.uCom.valor
                    unidade.save()

                produto.unidade = unidade
                produto.save()

            itens_compra.produto = produto
            itens_compra.quantidade = det.prod.qCom.valor
            itens_compra.valor_unit = det.prod.vUnCom.valor
            itens_compra.tipo_desconto = u'0'
            itens_compra.desconto = det.prod.vDesc.valor
            itens_compra.subtotal = det.prod.vProd.valor
            itens_compra.inf_ad_prod = det.infAdProd.valor
            itens_compra.vicms = det.imposto.ICMS.vICMS.valor
            itens_compra.vipi = det.imposto.IPI.vIPI.valor
            itens_compra.p_icms = det.imposto.ICMS.pICMS.valor
            itens_compra.p_ipi = det.imposto.IPI.pIPI.valor
            itens_compra.save()

        nota_entrada.compra = compra
        nota_entrada.save()

    def verificar_configuracao(self):
        try:
            self.conf_nfe = ConfiguracaoNotaFiscal.objects.all()[:1].get()
        except ConfiguracaoNotaFiscal.DoesNotExist:
            return self.salvar_mensagem(message=u'Emissão de NF-e não configurada.', erro=True)

        if not self.conf_nfe.arquivo_certificado_a1:
            return self.salvar_mensagem(message=u'Certificado A1 não encontrado.', erro=True)

        try:
            with open(self.conf_nfe.get_certificado_a1(), 'rb') as f:
                arquivo = f.read()
            self.info_certificado = self.nova_nfe.extrair_certificado_a1(
                arquivo, self.conf_nfe.senha_certificado)
        except:
            return self.salvar_mensagem(message=u'Erro ao tentar ler o certificado, verifique se sua senha está correta.', erro=True)

    def verificar_configuracao_nfe(self, nota_obj):
        try:
            self.conf_nfe = ConfiguracaoNotaFiscal.objects.all()[:1].get()
        except ConfiguracaoNotaFiscal.DoesNotExist:
            e = ErrosValidacaoNotaFiscal(nfe=nota_obj)
            e.tipo = u'0'
            e.descricao = u'Emissão de NF-e não configurada.'
            e.save()
            return self.salvar_mensagem(message=e.descricao, erro=True)

        if not self.conf_nfe.arquivo_certificado_a1:
            e = ErrosValidacaoNotaFiscal(nfe=nota_obj)
            e.tipo = u'0'
            e.descricao = u'Certificado A1 não encontrado.'
            e.save()
            return self.salvar_mensagem(message=e.descricao, erro=True)

        try:
            with open(self.conf_nfe.get_certificado_a1(), 'rb') as f:
                arquivo = f.read()
            self.info_certificado = self.nova_nfe.extrair_certificado_a1(
                arquivo, self.conf_nfe.senha_certificado)
        except:
            e = ErrosValidacaoNotaFiscal(nfe=nota_obj)
            e.tipo = u'0'
            e.descricao = u'Erro ao tentar ler o certificado, verifique se sua senha está correta.'
            e.save()
            return self.salvar_mensagem(message=e.descricao, erro=True)

    def validar_nota(self, nota_obj):
        ErrosValidacaoNotaFiscal.objects.filter(nfe=nota_obj).delete()
        self.nova_nfe = nf_e()

        self.verificar_configuracao_nfe(nota_obj)
        if not self.info_certificado:
            return self.salvar_mensagem(message='Emissão de NF-e não configurada.', erro=True)

        nfe = self.montar_nota(nota_obj)

        if not nota_obj.estado:
            e = ErrosValidacaoNotaFiscal(nfe=nota_obj)
            e.tipo = u'0'
            e.descricao = u'Estado do emitente não foi preenchido.'
            e.save()
            return self.salvar_mensagem(message=e.descricao, erro=True)
        else:
            processo = self.nova_nfe.gerar_xml(xml_nfe=nfe.xml, cert=self.info_certificado['cert'], key=self.info_certificado['key'],
                                               versao=nota_obj.versao, ambiente=int(nota_obj.tp_amb), estado=nota_obj.estado, consumidor=nota_obj.consumidor, caminho=MEDIA_ROOT)
        temp_list = []
        for err in processo.envio.erros:
            e = ErrosValidacaoNotaFiscal(nfe=nota_obj)
            e.tipo = u'0'
            err.replace("\\", "")
            elemento_xml = err.split("'")
            if(elemento_xml[1] not in temp_list):
                temp_list.append(elemento_xml[1])
                e.descricao = "Elemento: " + \
                    elemento_xml[1] + " Não foi preenchido ou está incorreto."
                e.save()

        for alerta in processo.envio.alertas:
            e = ErrosValidacaoNotaFiscal(nfe=nota_obj)
            e.tipo = u'1'
            e.descricao = alerta
            e.save()

        for nf in processo.envio.NFe:
            for err_nf in nf.erros:
                e = ErrosValidacaoNotaFiscal(nfe=nota_obj)
                e.tipo = u'0'
                err_nf.replace("\\", "")
                elemento_xml = err_nf.split("'")
                if (elemento_xml[1] not in temp_list):
                    temp_list.append(elemento_xml[1])
                    e.descricao = "Elemento: " + \
                        elemento_xml[1] + \
                        " Não foi preenchido ou está incorreto."
                    e.save()

            for alerta_nf in nf.alertas:
                e = ErrosValidacaoNotaFiscal(nfe=nota_obj)
                e.tipo = u'1'
                e.descricao = alerta_nf
                e.save()

        if ErrosValidacaoNotaFiscal.objects.filter(nfe=nota_obj).filter(tipo='0').count():
            nota_obj.status_nfe = u'3'
            return self.salvar_mensagem(message='Erros de validação encontrados. Verifique a tab \"Validação\" para mais detalhes.', erro=True)
        else:
            nota_obj.status_nfe = u'6'
            nota_obj.save()
            return self.salvar_mensagem(message='XML Validado', erro=False)

    def emitir_nota(self, nota_obj):
        RespostaSefazNotaFiscal.objects.filter(nfe=nota_obj).delete()
        self.nova_nfe = nf_e()

        self.verificar_configuracao_nfe(nota_obj)
        if not self.info_certificado:
            return self.salvar_mensagem(message='Emissão de NF-e não configurada.', erro=True)

        nfe = self.montar_nota(nota_obj)
        nota_obj.chave = nfe.chave
        nota_obj.save()

        if not nota_obj.estado:
            e = ErrosValidacaoNotaFiscal(nfe=nota_obj)
            e.tipo = u'0'
            e.descricao = u'Estado do emitente não foi preenchido.'
            e.save()
            return self.salvar_mensagem(message=e.descricao, erro=True)
        else:
            try:
                processos = self.nova_nfe.processar_nota(xml_nfe=nfe.xml, cert=self.info_certificado['cert'], key=self.info_certificado['key'],
                                                         versao=nota_obj.versao, ambiente=int(nota_obj.tp_amb), estado=nota_obj.estado, consumidor=nota_obj.consumidor, contingencia=nota_obj.contingencia,
                                                         consultar_servico=False, numero_lote=nota_obj.numero_lote, caminho=MEDIA_ROOT)

                # HTTP 200 - OK
                if processos['lote'].resposta.status in (u'200', 200):
                    # Lote processado
                    if processos['lote'].resposta.cStat.valor in (u'104', 104):
                        if len(processos['notas']):
                            proc = processos['notas'][0]

                            # Autorizada
                            if proc.protNFe.infProt.cStat.valor == u'100':
                                nota_obj.status_nfe = u'1'
                                nota_obj.chave = proc.NFe.chave
                                nota_obj.arquivo_proc = proc.caminho_xml

                                e = RespostaSefazNotaFiscal(nfe=nota_obj)
                                e.tipo = u'1'
                                e.codigo = str(
                                    proc.protNFe.infProt.cStat.valor)
                                e.descricao = str(
                                    proc.protNFe.infProt.xMotivo.valor)
                                e.save()
                                self.salvar_mensagem(
                                    message=e.descricao, erro=False)

                            # Denegada
                            elif proc.protNFe.infProt.cStat.valor in (u'110', u'301', u'302', u'303'):
                                nota_obj.status_nfe = u'2'
                                nota_obj.chave = proc.NFe.chave

                                e = RespostaSefazNotaFiscal(nfe=nota_obj)
                                e.tipo = u'3'
                                e.codigo = str(
                                    proc.protNFe.infProt.cStat.valor)
                                e.descricao = str(
                                    proc.protNFe.infProt.xMotivo.valor)
                                e.save()
                                self.salvar_mensagem(
                                    message=e.descricao, erro=True)

                            # Resultado do processamento (provavelmente nao
                            # ocorre)
                            elif proc.protNFe.infProt.cStat.valor < u'200':
                                nota_obj.chave = proc.NFe.chave

                                e = RespostaSefazNotaFiscal(nfe=nota_obj)
                                e.tipo = u'1'
                                e.codigo = str(
                                    proc.protNFe.infProt.cStat.valor)
                                e.descricao = str(
                                    proc.protNFe.infProt.xMotivo.valor)
                                e.save()
                                self.salvar_mensagem(
                                    message=e.descricao, erro=True)

                            # Rejeicao
                            else:
                                nota_obj.status_nfe = u'5'
                                nota_obj.chave = proc.NFe.chave

                                e = RespostaSefazNotaFiscal(nfe=nota_obj)
                                e.tipo = u'2'
                                e.codigo = str(
                                    proc.protNFe.infProt.cStat.valor)
                                e.descricao = str(
                                    proc.protNFe.infProt.xMotivo.valor)
                                e.save()
                                self.salvar_mensagem(
                                    message=e.descricao, erro=True)

                            nota_obj.numero_protocolo = proc.protNFe.infProt.nProt.valor
                            nota_obj.save()

                    # Lote em processamento
                    elif processos['lote'].resposta.cStat.valor in (u'105', 105):
                        nota_obj.status_nfe = u'4'
                        nota_obj.save()

                        e = RespostaSefazNotaFiscal(nfe=nota_obj)
                        e.tipo = u'4'
                        e.descricao = processos['lote'].resposta.xMotivo.valor
                        e.codigo = str(processos['lote'].resposta.cStat.valor)
                        e.save()
                        self.salvar_mensagem(message=e.descricao, erro=False)
                    elif processos['lote'].resposta.cStat.valor in (u'100', 100):
                        nota_obj.status_nfe = u'1'
                        nota_obj.save()

                        e = RespostaSefazNotaFiscal(nfe=nota_obj)
                        e.tipo = u'1'
                        e.codigo = str(processos['lote'].resposta.cStat.valor)
                        e.descricao = processos['lote'].resposta.xMotivo.valor
                        e.save()
                        self.salvar_mensagem(message=e.descricao, erro=False)
                    else:
                        e = RespostaSefazNotaFiscal(nfe=nota_obj)
                        e.tipo = u'0'
                        e.descricao = 'Erro ao processar lote, motivo: ' + \
                            str(processos['lote'].resposta.xMotivo.valor)
                        e.codigo = str(processos['lote'].resposta.cStat.valor)
                        e.save()
                        self.salvar_mensagem(message=e.descricao, erro=True)

                # HTTP 403 - Acesso proibido
                elif processos['lote'].resposta.status in (u'403', 403):
                    e = RespostaSefazNotaFiscal(nfe=nota_obj)
                    e.tipo = u'0'
                    e.descricao = 'Erro de autenticação, verifique se seu certificado é válido.'
                    e.save()
                    self.salvar_mensagem(message=e.descricao, erro=True)

                else:
                    e = RespostaSefazNotaFiscal(nfe=nota_obj)
                    e.tipo = u'0'
                    e.descricao = 'Erro ao enviar nota, verifique a versão do seu aplicativo e a validade do seu certificado.'
                    e.save()
                    self.salvar_mensagem(message=e.descricao, erro=True)

                nota_obj.numero_lote = processos['numero_lote']
                nota_obj.save()

            except SSLError:
                e = RespostaSefazNotaFiscal(nfe=nota_obj)
                e.tipo = u'0'
                e.descricao = 'Erro de autenticação, verifique se seu certificado é válido.'
                e.save()
                self.salvar_mensagem(message=e.descricao, erro=True)

    def cancelar_nota(self, nota_obj):
        RespostaSefazNotaFiscal.objects.filter(nfe=nota_obj).delete()
        self.nova_nfe = nf_e()

        self.verificar_configuracao_nfe(nota_obj)
        if not self.info_certificado:
            return self.salvar_mensagem(message='Emissão de NF-e não configurada.', erro=True)

        if not nota_obj.estado:
            e = ErrosValidacaoNotaFiscal(nfe=nota_obj)
            e.tipo = u'0'
            e.descricao = u'Estado do emitente não foi preenchido.'
            e.save()
            return self.salvar_mensagem(message=e.descricao, erro=True)
        else:
            try:
                processo = self.nova_nfe.cancelar_nota(chave=nota_obj.chave, protocolo=nota_obj.numero_protocolo, justificativa=nota_obj.just_canc, cert=self.info_certificado['cert'], key=self.info_certificado['key'],
                                                       versao=nota_obj.versao, ambiente=int(nota_obj.tp_amb), estado=nota_obj.estado, contingencia=nota_obj.contingencia, caminho=MEDIA_ROOT)

                # HTTP 200 - OK
                if processo.resposta.status in (u'200', 200):
                    if len(processo.resposta.retEvento):
                        ret = processo.resposta.retEvento[0]

                        # Cancelamento de NF-e homologado / Evento registrado e
                        # vinculado a NF-e
                        if ret.infEvento.cStat.valor == u'101' or ret.infEvento.cStat.valor == u'135':
                            nota_obj.status_nfe = u'8'
                            nota_obj.numero_protocolo = ret.infEvento.nProt.valor
                            nota_obj.save()

                            e = RespostaSefazNotaFiscal(nfe=nota_obj)
                            e.tipo = u'1'
                            e.codigo = str(ret.infEvento.cStat.valor)
                            e.descricao = str(ret.infEvento.xMotivo.valor)
                            e.save()
                            self.salvar_mensagem(
                                message=e.descricao, erro=False)

                        elif ret.infEvento.cStat.valor < u'200':
                            e = RespostaSefazNotaFiscal(nfe=nota_obj)
                            e.tipo = u'1'
                            e.codigo = str(ret.infEvento.cStat.valor)
                            e.descricao = str(ret.infEvento.xMotivo.valor)
                            e.save()
                            self.salvar_mensagem(
                                message=e.descricao, erro=True)

                        else:
                            e = RespostaSefazNotaFiscal(nfe=nota_obj)
                            e.tipo = u'2'
                            e.codigo = str(ret.infEvento.cStat.valor)
                            e.descricao = str(ret.infEvento.xMotivo.valor)
                            e.save()
                            self.salvar_mensagem(
                                message=e.descricao, erro=True)

                # HTTP 403 - Acesso proibido
                elif processo.resposta.status in (u'403', 403):
                    e = RespostaSefazNotaFiscal(nfe=nota_obj)
                    e.tipo = u'0'
                    e.descricao = 'Erro de autenticação, verifique se seu certificado é válido.'
                    e.save()
                    self.salvar_mensagem(message=e.descricao, erro=True)

                else:
                    e = RespostaSefazNotaFiscal(nfe=nota_obj)
                    e.tipo = u'0'
                    e.descricao = 'Erro ao enviar nota, verifique a versão do seu aplicativo e a validade do seu certificado.'
                    e.save()
                    self.salvar_mensagem(message=e.descricao, erro=True)

            except SSLError:
                e = RespostaSefazNotaFiscal(nfe=nota_obj)
                e.tipo = u'0'
                e.descricao = 'Erro de autenticação, verifique se seu certificado é válido.'
                e.save()
                self.salvar_mensagem(message=e.descricao, erro=True)

    def gerar_danfe(self, nota_obj):
        self.nova_nfe = nf_e()

        self.verificar_configuracao_nfe(nota_obj)
        if not self.conf_nfe:
            return self.salvar_mensagem(message='Emissão de NF-e não configurada.', erro=True)

        if not nota_obj.caminho_proc_completo:
            return self.salvar_mensagem(message='Arquivo de processamento da nota não encontrado. Verifique se sua nota foi processada corretamente.', erro=True)

        try:
            # Tentar ler arquivo do processamento da NF-e
            f = open(nota_obj.caminho_proc_completo, encoding='utf8')
            proc_nfe = f.read()
            f.close()
        except FileNotFoundError:
            return self.salvar_mensagem(message='Arquivo de processamento da nota não encontrado. Verifique se sua nota foi processada corretamente.', erro=True)

        logo_path = u''

        if self.conf_nfe.inserir_logo_danfe:
            logo_path = nota_obj.emit_saida.caminho_completo_logo

        danfe = self.nova_nfe.gerar_danfe(
            proc_nfe, nome_sistema=u'PySIGNFe', leiaute_logo_vertical=self.conf_nfe.leiaute_logo_vertical, versao=nota_obj.versao, logo=logo_path)

        return danfe

    def gerar_danfce(self, nota_obj):
        self.nova_nfe = nf_e()

        self.verificar_configuracao_nfe(nota_obj)
        if not self.conf_nfe:
            return self.salvar_mensagem(message='Emissão de NF-e não configurada.', erro=True)

        if not nota_obj.caminho_proc_completo:
            return self.salvar_mensagem(message='Arquivo de processamento da nota não encontrado. Verifique se sua nota foi processada corretamente.', erro=True)

        try:
            # Tentar ler arquivo do processamento da NF-e
            f = open(nota_obj.caminho_proc_completo, encoding='utf8')
            proc_nfe = f.read()
            f.close()
        except FileNotFoundError:
            return self.salvar_mensagem(message='Arquivo de processamento da nota não encontrado. Verifique se sua nota foi processada corretamente.', erro=True)

        if not self.conf_nfe.csc or not self.conf_nfe.cidtoken:
            return self.salvar_mensagem(message='Insira o Código de Segurança do Contribuinte e o Identificador do CSC na área de configuração de NF-e.', erro=True)

        danfce = self.nova_nfe.gerar_danfe(
            proc_nfe, csc=self.conf_nfe.csc, cidtoken=self.conf_nfe.cidtoken, versao=nota_obj.versao)

        return danfce

    def consultar_cadastro(self, empresa, salvar_arquivos):
        self.nova_nfe = nf_e()

        self.verificar_configuracao()
        if not self.conf_nfe or not self.info_certificado:
            return self.salvar_mensagem(message='Emissão de NF-e não configurada.', erro=True)

        if not empresa.uf_padrao:
            return self.salvar_mensagem(message=u'Estado do emitente não foi preenchido.', erro=True)
        elif not empresa.cpf_cnpj_apenas_digitos:
            return self.salvar_mensagem(message=u'CNPJ do emitente não foi preenchido.', erro=True)
        else:
            try:
                processo = self.nova_nfe.consultar_cadastro(cert=self.info_certificado['cert'], key=self.info_certificado['key'], cpf_cnpj=empresa.cpf_cnpj_apenas_digitos, versao=u'4.00',
                                                            ambiente=2, estado=empresa.uf_padrao, contingencia=False, salvar_arquivos=salvar_arquivos, caminho=MEDIA_ROOT)

                self.processo = processo

                if processo.resposta.status in (u'200', 200):
                    if processo.resposta.infCons.cStat.valor and processo.resposta.infCons.cStat.valor < u'200':
                        return self.salvar_mensagem(message=str(processo.resposta.infCons.xMotivo.valor), erro=False)
                    else:
                        return self.salvar_mensagem(message=str(processo.resposta.infCons.xMotivo.valor), erro=True)
                else:
                    return self.salvar_mensagem(message='Erro ao consultar cadastro, verifique a versão do seu aplicativo e a validade do seu certificado.', erro=True)

            except SSLError as e:
                return self.salvar_mensagem(message=u'Erro de autenticação: {}'.format(e), erro=True)

    def inutilizar_notas(self, empresa, ambiente, modelo, serie, numero_inicial, numero_final, justificativa, salvar_arquivos):
        self.nova_nfe = nf_e()

        if modelo == '65':
            nfce = True
        else:
            nfce = False

        self.verificar_configuracao()
        if not self.conf_nfe or not self.info_certificado:
            return self.salvar_mensagem(message='Emissão de NF-e não configurada.', erro=True)

        if not empresa.uf_padrao:
            return self.salvar_mensagem(message=u'Estado do emitente não foi preenchido.', erro=True)
        elif not empresa.cpf_cnpj_apenas_digitos:
            return self.salvar_mensagem(message=u'CNPJ do emitente não foi preenchido.', erro=True)
        else:
            processo = self.nova_nfe.inutilizar_faixa_numeracao(cnpj=empresa.cpf_cnpj_apenas_digitos, serie=serie, numero_inicial=numero_inicial, numero_final=numero_final, justificativa=justificativa,
                                                                cert=self.info_certificado['cert'], key=self.info_certificado['key'], versao=u'4.00', ambiente=int(ambiente), estado=empresa.uf_padrao, nfce=nfce, contingencia=False, caminho=MEDIA_ROOT)

            self.processo = processo

            if processo.resposta.status in (u'200', 200):
                if processo.resposta.infInut.cStat.valor and processo.resposta.infInut.cStat.valor < u'200':
                    return self.salvar_mensagem(message=str(processo.resposta.infInut.xMotivo.valor), erro=False)
                else:
                    return self.salvar_mensagem(message=str(processo.resposta.infInut.xMotivo.valor), erro=True)
            else:
                return self.salvar_mensagem(message='Erro ao inutilizar notas, verifique a versão do seu aplicativo e a validade do seu certificado.', erro=True)

    def consultar_nota(self, chave, ambiente, salvar_arquivos):
        self.nova_nfe = nf_e()

        self.verificar_configuracao()
        if not self.conf_nfe or not self.info_certificado:
            return self.salvar_mensagem(message='Emissão de NF-e não configurada.', erro=True)

        try:
            uf = dict(COD_UF)[chave[:2]]
        except KeyError:
            return self.salvar_mensagem(message=u'Chave com código da UF incorreto.', erro=True)

        processo = self.nova_nfe.consultar_nfe(chave=chave, cert=self.info_certificado['cert'], key=self.info_certificado['key'], versao=u'4.00', ambiente=int(
            ambiente), estado=uf, contingencia=False, caminho=MEDIA_ROOT)

        self.processo = processo

        if processo.resposta.status in (u'200', 200):
            if processo.resposta.cStat.valor and processo.resposta.cStat.valor < u'200':
                return self.salvar_mensagem(message=str(processo.resposta.xMotivo.valor), erro=False)
            else:
                return self.salvar_mensagem(message=str(processo.resposta.xMotivo.valor), erro=True)
        else:
            return self.salvar_mensagem(message='Erro ao consultar nota, verifique a versão do seu aplicativo e a validade do seu certificado.', erro=True)

    def baixar_nota(self, chave, ambiente, ambiente_nacional, salvar_arquivos):
        self.nova_nfe = nf_e()

        self.verificar_configuracao()
        if not self.conf_nfe or not self.info_certificado:
            return self.salvar_mensagem(message='Emissão de NF-e não configurada.', erro=True)

        try:
            uf = dict(COD_UF)[chave[:2]]
        except KeyError:
            return self.salvar_mensagem(message=u'Chave com código da UF incorreto.', erro=True)

        cnpj = chave[6:20]

        processo = self.nova_nfe.download_notas(cnpj=cnpj, lista_chaves=[chave, ], ambiente_nacional=ambiente_nacional, cert=self.info_certificado['cert'], key=self.info_certificado['key'],
                                                versao=u'4.00', ambiente=int(ambiente), estado=uf, contingencia=False, caminho=MEDIA_ROOT)

        self.processo = processo

        if processo.resposta.status in (u'200', 200):
            if processo.resposta.cStat.valor and processo.resposta.cStat.valor < u'200':
                return self.salvar_mensagem(message=str(processo.resposta.xMotivo.valor), erro=False)
            else:
                return self.salvar_mensagem(message=str(processo.resposta.xMotivo.valor), erro=True)
        else:
            return self.salvar_mensagem(message='Erro ao baixar nota, verifique a versão do seu aplicativo e a validade do seu certificado.', erro=True)

    def efetuar_manifesto(self, chave, cnpj, ambiente, tipo_manifesto, justificativa, ambiente_nacional, salvar_arquivos):
        self.nova_nfe = nf_e()

        self.verificar_configuracao()
        if not self.conf_nfe or not self.info_certificado:
            return self.salvar_mensagem(message='Emissão de NF-e não configurada.', erro=True)

        try:
            uf = dict(COD_UF)[chave[:2]]
        except KeyError:
            return self.salvar_mensagem(message=u'Chave com código da UF incorreto.', erro=True)

        processo = self.nova_nfe.efetuar_manifesto(cnpj=cnpj, tipo_manifesto=tipo_manifesto, chave=chave, ambiente_nacional=ambiente_nacional, cert=self.info_certificado['cert'], key=self.info_certificado['key'], versao=u'4.00',
                                                   ambiente=int(ambiente), estado=uf, contingencia=False, caminho=MEDIA_ROOT)

        self.processo = processo

        if processo.resposta.status in (u'200', 200):
            if processo.resposta.cStat.valor and processo.resposta.cStat.valor < u'200':
                return self.salvar_mensagem(message=str(processo.resposta.xMotivo.valor), erro=False)
            else:
                return self.salvar_mensagem(message=str(processo.resposta.xMotivo.valor), erro=True)
        else:
            return self.salvar_mensagem(message='Erro ao efetuar manifesto, verifique a versão do seu aplicativo e a validade do seu certificado.', erro=True)
