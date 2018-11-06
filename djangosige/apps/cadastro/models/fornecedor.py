# -*- coding: utf-8 -*-

from django.db import models

from .base import Pessoa


class Fornecedor(Pessoa):
    ramo = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = "Fornecedor"
