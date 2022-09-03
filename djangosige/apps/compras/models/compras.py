# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import date
from django.core.validators import MinValueValidator
from django.urls import reverse_lazy

from decimal import Decimal

from djangosige.apps.vendas.models import TIPOS_DESCONTO_ESCOLHAS, MOD_FRETE_ESCOLHAS, STATUS_ORCAMENTO_ESCOLHAS
from djangosige.apps.estoque.models import DEFAULT_LOCAL_ID

import locale
locale.setlocale(locale.LC_ALL, '')

STATUS_PEDIDO_COMPRA_ESCOLHAS = (
    (u'0', u'Aberto'),
    (u'1', u'Realizado'),
    (u'2', u'Cancelado'),
    (u'3', u'Importado por XML'),
    (u'4', u'Recebido')
)


class ItensCompra(models.Model):
    produto = models.ForeignKey('cadastro.Produto', related_name="compra_produto",
                                on_delete=models.CASCADE, null=True, blank=True)
    compra_id = models.ForeignKey(
        'compras.Compra', related_name="itens_compra", on_delete=models.CASCADE)
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

    vicms = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    vipi = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    p_icms = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                 MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    p_ipi = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))], null=True, blank=True)

    # Opcoes
    icms_incluido_preco = models.BooleanField(default=False)
    ipi_incluido_preco = models.BooleanField(default=False)
    incluir_bc_icms = models.BooleanField(
        default=False)  # incluir IPI na BC do ICMS
    auto_calcular_impostos = models.BooleanField(default=True)

    @property
    def vprod(self):
        return round(self.quantidade * self.valor_unit, 2)

    def get_total_sem_desconto(self):
        if self.tipo_desconto == '0':
            return self.subtotal + self.desconto
        else:
            tot_sem_desc = (self.subtotal * 100) / (100 - self.desconto)
            return tot_sem_desc

    def get_valor_desconto(self):
        if self.tipo_desconto == '0':
            return self.desconto
        else:
            tot_sem_desc = self.get_total_sem_desconto()
            v_desconto = tot_sem_desc * (self.desconto / 100)
            return v_desconto

    def get_total_impostos(self):
        return sum(filter(None, [self.vicms, self.vipi]))

    def get_total_com_impostos(self):
        total_com_impostos = self.subtotal + self.get_total_impostos()
        return total_com_impostos

    def format_total_impostos(self):
        return locale.format(u'%.2f', self.get_total_impostos(), 1)

    def format_total_com_imposto(self):
        return locale.format(u'%.2f', self.get_total_com_impostos(), 1)

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

    def format_valor_attr(self, nome_attr):
        valor = getattr(self, nome_attr)
        if valor is not None:
            return locale.format(u'%.2f', valor, 1)


class Compra(models.Model):
    # Fornecedor
    fornecedor = models.ForeignKey(
        'cadastro.Fornecedor', related_name="compra_fornecedor", on_delete=models.CASCADE)
    # Transporte
    mod_frete = models.CharField(
        max_length=1, choices=MOD_FRETE_ESCOLHAS, default='9')
    # Estoque
    local_dest = models.ForeignKey(
        'estoque.LocalEstoque', related_name="compra_local_estoque", default=DEFAULT_LOCAL_ID, on_delete=models.PROTECT)
    movimentar_estoque = models.BooleanField(default=True)
    # Info
    data_emissao = models.DateField(null=True, blank=True)
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
    total_icms = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                     MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    total_ipi = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                    MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    cond_pagamento = models.ForeignKey(
        'vendas.CondicaoPagamento', related_name="compra_pagamento", on_delete=models.SET_NULL, null=True, blank=True)
    observacoes = models.CharField(max_length=1055, null=True, blank=True)

    def get_total_sem_imposto(self):
        total_sem_imposto = self.valor_total - self.impostos
        return total_sem_imposto

    def get_total_produtos(self):
        itens = ItensCompra.objects.filter(compra_id=self.id)
        tot = 0
        for it in itens:
            tot += it.vprod
        return tot

    def get_total_produtos_estoque(self):
        itens = self.itens_compra.all()
        tot = 0
        for it in itens:
            if it.produto.controlar_estoque:
                tot += it.vprod
        return tot

    def format_total_produtos(self):
        return locale.format(u'%.2f', self.get_total_produtos(), 1)

    @property
    def impostos(self):
        return (self.total_icms + self.total_ipi)

    @property
    def format_data_emissao(self):
        return '%s' % date(self.data_emissao, "d/m/Y")

    def format_valor_total(self):
        return locale.format(u'%.2f', self.valor_total, 1)

    def format_frete(self):
        return locale.format(u'%.2f', self.frete, 1)

    def format_impostos(self):
        return locale.format(u'%.2f', self.impostos, 1)

    def format_vicms(self):
        return locale.format(u'%.2f', self.total_icms, 1)

    def format_vipi(self):
        return locale.format(u'%.2f', self.total_ipi, 1)

    def format_total_sem_imposto(self):
        return locale.format(u'%.2f', self.get_total_sem_imposto(), 1)

    def format_desconto(self):
        if self.tipo_desconto == '0':
            return locale.format(u'%.2f', self.desconto, 1)
        else:
            itens = ItensCompra.objects.filter(compra_id=self.id)
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

    def get_local_dest_id(self):
        if self.local_dest:
            return self.local_dest.id
        else:
            return ""

    def get_child(self):
        try:
            return PedidoCompra.objects.get(id=self.id)
        except PedidoCompra.DoesNotExist:
            return OrcamentoCompra.objects.get(id=self.id)

    def __unicode__(self):
        s = u'Compra nº %s' % (self.id)
        return s

    def __str__(self):
        s = u'Compra nº %s' % (self.id)
        return s


class OrcamentoCompra(Compra):
    data_vencimento = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=STATUS_ORCAMENTO_ESCOLHAS, default='0')

    class Meta:
        verbose_name = "Orçamento de Compra"

    @property
    def format_data_vencimento(self):
        return '%s' % date(self.data_vencimento, "d/m/Y")

    @property
    def tipo_compra(self):
        return 'Orçamento'

    def edit_url(self):
        return reverse_lazy('djangosige.apps.compras:editarorcamentocompraview', kwargs={'pk': self.id})

    def __unicode__(self):
        s = u'Orçamento nº %s' % (self.id)
        return s

    def __str__(self):
        s = u'Orçamento nº %s' % (self.id)
        return s


class PedidoCompra(Compra):
    orcamento = models.ForeignKey(
        'compras.OrcamentoCompra', related_name="orcamento_pedido", on_delete=models.SET_NULL, null=True, blank=True)
    data_entrega = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=STATUS_PEDIDO_COMPRA_ESCOLHAS, default='0')

    class Meta:
        verbose_name = "Pedido de Compra"
        permissions = (
            ("faturar_pedidocompra", "Pode faturar Pedidos de Compra"),
        )

    @property
    def format_data_entrega(self):
        return '%s' % date(self.data_entrega, "d/m/Y")

    @property
    def tipo_compra(self):
        return 'Pedido'

    def edit_url(self):
        return reverse_lazy('djangosige.apps.compras:editarpedidocompraview', kwargs={'pk': self.id})

    def __unicode__(self):
        s = u'Pedido de compra nº %s (%s)' % (
            self.id, self.get_status_display())
        return s

    def __str__(self):
        s = u'Pedido de compra nº %s (%s)' % (
            self.id, self.get_status_display())
        return s
