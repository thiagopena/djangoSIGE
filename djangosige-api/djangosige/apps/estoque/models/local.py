# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from djangosige.apps.cadastro.models import Produto

DEFAULT_LOCAL_ID = 1


class ProdutoEstocado(models.Model):
    local = models.ForeignKey('estoque.LocalEstoque', related_name="local_produto_estocado",
                              on_delete=models.CASCADE, null=True, blank=True)
    produto = models.ForeignKey('cadastro.Produto', related_name="produto_estocado",
                                on_delete=models.CASCADE, null=True, blank=True)
    quantidade = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                     MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))


class LocalEstoque(models.Model):
    descricao = models.CharField(max_length=1055)
    produtos_estoque = models.ManyToManyField(
        Produto, through='estoque.ProdutoEstocado')

    class Meta:
        verbose_name = "Local de Estoque"

    def __unicode__(self):
        s = u'%s' % (self.descricao)
        return s

    def __str__(self):
        s = u'%s' % (self.descricao)
        return s
