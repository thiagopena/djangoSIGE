# -*- coding: utf-8 -*-

import re
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

UF_SIGLA = [
    ("AC", "AC"),
    ("AL", "AL"),
    ("AP", "AP"),
    ("AM", "AM"),
    ("BA", "BA"),
    ("CE", "CE"),
    ("DF", "DF"),
    ("ES", "ES"),
    ("EX", "EX"),
    ("GO", "GO"),
    ("MA", "MA"),
    ("MT", "MT"),
    ("MS", "MS"),
    ("MG", "MG"),
    ("PA", "PA"),
    ("PB", "PB"),
    ("PR", "PR"),
    ("PE", "PE"),
    ("PI", "PI"),
    ("RJ", "RJ"),
    ("RN", "RN"),
    ("RS", "RS"),
    ("RO", "RO"),
    ("RR", "RR"),
    ("SC", "SC"),
    ("SP", "SP"),
    ("SE", "SE"),
    ("TO", "TO"),
]

CST_ICMS_ESCOLHAS = (
    ("00", "00 - Tributada integralmente"),
    ("10", "10 - Tributada e com cobrança do ICMS por substituição tributária"),
    (
        "10p",
        "10 - Tributada e com cobrança do ICMS por substituição tributária (com partilha do ICMS)",
    ),
    ("20", "20 - Com redução de base de cálculo."),
    (
        "30",
        "30 - Isenta ou não tributada e com cobrança do ICMS por substituição tributária",
    ),
    ("40", "40 - Isenta"),
    ("41", "41 - Não tributada"),
    (
        "41r",
        "41 - Não tributada ( ICMS ST devido para a UF de destino, nas operações interestaduais de produtos que tiveram retenção antecipada de ICMS por ST na UF do remetente)",
    ),
    ("50", "50 - Suspensão"),
    ("51", "51 - Diferimento"),
    ("60", "60 - Cobrado anteriormente por substituição tributária"),
    (
        "70",
        "70 - Com redução de base de cálculo e cobrança do ICMS por substituição tributária",
    ),
    ("90p", "90 - Outros (com partilha do ICMS)"),
    ("90", "90 -  Outros"),
)

CST_IPI_ESCOLHAS = (
    ("00", "00 - Entrada com Recuperação de Crédito"),
    ("01", "01 - Entrada Tributável com Alíquota Zero"),
    ("02", "02 - Entrada Isenta"),
    ("03", "03 - Entrada Não-Tributada"),
    ("04", "04 - Entrada Imune"),
    ("05", "05 - Entrada com Suspensão"),
    ("49", "49 - Outras Entradas"),
    ("50", "50 - Saída Tributada"),
    ("51", "51 - Saída Tributável com Alíquota Zero"),
    ("52", "52 - Saída Isenta"),
    ("53", "53 - Saída Não-Tributada"),
    ("54", "54 - Saída Imune"),
    ("55", "55 - Saída com Suspensão"),
    ("99", "99 - Outras Saídas"),
)

CST_PIS_COFINS_ESCOLHAS = (
    ("01", "01 - Operação Tributável com Alíquota Básica"),
    ("02", "02 - Operação Tributável com Alíquota Diferenciada"),
    ("03", "03 - Operação Tributável com Alíquota por Unidade de Medida de Produto"),
    ("04", "04 - Operação Tributável Monofásica - Revenda a Alíquota Zero"),
    ("05", "05 - Operação Tributável por Substituição Tributária"),
    ("06", "06 - Operação Tributável a Alíquota Zero"),
    ("07", "07 - Operação Isenta da Contribuição"),
    ("08", "08 - Operação sem Incidência da Contribuição"),
    ("09", "09 - Operação com Suspensão da Contribuição"),
    ("49", "49 - Outras Operações de Saída"),
    (
        "50",
        "50 - Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno",
    ),
    (
        "51",
        "51 - Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno",
    ),
    (
        "52",
        "52 - Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação",
    ),
    (
        "53",
        "53 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno",
    ),
    (
        "54",
        "54 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação",
    ),
    (
        "55",
        "55 - Operação com Direito a Crédito - Vinculada a Receitas Não Tributadas no Mercado Interno e de Exportação",
    ),
    (
        "56",
        "56 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno e de Exportação",
    ),
    (
        "60",
        "60 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno",
    ),
    (
        "61",
        "61 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno",
    ),
    (
        "62",
        "62 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação",
    ),
    (
        "63",
        "63 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno",
    ),
    (
        "64",
        "64 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação",
    ),
    (
        "65",
        "65 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação",
    ),
    (
        "66",
        "66 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno e de Exportação",
    ),
    ("67", "67 - Crédito Presumido - Outras Operações"),
    ("70", "70 - Operação de Aquisição sem Direito a Crédito"),
    ("71", "71 - Operação de Aquisição com Isenção"),
    ("72", "72 - Operação de Aquisição com Suspensão"),
    ("73", "73 - Operação de Aquisição a Alíquota Zero"),
    ("74", "74 - Operação de Aquisição sem Incidência da Contribuição"),
    ("75", "75 - Operação de Aquisição por Substituição Tributária"),
    ("98", "98 - Outras Operações de Entrada"),
    ("99", "99 - Outras Operações"),
)

