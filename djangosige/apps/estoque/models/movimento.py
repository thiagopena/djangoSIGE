# -*- coding: utf-8 -*-

import operator
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.urls import reverse_lazy
from django.template.defaultfilters import date

from . import DEFAULT_LOCAL_ID

import locale
locale.setlocale(locale.LC_ALL, '')

TIPOS_MOVIMENTO_ENTRADA = (
    (u'0', u'Ajuste'),
    (u'1', u'Entrada por pedido de compra'),
    (u'2', u'Entrada por importação de nota fiscal de fornecedor'),
    (u'3', u'Ajuste inicial'),
)

TIPOS_MOVIMENTO_SAIDA = (
    (u'0', u'Ajuste'),
    (u'1', u'Saída por pedido de venda'),
    (u'2', u'Saída por importação de nota fiscal'),
)


class ItensMovimento(models.Model):
    produto = models.ForeignKey('cadastro.Produto', related_name="moviment_estoque_produto",
                                on_delete=models.CASCADE, null=True, blank=True)
    movimento_id = models.ForeignKey(
        'estoque.MovimentoEstoque', related_name="itens_movimento", on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                     MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    valor_unit = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                     MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    subtotal = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                   MinValueValidator(Decimal('0.00'))], null=True, blank=True)

    def get_estoque_atual_produto(self):
        if self.produto:
            if self.produto.controlar_estoque and self.produto.estoque_atual:
                return self.produto.estoque_atual
            else:
                return 'Não controlado'

    def format_estoque_atual_produto(self):
        estoque_atual = self.get_estoque_atual_produto()
        if isinstance(estoque_atual, Decimal):
            return locale.format(u'%.2f', estoque_atual, 1)
        else:
            return estoque_atual


class MovimentoEstoque(models.Model):
    data_movimento = models.DateField(null=True, blank=True)
    quantidade_itens = models.IntegerField(
        validators=[MinValueValidator(0)], default=0)
    valor_total = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                      MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    observacoes = models.CharField(max_length=1055, null=True, blank=True)

    class Meta:
        verbose_name = "Movimento de Estoque"
        permissions = (
            ("consultar_estoque", "Pode consultar estoque"),
        )

    @property
    def format_data_movimento(self):
        return '%s' % date(self.data_movimento, "d/m/Y")

    def format_quantidade_itens(self):
        return locale.format(u'%.2f', self.quantidade_itens, 1)

    def format_valor_total(self):
        return locale.format(u'%.2f', self.valor_total, 1)


@receiver(
    pre_delete,
    sender=MovimentoEstoque,
    dispatch_uid="movimento_estoque_delete"
)
def reajusta_estoque_produtos(sender, instance, using, **kwargs):
    if hasattr(instance, "entradaestoque"):
        operation = operator.sub
    elif hasattr(instance, "saidaestoque"):
        operation = operator.add
    else:
        return
    for item in instance.itens_movimento.all():
        produto = item.produto
        produto.estoque_atual = operation(produto.estoque_atual, item.quantidade)
        produto.save()
        for produto_estocado in produto.produto_estocado.all():
            produto_estocado.quantidade = operation(produto_estocado.quantidade, item.quantidade)
            produto_estocado.save()


class EntradaEstoque(MovimentoEstoque):
    tipo_movimento = models.CharField(
        max_length=1, choices=TIPOS_MOVIMENTO_ENTRADA, default='0')
    pedido_compra = models.ForeignKey(
        'compras.PedidoCompra', related_name="entrada_estoque_pedido", on_delete=models.SET_NULL, null=True, blank=True)
    fornecedor = models.ForeignKey(
        'cadastro.Fornecedor', related_name="entrada_estoque_fornecedor", on_delete=models.SET_NULL, null=True, blank=True)
    local_dest = models.ForeignKey(
        'estoque.LocalEstoque', related_name="entrada_estoque_local", default=DEFAULT_LOCAL_ID, on_delete=models.PROTECT)

    def get_edit_url(self):
        return reverse_lazy('djangosige.apps.estoque:detalharentradaestoqueview', kwargs={'pk': self.id})

    def get_tipo(self):
        return 'Entrada'


class SaidaEstoque(MovimentoEstoque):
    tipo_movimento = models.CharField(
        max_length=1, choices=TIPOS_MOVIMENTO_SAIDA, default='0')
    pedido_venda = models.ForeignKey(
        'vendas.PedidoVenda', related_name="saida_estoque", on_delete=models.SET_NULL, null=True, blank=True)
    local_orig = models.ForeignKey(
        'estoque.LocalEstoque', related_name="saida_estoque_local", default=DEFAULT_LOCAL_ID, on_delete=models.PROTECT)

    def get_edit_url(self):
        return reverse_lazy('djangosige.apps.estoque:detalharsaidaestoqueview', kwargs={'pk': self.id})

    def get_tipo(self):
        return 'Saída'


class TransferenciaEstoque(MovimentoEstoque):
    local_estoque_orig = models.ForeignKey(
        'estoque.LocalEstoque', related_name="transf_estoque_orig", on_delete=models.CASCADE)
    local_estoque_dest = models.ForeignKey(
        'estoque.LocalEstoque', related_name="transf_estoque_dest", on_delete=models.CASCADE)

    def get_edit_url(self):
        return reverse_lazy('djangosige.apps.estoque:detalhartransferenciaestoqueview', kwargs={'pk': self.id})

    def get_tipo(self):
        return 'Transferência'
