# -*- coding: utf-8 -*-

import locale
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

locale.setlocale(locale.LC_ALL, "")


FORMAS_PAG_ESCOLHAS = (
    ("01", "Dinheiro"),
    ("02", "Cheque"),
    ("03", "Cartão de Crédito"),
    ("04", "Cartão de Débito"),
    ("05", "Crédito Loja"),
    ("10", "Vale Alimentação"),
    ("11", "Vale Refeição"),
    ("12", "Vale Presente"),
    ("13", "Vale Combustível"),
    ("99", "Outros"),
)


class Pagamento(models.Model):
    venda_id = models.ForeignKey(
        "vendas.Venda", related_name="parcela_pagamento", on_delete=models.CASCADE
    )
    indice_parcela = models.IntegerField()
    vencimento = models.DateField()
    valor_parcela = models.DecimalField(
        max_digits=13, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    @property
    def format_valor_parcela(self):
        return locale.format("%.2f", self.valor_parcela, 1)

    @property
    def format_vencimento(self):
        return self.vencimento.strftime("%d/%m/%Y")


class CondicaoPagamento(models.Model):
    descricao = models.CharField(max_length=255)
    forma = models.CharField(max_length=2, choices=FORMAS_PAG_ESCOLHAS, default="99")
    n_parcelas = models.IntegerField()
    dias_recorrencia = models.IntegerField(default=0)
    parcela_inicial = models.IntegerField(default=0)  # Dias

    class Meta:
        verbose_name = "Condição de Pagamento"

    def __unicode__(self):
        s = "%s" % (self.descricao)
        return s

    def __str__(self):
        s = "%s" % (self.descricao)
        return s