CSOSN_ESCOLHAS = (
    ("101", "101 - Tributada  com permissão de crédito"),
    ("102", "102 - Tributada sem permissão de crédito"),
    ("103", "103 - Isenção do ICMS para faixa de receita bruta"),
    (
        "201",
        "201 - Tributada com permissão de crédito e com cobrança do ICMS por Substituição Tributária",
    ),
    (
        "202",
        "202 - Tributada sem permissão de crédito e com cobrança do ICMS por Substituição Tributária",
    ),
    (
        "203",
        "203 - Isenção do ICMS para faixa de receita bruta e com cobrança do ICMS por Substituição Tributária",
    ),
    ("300", "300 - Imune"),
    ("400", "400 - Não tributada"),
    (
        "500",
        "500 - ICMS cobrado anteriormente por substituição tributária (substituído) ou por antecipação.",
    ),
    ("900", "900 - Outros"),
)

MOD_BCST_ESCOLHAS = (
    ("0", "0 - Preço tabelado ou máximo sugerido"),
    ("1", "1 - Lista Negativa (valor)"),
    ("2", "2 - Lista Positiva (valor)"),
    ("3", "3 - Lista Neutra (valor)"),
    ("4", "4 - Margem Valor Agregado (%)"),
    ("5", "5 - Pauta (valor)"),
)

MOD_BC_ESCOLHAS = (
    ("0", "0 - Margem Valor Agregado (%)"),
    ("1", "1 - Pauta (Valor)"),
    ("2", "2 - Preço Tabelado Máx. (valor)"),
    ("3", "3 - Valor da operação"),
)

MOT_DES_ICMS = (
    ("1", "1 - Táxi"),
    ("3", "3 - Produtor Agropecuário"),
    ("4", "4 - Frotista/Locadora"),
    ("5", "5 - Diplomático/Consular"),
    (
        "6",
        "6 - Utilitários e Motocicletas da Amazônia Ocidental e Áreas de Livre Comércio",
    ),
    ("7", "7 - SUFRAMA"),
    ("8", "8 - Venda a Órgão Público"),
    ("9", "9 - Outros"),
    ("10", "10 - Deficiente Condutor"),
    ("11", "11 - Deficiente Não Condutor"),
    ("12", "12 - Órgão de fomento e desenvolvimento agropecuário"),
    ("16", "16 - Olimpíadas Rio 2016"),
)

P_ICMS_INTER_ESCOLHAS = (
    (Decimal("4.00"), "4% alíquota interestadual para produtos importados"),
    (
        Decimal("7.00"),
        "7% para os Estados de origem do Sul e Sudeste (exceto ES), destinado para os Estados do Norte, Nordeste, CentroOeste e Espírito Santo",
    ),
    (Decimal("12.00"), "12% para os demais casos"),
)

P_ICMS_INTER_PART_ESCOLHAS = (
    (Decimal("40.00"), "40% em 2016"),
    (Decimal("60.00"), "60% em 2017"),
    (Decimal("80.00"), "80% em 2018"),
    (Decimal("100.00"), "100% a partir de 2019"),
)

REGIME_TRIB_ESCOLHAS = (
    ("0", "Tributação Normal"),
    ("1", "Simples Nacional"),
)

TIPO_IPI = (
    ("0", "Não sujeito ao IPI"),
    ("1", "Valor fixo"),
    ("2", "Alíquota"),
)


class GrupoFiscal(models.Model):
    descricao = models.CharField(max_length=255)
    regime_trib = models.CharField(max_length=1, choices=REGIME_TRIB_ESCOLHAS)

    class Meta:
        verbose_name = "Grupo Fiscal"

    def __unicode__(self):
        s = "%s" % (self.descricao)
        return s

    def __str__(self):
        s = "%s" % (self.descricao)
        return s


