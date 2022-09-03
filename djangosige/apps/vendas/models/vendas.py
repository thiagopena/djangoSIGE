# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import date
from django.core.validators import MinValueValidator
from django.urls import reverse_lazy

from decimal import Decimal

from djangosige.apps.fiscal.models import PIS, COFINS
from djangosige.apps.estoque.models import DEFAULT_LOCAL_ID

import locale
locale.setlocale(locale.LC_ALL, '')

STATUS_ORCAMENTO_ESCOLHAS = (
    (u'0', u'Aberto'),
    (u'1', u'Baixado'),
    (u'2', u'Cancelado'),
)

STATUS_PEDIDO_VENDA_ESCOLHAS = (
    (u'0', u'Aberto'),
    (u'1', u'Faturado'),
    (u'2', u'Cancelado'),
    (u'3', u'Importado por XML'),
)

TIPOS_DESCONTO_ESCOLHAS = (
    (u'0', u'Valor'),
    (u'1', u'Percentual'),
)

MOD_FRETE_ESCOLHAS = (
    (u'0', u'Por conta do emitente'),
    (u'1', u'Por conta do destinatário/remetente'),
    (u'2', u'Por conta de terceiros'),
    (u'9', u'Sem frete'),
)


class ItensVenda(models.Model):
    produto = models.ForeignKey('cadastro.Produto', related_name="venda_produto",
                                on_delete=models.CASCADE, null=True, blank=True)
    venda_id = models.ForeignKey(
        'vendas.Venda', related_name="itens_venda", on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                     MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    valor_unit = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                     MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    tipo_desconto = models.CharField(
        max_length=1, choices=TIPOS_DESCONTO_ESCOLHAS, null=True, blank=True)
    desconto = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                   MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    subtotal = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                   MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    inf_ad_prod = models.CharField(max_length=500, null=True, blank=True)

    # Rateio
    valor_rateio_frete = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                             MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    valor_rateio_despesas = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                                MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    valor_rateio_seguro = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                              MinValueValidator(Decimal('0.00'))], null=True, blank=True)

    # Bases de calculo
    vbc_icms = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                   MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vbc_icms_st = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                      MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vbc_ipi = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                  MinValueValidator(Decimal('0.00'))], null=True, blank=True)

    # Valores e aliquotas
    vicms = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vicms_st = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                   MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vipi = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vfcp = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vicmsufdest = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                      MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vicmsufremet = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                       MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vicms_deson = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                      MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    p_icms = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                 MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    p_icmsst = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                   MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    p_ipi = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))], null=True, blank=True)

    # Valores do PIS e COFINS
    vq_bcpis = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                   MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vq_bccofins = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                      MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vpis = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vcofins = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                  MinValueValidator(Decimal('0.00'))], null=True, blank=True)

    # Opcoes
    icms_incluido_preco = models.BooleanField(default=False)
    icmsst_incluido_preco = models.BooleanField(default=False)
    ipi_incluido_preco = models.BooleanField(default=False)
    incluir_bc_icms = models.BooleanField(
        default=False)  # incluir IPI na BC do ICMS
    incluir_bc_icmsst = models.BooleanField(
        default=False)  # incluir IPI na BC do ICMS-ST
    auto_calcular_impostos = models.BooleanField(default=True)

    @property
    def vprod(self):
        return round(self.quantidade * self.valor_unit, 2)

    @property
    def vbc_uf_dest(self):
        return self.subtotal + self.vipi

    @property
    def vicms_cred_sn(self):
        try:
            icms_obj = self.produto.grupo_fiscal.icms_sn_padrao.get()
            if icms_obj.p_cred_sn:
                return round((self.subtotal * icms_obj.p_cred_sn) / 100, 2)
            else:
                return ''
        except:
            return ''

    def get_valor_desconto(self, decimais=2):
        if self.tipo_desconto == '0':
            return round(self.desconto, decimais)
        else:
            tot_sem_desc = self.get_total_sem_desconto()
            v_desconto = tot_sem_desc * (self.desconto / 100)
            return round(v_desconto, decimais)

    def format_desconto(self):
        return '{0}'.format(locale.format(u'%.2f', self.get_valor_desconto(), 1))

    def format_quantidade(self):
        return locale.format(u'%.2f', self.quantidade, 1)

    def format_valor_unit(self):
        return locale.format(u'%.2f', self.valor_unit, 1)

    def format_total(self):
        return locale.format(u'%.2f', self.subtotal, 1)

    def format_vprod(self):
        return locale.format(u'%.2f', self.vprod, 1)

    def get_total_sem_desconto(self):
        if self.tipo_desconto == '0':
            return self.subtotal + self.desconto
        else:
            tot_sem_desc = (self.subtotal * 100) / (100 - self.desconto)
            return tot_sem_desc

    def get_mot_deson_icms(self):
        try:
            icms_obj = self.produto.grupo_fiscal.icms_padrao.get()
            if icms_obj.mot_des_icms:
                return icms_obj.get_mot_des_icms_display()
            else:
                return ''
        except:
            return ''

    def get_total_impostos(self):
        return sum(filter(None, [self.vicms, self.vicms_st, self.vipi, self.vfcp, self.vicmsufdest, self.vicmsufremet]))

    def format_total_impostos(self):
        return locale.format(u'%.2f', self.get_total_impostos(), 1)

    def get_total_com_impostos(self):
        total_com_impostos = self.subtotal + self.get_total_impostos()
        return total_com_impostos

    def format_total_com_imposto(self):
        return locale.format(u'%.2f', self.get_total_com_impostos(), 1)

    def format_valor_attr(self, nome_attr):
        valor = getattr(self, nome_attr)
        if valor is not None:
            return locale.format(u'%.2f', valor, 1)

    def get_aliquota_pis(self, format=True):
        try:
            pis_padrao = PIS.objects.get(
                grupo_fiscal=self.produto.grupo_fiscal)

            if pis_padrao.valiq_pis:
                if format:
                    return locale.format(u'%.2f', pis_padrao.valiq_pis, 1)
                else:
                    return pis_padrao.valiq_pis
            elif pis_padrao.p_pis:
                if format:
                    return locale.format(u'%.2f', pis_padrao.p_pis, 1)
                else:
                    return pis_padrao.p_pis

        except PIS.DoesNotExist:
            return

    def get_aliquota_cofins(self, format=True):
        try:
            cofins_padrao = COFINS.objects.get(
                grupo_fiscal=self.produto.grupo_fiscal)

            if cofins_padrao.valiq_cofins:
                if format:
                    return locale.format(u'%.2f', cofins_padrao.valiq_cofins, 1)
                else:
                    return cofins_padrao.valiq_cofins
            elif cofins_padrao.p_cofins:
                if format:
                    return locale.format(u'%.2f', cofins_padrao.p_cofins, 1)
                else:
                    return cofins_padrao.p_cofins

        except COFINS.DoesNotExist:
            return

    def calcular_pis_cofins(self):
        vbc = self.subtotal
        if self.valor_rateio_despesas:
            vbc += self.valor_rateio_despesas
        if self.desconto:
            vbc -= self.desconto

        if self.produto.grupo_fiscal:

            try:
                pis_padrao = PIS.objects.get(
                    grupo_fiscal=self.produto.grupo_fiscal)
                cofins_padrao = COFINS.objects.get(
                    grupo_fiscal=self.produto.grupo_fiscal)

                # Calculo Vl. PIS
                if pis_padrao.valiq_pis:
                    self.vq_bcpis = self.quantidade
                    self.vpis = self.quantidade * pis_padrao.valiq_pis
                elif pis_padrao.p_pis:
                    self.vq_bcpis = vbc
                    self.vpis = vbc * (pis_padrao.p_pis / 100)

                # Calculo Vl. COFINS
                if cofins_padrao.valiq_cofins:
                    self.vq_bccofins = self.quantidade
                    self.vcofins = self.quantidade * cofins_padrao.valiq_cofins
                elif cofins_padrao.p_cofins:
                    self.vq_bccofins = vbc
                    self.vcofins = vbc * (cofins_padrao.p_cofins / 100)

            except (PIS.DoesNotExist, COFINS.DoesNotExist):
                pass


