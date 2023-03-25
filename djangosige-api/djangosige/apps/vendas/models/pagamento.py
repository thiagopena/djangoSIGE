# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

import locale
locale.setlocale(locale.LC_ALL, '')


FORMAS_PAG_ESCOLHAS = (
    (u'01', u'Dinheiro'),
    (u'02', u'Cheque'),
    (u'03', u'Cartão de Crédito'),
    (u'04', u'Cartão de Débito'),
    (u'05', u'Crédito Loja'),
    (u'10', u'Vale Alimentação'),
    (u'11', u'Vale Refeição'),
    (u'12', u'Vale Presente'),
    (u'13', u'Vale Combustível'),
    (u'99', u'Outros'),
)


class Pagamento(models.Model):
    venda_id = models.ForeignKey(
        'vendas.Venda', related_name="parcela_pagamento", on_delete=models.CASCADE)
    indice_parcela = models.IntegerField()
    vencimento = models.DateField()
    valor_parcela = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                        MinValueValidator(Decimal('0.00'))])

    @property
    def format_valor_parcela(self):
        return locale.format(u'%.2f', self.valor_parcela, 1)

    @property
    def format_vencimento(self):
        return self.vencimento.strftime('%d/%m/%Y')


class CondicaoPagamento(models.Model):
    descricao = models.CharField(max_length=255)
    forma = models.CharField(
        max_length=2, choices=FORMAS_PAG_ESCOLHAS, default='99')
    n_parcelas = models.IntegerField()
    dias_recorrencia = models.IntegerField(default=0)
    parcela_inicial = models.IntegerField(default=0)  # Dias

    class Meta:
        verbose_name = "Condição de Pagamento"

    def __unicode__(self):
        s = u'%s' % (self.descricao)
        return s

    def __str__(self):
        s = u'%s' % (self.descricao)
        return s