class ICMS(models.Model):
    # Nota Fiscal
    cst = models.CharField(
        max_length=3, choices=CST_ICMS_ESCOLHAS, help_text="icms-cst"
    )
    mod_bc = models.CharField(
        max_length=1,
        choices=MOD_BC_ESCOLHAS,
        default="3",
        help_text="icms00 icms10 icms20 icms51 icms70 icms90 icms10p icms90p",
    )
    p_icms = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icms00 icms10 icms20 icms51 icms70 icms90 icms10p icms90p",
    )
    p_red_bc = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icms20 icms51 icms70 icms90 icms10p icms90p",
    )
    mod_bcst = models.CharField(
        max_length=1,
        choices=MOD_BCST_ESCOLHAS,
        default="4",
        help_text="icms10 icms30 icms70 icms90 icms10p icms90p",
    )
    p_mvast = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icms10 icms30 icms70 icms90 icms10p icms90p",
    )
    p_red_bcst = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icms10 icms30 icms70 icms90 icms10p icms90p",
    )
    p_icmsst = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icms10 icms30 icms70 icms90 icms10p icms90p",
    )
    mot_des_icms = models.CharField(
        max_length=3,
        choices=MOT_DES_ICMS,
        null=True,
        blank=True,
        help_text="icms20 icms30 icms40 icms41 icms50 icms70 icms90",
    )
    p_dif = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icms51",
    )
    p_bc_op = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icms10p icms90p",
    )
    ufst = models.CharField(
        max_length=2,
        choices=UF_SIGLA,
        null=True,
        blank=True,
        help_text="icms10p icms90p",
    )
    grupo_fiscal = models.ForeignKey(
        "fiscal.GrupoFiscal",
        related_name="icms_padrao",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # Calculo do imposto
    icms_incluido_preco = models.BooleanField(default=False, help_text="calculo-icms")
    icmsst_incluido_preco = models.BooleanField(default=False, help_text="calculo-icms")


class ICMSUFDest(models.Model):
    p_fcp_dest = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
    )
    p_icms_dest = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
    )
    p_icms_inter = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        choices=P_ICMS_INTER_ESCOLHAS,
        null=True,
        blank=True,
    )
    p_icms_inter_part = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        choices=P_ICMS_INTER_PART_ESCOLHAS,
        null=True,
        blank=True,
    )
    grupo_fiscal = models.ForeignKey(
        "fiscal.GrupoFiscal",
        related_name="icms_dest_padrao",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class ICMSSN(models.Model):
    csosn = models.CharField(
        max_length=3, choices=CSOSN_ESCOLHAS, help_text="icmssn-csosn"
    )
    p_cred_sn = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icmssn101 icmssn201 icmssn900",
    )
    mod_bc = models.CharField(
        max_length=1, choices=MOD_BC_ESCOLHAS, default="3", help_text="icmssn900"
    )
    mod_bcst = models.CharField(
        max_length=1,
        choices=MOD_BCST_ESCOLHAS,
        default="4",
        help_text="icmssn201 icmssn202 icmssn203 icmssn900",
    )
    p_mvast = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icmssn201 icmssn202 icmssn203 icmssn900",
    )
    p_red_bcst = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icmssn201 icmssn202 icmssn203 icmssn900",
    )
    p_icmsst = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icmssn201 icmssn202 icmssn203 icmssn900",
    )
    p_red_bc = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icmssn201 icmssn202 icmssn203 icmssn900",
    )
    p_icms = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
        help_text="icmssn201 icmssn202 icmssn203 icmssn900",
    )
    grupo_fiscal = models.ForeignKey(
        "fiscal.GrupoFiscal",
        related_name="icms_sn_padrao",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # Calculo do imposto
    icmssn_incluido_preco = models.BooleanField(
        default=False, help_text="calculo-icmssn"
    )
    icmssnst_incluido_preco = models.BooleanField(
        default=False, help_text="calculo-icmssn"
    )


class IPI(models.Model):
    cst = models.CharField(
        max_length=2, choices=CST_IPI_ESCOLHAS, null=True, blank=True
    )
    cl_enq = models.CharField(max_length=5, null=True, blank=True)
    c_enq = models.CharField(max_length=3, null=True, blank=True)
    cnpj_prod = models.CharField(max_length=32, null=True, blank=True)
    tipo_ipi = models.CharField(max_length=1, choices=TIPO_IPI, default="2")
    p_ipi = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
    )
    valor_fixo = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
    )  # Caso IPI for valor fixo
    grupo_fiscal = models.ForeignKey(
        "fiscal.GrupoFiscal",
        related_name="ipi_padrao",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # Calculo do imposto
    ipi_incluido_preco = models.BooleanField(default=False, help_text="calculo-ipi")
    incluir_bc_icms = models.BooleanField(default=False, help_text="calculo-ipi")
    incluir_bc_icmsst = models.BooleanField(default=False, help_text="calculo-ipi")

    def get_cnpj_prod_apenas_digitos(self):
        return re.sub("[./-]", "", self.cnpj_prod)


class PIS(models.Model):
    cst = models.CharField(
        max_length=2, choices=CST_PIS_COFINS_ESCOLHAS, null=True, blank=True
    )
    p_pis = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
    )
    valiq_pis = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
    )
    grupo_fiscal = models.ForeignKey(
        "fiscal.GrupoFiscal",
        related_name="pis_padrao",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class COFINS(models.Model):
    cst = models.CharField(
        max_length=2, choices=CST_PIS_COFINS_ESCOLHAS, null=True, blank=True
    )
    p_cofins = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
    )
    valiq_cofins = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
    )
    grupo_fiscal = models.ForeignKey(
        "fiscal.GrupoFiscal",
        related_name="cofins_padrao",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


# class ISSQN(models.Model):
