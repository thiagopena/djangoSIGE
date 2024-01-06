# -*- coding: utf-8 -*-

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

ORIGEM_ESCOLHAS = (
    ("0", "0 - Nacional"),
    ("1", "1 - Estrangeira - Importação direta."),
    ("2", "2 - Estrangeira - Adquirida no mercado interno."),
    (
        "3",
        "3 - Nacional - Mercadoria ou bem com Conteúdo de Importação superior a 40% e inferior ou igual a 70%.",
    ),
    (
        "4",
        "4 - Nacional - Cuja produção tenha sido feita em conformidade com os processos produtivos básicos de que tratam o Decreto-Lei nº 288/67, e as Leis nºs 8.248/91, 8.387/91, 10.176/01 e 11.484/ 07",
    ),
    (
        "5",
        "5 - Nacional - Mercadoria ou bem com Conteúdo de Importação inferior ou igual a 40% (quarenta por cento)",
    ),
    (
        "6",
        "6 - Estrangeira - Importação direta, sem similar nacional, constante em lista da Resolução CAMEX nº 79/2012 e gás natural",
    ),
    (
        "7",
        "7 - Estrangeira - Adquirida no mercado interno, sem similar nacional, constante em lista da Resolução CAMEX nº 79/2012 e gás natural",
    ),
    (
        "8",
        "8 - Nacional - Mercadoria ou bem com Conteúdo de Importação superior a 70% (setenta por cento).",
    ),
)

TP_OPERACAO_OPCOES = (
    ("0", "0 - Entrada"),
    ("1", "1 - Saída"),
)

ID_DEST_OPCOES = (
    ("1", "1 - Operação interna."),
    ("2", "2 - Operação interestadual."),
    ("3", "3 - Operação com exterior"),
)


class Categoria(models.Model):
    categoria_desc = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Categoria"

    def __unicode__(self):
        s = "%s" % (self.categoria_desc)
        return s

    def __str__(self):
        s = "%s" % (self.categoria_desc)
        return s


class Marca(models.Model):
    marca_desc = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Marca"

    def __unicode__(self):
        s = "%s" % (self.marca_desc)
        return s

    def __str__(self):
        s = "%s" % (self.marca_desc)
        return s


class Unidade(models.Model):
    sigla_unidade = models.CharField(max_length=3)
    unidade_desc = models.CharField(max_length=16)

    class Meta:
        verbose_name = "Unidade"

    def __unicode__(self):
        s = "(%s) %s" % (self.sigla_unidade, self.unidade_desc)
        return s

    def __str__(self):
        s = "(%s) %s" % (self.sigla_unidade, self.unidade_desc)
        return s


class Produto(models.Model):
    # Dados gerais
    codigo = models.CharField(max_length=15)
    codigo_barras = models.CharField(max_length=16, null=True, blank=True)  # GTIN/EAN
    descricao = models.CharField(max_length=255)
    categoria = models.ForeignKey(
        Categoria, null=True, blank=True, on_delete=models.PROTECT
    )
    marca = models.ForeignKey(Marca, null=True, blank=True, on_delete=models.PROTECT)
    unidade = models.ForeignKey(
        Unidade, null=True, blank=True, on_delete=models.PROTECT
    )
    custo = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("0.00"),
    )
    venda = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("0.00"),
    )
    inf_adicionais = models.CharField(max_length=255, null=True, blank=True)

    # Fiscal
    ncm = models.CharField(max_length=11, null=True, blank=True)  # NCM + EXTIPI
    origem = models.CharField(max_length=1, choices=ORIGEM_ESCOLHAS, default="0")
    # Código Especificador da Substituição Tributária
    cest = models.CharField(max_length=7, null=True, blank=True)
    cfop_padrao = models.ForeignKey(
        "fiscal.NaturezaOperacao", null=True, blank=True, on_delete=models.PROTECT
    )
    grupo_fiscal = models.ForeignKey(
        "fiscal.GrupoFiscal", null=True, blank=True, on_delete=models.PROTECT
    )

    # Estoque
    estoque_minimo = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("0.00"),
    )
    estoque_atual = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("0.00"),
    )
    controlar_estoque = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Produto"

    @property
    def format_unidade(self):
        if self.unidade:
            return self.unidade.sigla_unidade
        else:
            return ""

    def get_sigla_unidade(self):
        if self.unidade:
            return self.unidade.sigla_unidade
        else:
            return ""

    def get_cfop_padrao(self):
        if self.cfop_padrao:
            return self.cfop_padrao.cfop
        else:
            return ""

    def __unicode__(self):
        s = "%s" % (self.descricao)
        return s

    def __str__(self):
        s = "%s" % (self.descricao)
        return s
