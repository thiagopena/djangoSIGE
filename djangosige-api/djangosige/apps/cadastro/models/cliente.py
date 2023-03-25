# -*- coding: utf-8 -*-

from django.db import models

from decimal import Decimal

from .base import Pessoa

INDICADOR_IE_DEST = [
    ('1', 'Contribuinte ICMS'),
    ('2', 'Contribuinte isento de Inscrição'),
    ('9', 'Não Contribuinte'),
]


class Cliente(Pessoa):
    limite_de_credito = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    indicador_ie = models.CharField(
        max_length=1, choices=INDICADOR_IE_DEST, default='9')
    id_estrangeiro = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "Cliente"