class Venda(models.Model):
    # Cliente
    cliente = models.ForeignKey(
        'cadastro.Cliente', related_name="venda_cliente", on_delete=models.CASCADE)
    ind_final = models.BooleanField(default=False)
    # Transporte
    transportadora = models.ForeignKey(
        'cadastro.Transportadora', related_name="venda_transportadora", on_delete=models.CASCADE, null=True, blank=True)
    veiculo = models.ForeignKey('cadastro.Veiculo', related_name="venda_veiculo",
                                on_delete=models.SET_NULL, null=True, blank=True)
    mod_frete = models.CharField(
        max_length=1, choices=MOD_FRETE_ESCOLHAS, default='9')
    # Estoque
    local_orig = models.ForeignKey(
        'estoque.LocalEstoque', related_name="venda_local_estoque", default=DEFAULT_LOCAL_ID, on_delete=models.PROTECT)
    movimentar_estoque = models.BooleanField(default=True)
    # Info
    data_emissao = models.DateField(null=True, blank=True)
    vendedor = models.CharField(max_length=255, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                      MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    tipo_desconto = models.CharField(
        max_length=1, choices=TIPOS_DESCONTO_ESCOLHAS, default='0')
    desconto = models.DecimalField(max_digits=15, decimal_places=4, validators=[
                                   MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    despesas = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                   MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    frete = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    seguro = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                 MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    impostos = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                   MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    cond_pagamento = models.ForeignKey(
        'vendas.CondicaoPagamento', related_name="venda_pagamento", on_delete=models.SET_NULL, null=True, blank=True)
    observacoes = models.CharField(max_length=1055, null=True, blank=True)

    def get_total_sem_imposto(self):
        total_sem_imposto = self.valor_total - self.impostos
        return total_sem_imposto

    def get_total_produtos(self):
        itens = ItensVenda.objects.filter(venda_id=self.id)
        tot = 0
        for it in itens:
            tot += it.vprod
        return tot

    def get_total_produtos_estoque(self):
        itens = self.itens_venda.all()
        tot = 0
        for it in itens:
            if it.produto.controlar_estoque:
                tot += it.vprod
        return tot

    def format_total_produtos(self):
        return locale.format(u'%.2f', self.get_total_produtos(), 1)

    @property
    def format_data_emissao(self):
        return '%s' % date(self.data_emissao, "d/m/Y")

    def get_valor_desconto_total(self, decimais=2):
        if self.tipo_desconto == '0':
            return round(self.desconto, decimais)
        else:
            tot_sem_desc = self.get_total_sem_desconto()
            v_desconto = tot_sem_desc * (self.desconto / 100)
            return round(v_desconto, decimais)

    def format_valor_total(self):
        return locale.format(u'%.2f', self.valor_total, 1)

    def format_frete(self):
        return locale.format(u'%.2f', self.frete, 1)

    def format_impostos(self):
        return locale.format(u'%.2f', self.impostos, 1)

    def format_total_sem_imposto(self):
        return locale.format(u'%.2f', self.get_total_sem_imposto(), 1)

    def format_desconto(self):
        if self.tipo_desconto == '0':
            return locale.format(u'%.2f', self.desconto, 1)
        else:
            itens = ItensVenda.objects.filter(venda_id=self.id)
            tot = 0
            for it in itens:
                tot += it.get_total_sem_desconto()

            v_desconto = tot * (self.desconto / 100)
            return locale.format(u'%.2f', v_desconto, 1)

    def format_seguro(self):
        return locale.format(u'%.2f', self.seguro, 1)

    def format_despesas(self):
        return locale.format(u'%.2f', self.despesas, 1)

    def format_total_sem_desconto(self):
        total_sem_desconto = self.valor_total - self.desconto
        return locale.format(u'%.2f', total_sem_desconto, 1)

    def get_forma_pagamento(self):
        if self.cond_pagamento:
            return self.cond_pagamento.get_forma_display()
        else:
            return ""

    def get_local_orig_id(self):
        if self.local_orig:
            return self.local_orig.id
        else:
            return ""

    def get_valor_total_attr(self, nome_attr):
        valor_total = 0
        for item in self.itens_venda.all():
            v = getattr(item, nome_attr, 0)
            if v:
                valor_total += v

        return valor_total

    def get_child(self):
        try:
            return PedidoVenda.objects.get(id=self.id)
        except PedidoVenda.DoesNotExist:
            return OrcamentoVenda.objects.get(id=self.id)

    def __unicode__(self):
        s = u'Venda nº %s' % (self.id)
        return s

    def __str__(self):
        s = u'Venda nº %s' % (self.id)
        return s


class OrcamentoVenda(Venda):
    data_vencimento = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=STATUS_ORCAMENTO_ESCOLHAS, default='0')

    class Meta:
        verbose_name = "Orçamento de Venda"

    @property
    def format_data_vencimento(self):
        return '%s' % date(self.data_vencimento, "d/m/Y")

    @property
    def tipo_venda(self):
        return 'Orçamento'

    def edit_url(self):
        return reverse_lazy('djangosige.apps.vendas:editarorcamentovendaview', kwargs={'pk': self.id})

    def __unicode__(self):
        s = u'Orçamento de venda nº %s' % (self.id)
        return s

    def __str__(self):
        s = u'Orçamento de venda nº %s' % (self.id)
        return s


class PedidoVenda(Venda):
    orcamento = models.ForeignKey(
        'vendas.OrcamentoVenda', related_name="orcamento_pedido", on_delete=models.SET_NULL, null=True, blank=True)
    data_entrega = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=STATUS_PEDIDO_VENDA_ESCOLHAS, default='0')

    class Meta:
        verbose_name = "Pedido de Venda"
        permissions = (
            ("faturar_pedidovenda", "Pode faturar Pedidos de Venda"),
        )

    @property
    def format_data_entrega(self):
        return '%s' % date(self.data_entrega, "d/m/Y")

    @property
    def tipo_venda(self):
        return 'Pedido'

    def edit_url(self):
        return reverse_lazy('djangosige.apps.vendas:editarpedidovendaview', kwargs={'pk': self.id})

    def __unicode__(self):
        s = u'Pedido de venda nº %s (%s)' % (
            self.id, self.get_status_display())
        return s

    def __str__(self):
        s = u'Pedido de venda nº %s (%s)' % (
            self.id, self.get_status_display())
        return s
