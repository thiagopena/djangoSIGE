# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import re

UF_SIGLA = [
    ('AC', 'AC'),
    ('AL', 'AL'),
    ('AP', 'AP'),
    ('AM', 'AM'),
    ('BA', 'BA'),
    ('CE', 'CE'),
    ('DF', 'DF'),
    ('ES', 'ES'),
    ('EX', 'EX'),
    ('GO', 'GO'),
    ('MA', 'MA'),
    ('MT', 'MT'),
    ('MS', 'MS'),
    ('MG', 'MG'),
    ('PA', 'PA'),
    ('PB', 'PB'),
    ('PR', 'PR'),
    ('PE', 'PE'),
    ('PI', 'PI'),
    ('RJ', 'RJ'),
    ('RN', 'RN'),
    ('RS', 'RS'),
    ('RO', 'RO'),
    ('RR', 'RR'),
    ('SC', 'SC'),
    ('SP', 'SP'),
    ('SE', 'SE'),
    ('TO', 'TO'),
]

CST_ICMS_ESCOLHAS = (
    (u'00', u'00 - Tributada integralmente'),
    (u'10', u'10 - Tributada e com cobrança do ICMS por substituição tributária'),
    (u'10p', u'10 - Tributada e com cobrança do ICMS por substituição tributária (com partilha do ICMS)'),
    (u'20', u'20 - Com redução de base de cálculo.'),
    (u'30', u'30 - Isenta ou não tributada e com cobrança do ICMS por substituição tributária'),
    (u'40', u'40 - Isenta'),
    (u'41', u'41 - Não tributada'),
    (u'41r', u'41 - Não tributada ( ICMS ST devido para a UF de destino, nas operações interestaduais de produtos que tiveram retenção antecipada de ICMS por ST na UF do remetente)'),
    (u'50', u'50 - Suspensão'),
    (u'51', u'51 - Diferimento'),
    (u'60', u'60 - Cobrado anteriormente por substituição tributária'),
    (u'70', u'70 - Com redução de base de cálculo e cobrança do ICMS por substituição tributária'),
    (u'90p', u'90 - Outros (com partilha do ICMS)'),
    (u'90', u'90 -  Outros'),
)

CST_IPI_ESCOLHAS = (
    (u'00', u'00 - Entrada com Recuperação de Crédito'),
    (u'01', u'01 - Entrada Tributável com Alíquota Zero'),
    (u'02', u'02 - Entrada Isenta'),
    (u'03', u'03 - Entrada Não-Tributada'),
    (u'04', u'04 - Entrada Imune'),
    (u'05', u'05 - Entrada com Suspensão'),
    (u'49', u'49 - Outras Entradas'),
    (u'50', u'50 - Saída Tributada'),
    (u'51', u'51 - Saída Tributável com Alíquota Zero'),
    (u'52', u'52 - Saída Isenta'),
    (u'53', u'53 - Saída Não-Tributada'),
    (u'54', u'54 - Saída Imune'),
    (u'55', u'55 - Saída com Suspensão'),
    (u'99', u'99 - Outras Saídas'),
)

CST_PIS_COFINS_ESCOLHAS = (
    (u'01', u'01 - Operação Tributável com Alíquota Básica'),
    (u'02', u'02 - Operação Tributável com Alíquota Diferenciada'),
    (u'03', u'03 - Operação Tributável com Alíquota por Unidade de Medida de Produto'),
    (u'04', u'04 - Operação Tributável Monofásica - Revenda a Alíquota Zero'),
    (u'05', u'05 - Operação Tributável por Substituição Tributária'),
    (u'06', u'06 - Operação Tributável a Alíquota Zero'),
    (u'07', u'07 - Operação Isenta da Contribuição'),
    (u'08', u'08 - Operação sem Incidência da Contribuição'),
    (u'09', u'09 - Operação com Suspensão da Contribuição'),
    (u'49', u'49 - Outras Operações de Saída'),
    (u'50', u'50 - Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno'),
    (u'51', u'51 - Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno'),
    (u'52', u'52 - Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação'),
    (u'53', u'53 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno'),
    (u'54', u'54 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação'),
    (u'55', u'55 - Operação com Direito a Crédito - Vinculada a Receitas Não Tributadas no Mercado Interno e de Exportação'),
    (u'56', u'56 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno e de Exportação'),
    (u'60', u'60 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno'),
    (u'61', u'61 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno'),
    (u'62', u'62 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação'),
    (u'63', u'63 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno'),
    (u'64', u'64 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação'),
    (u'65', u'65 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação'),
    (u'66', u'66 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno e de Exportação'),
    (u'67', u'67 - Crédito Presumido - Outras Operações'),
    (u'70', u'70 - Operação de Aquisição sem Direito a Crédito'),
    (u'71', u'71 - Operação de Aquisição com Isenção'),
    (u'72', u'72 - Operação de Aquisição com Suspensão'),
    (u'73', u'73 - Operação de Aquisição a Alíquota Zero'),
    (u'74', u'74 - Operação de Aquisição sem Incidência da Contribuição'),
    (u'75', u'75 - Operação de Aquisição por Substituição Tributária'),
    (u'98', u'98 - Outras Operações de Entrada'),
    (u'99', u'99 - Outras Operações'),
)

CSOSN_ESCOLHAS = (
    (u'101', u'101 - Tributada  com permissão de crédito'),
    (u'102', u'102 - Tributada sem permissão de crédito'),
    (u'103', u'103 - Isenção do ICMS para faixa de receita bruta'),
    (u'201', u'201 - Tributada com permissão de crédito e com cobrança do ICMS por Substituição Tributária'),
    (u'202', u'202 - Tributada sem permissão de crédito e com cobrança do ICMS por Substituição Tributária'),
    (u'203', u'203 - Isenção do ICMS para faixa de receita bruta e com cobrança do ICMS por Substituição Tributária'),
    (u'300', u'300 - Imune'),
    (u'400', u'400 - Não tributada'),
    (u'500', u'500 - ICMS cobrado anteriormente por substituição tributária (substituído) ou por antecipação.'),
    (u'900', u'900 - Outros'),
)

MOD_BCST_ESCOLHAS = (
    (u'0', u'0 - Preço tabelado ou máximo sugerido'),
    (u'1', u'1 - Lista Negativa (valor)'),
    (u'2', u'2 - Lista Positiva (valor)'),
    (u'3', u'3 - Lista Neutra (valor)'),
    (u'4', u'4 - Margem Valor Agregado (%)'),
    (u'5', u'5 - Pauta (valor)'),
)

MOD_BC_ESCOLHAS = (
    (u'0', u'0 - Margem Valor Agregado (%)'),
    (u'1', u'1 - Pauta (Valor)'),
    (u'2', u'2 - Preço Tabelado Máx. (valor)'),
    (u'3', u'3 - Valor da operação'),
)

MOT_DES_ICMS = (
    (u'1', u'1 - Táxi'),
    (u'3', u'3 - Produtor Agropecuário'),
    (u'4', u'4 - Frotista/Locadora'),
    (u'5', u'5 - Diplomático/Consular'),
    (u'6', u'6 - Utilitários e Motocicletas da Amazônia Ocidental e Áreas de Livre Comércio'),
    (u'7', u'7 - SUFRAMA'),
    (u'8', u'8 - Venda a Órgão Público'),
    (u'9', u'9 - Outros'),
    (u'10', u'10 - Deficiente Condutor'),
    (u'11', u'11 - Deficiente Não Condutor'),
    (u'12', u'12 - Órgão de fomento e desenvolvimento agropecuário'),
    (u'16', u'16 - Olimpíadas Rio 2016'),
)

P_ICMS_INTER_ESCOLHAS = (
    (Decimal('4.00'), u'4% alíquota interestadual para produtos importados'),
    (Decimal('7.00'), u'7% para os Estados de origem do Sul e Sudeste (exceto ES), destinado para os Estados do Norte, Nordeste, CentroOeste e Espírito Santo'),
    (Decimal('12.00'), u'12% para os demais casos'),
)

P_ICMS_INTER_PART_ESCOLHAS = (
    (Decimal('40.00'), u'40% em 2016'),
    (Decimal('60.00'), u'60% em 2017'),
    (Decimal('80.00'), u'80% em 2018'),
    (Decimal('100.00'), u'100% a partir de 2019'),
)

REGIME_TRIB_ESCOLHAS = (
    (u'0', u'Tributação Normal'),
    (u'1', u'Simples Nacional'),
)

TIPO_IPI = (
    (u'0', 'Não sujeito ao IPI'),
    (u'1', u'Valor fixo'),
    (u'2', u'Alíquota'),
)


class GrupoFiscal(models.Model):
    descricao = models.CharField(max_length=255)
    regime_trib = models.CharField(max_length=1, choices=REGIME_TRIB_ESCOLHAS)

    class Meta:
        verbose_name = "Grupo Fiscal"

    def __unicode__(self):
        s = u'%s' % (self.descricao)
        return s

    def __str__(self):
        s = u'%s' % (self.descricao)
        return s


class ICMS(models.Model):
    # Nota Fiscal
    cst = models.CharField(
        max_length=3, choices=CST_ICMS_ESCOLHAS, help_text='icms-cst')
    mod_bc = models.CharField(max_length=1, choices=MOD_BC_ESCOLHAS, default='3',
                              help_text='icms00 icms10 icms20 icms51 icms70 icms90 icms10p icms90p')
    p_icms = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                 help_text='icms00 icms10 icms20 icms51 icms70 icms90 icms10p icms90p')
    p_red_bc = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                   help_text='icms20 icms51 icms70 icms90 icms10p icms90p')
    mod_bcst = models.CharField(max_length=1, choices=MOD_BCST_ESCOLHAS, default='4',
                                help_text='icms10 icms30 icms70 icms90 icms10p icms90p')
    p_mvast = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                  help_text='icms10 icms30 icms70 icms90 icms10p icms90p')
    p_red_bcst = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                     help_text='icms10 icms30 icms70 icms90 icms10p icms90p')
    p_icmsst = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                   help_text='icms10 icms30 icms70 icms90 icms10p icms90p')
    mot_des_icms = models.CharField(max_length=3, choices=MOT_DES_ICMS, null=True, blank=True,
                                    help_text='icms20 icms30 icms40 icms41 icms50 icms70 icms90')
    p_dif = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                help_text='icms51')
    p_bc_op = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                  help_text='icms10p icms90p')
    ufst = models.CharField(max_length=2, choices=UF_SIGLA, null=True, blank=True,
                            help_text='icms10p icms90p')
    grupo_fiscal = models.ForeignKey(
        'fiscal.GrupoFiscal', related_name="icms_padrao", on_delete=models.CASCADE, null=True, blank=True)

    # Calculo do imposto
    icms_incluido_preco = models.BooleanField(
        default=False, help_text='calculo-icms')
    icmsst_incluido_preco = models.BooleanField(
        default=False, help_text='calculo-icms')


class ICMSUFDest(models.Model):
    p_fcp_dest = models.DecimalField(max_digits=6, decimal_places=2, validators=[
                                     MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    p_icms_dest = models.DecimalField(max_digits=6, decimal_places=2, validators=[
                                      MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    p_icms_inter = models.DecimalField(max_digits=6, decimal_places=2, validators=[
                                       MinValueValidator(Decimal('0.00'))], choices=P_ICMS_INTER_ESCOLHAS, null=True, blank=True)
    p_icms_inter_part = models.DecimalField(max_digits=6, decimal_places=2, validators=[
                                            MinValueValidator(Decimal('0.00'))], choices=P_ICMS_INTER_PART_ESCOLHAS, null=True, blank=True)
    grupo_fiscal = models.ForeignKey(
        'fiscal.GrupoFiscal', related_name="icms_dest_padrao", on_delete=models.CASCADE, null=True, blank=True)


class ICMSSN(models.Model):
    csosn = models.CharField(
        max_length=3, choices=CSOSN_ESCOLHAS, help_text='icmssn-csosn')
    p_cred_sn = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                    help_text='icmssn101 icmssn201 icmssn900')
    mod_bc = models.CharField(max_length=1, choices=MOD_BC_ESCOLHAS, default='3',
                              help_text='icmssn900')
    mod_bcst = models.CharField(max_length=1, choices=MOD_BCST_ESCOLHAS, default='4',
                                help_text='icmssn201 icmssn202 icmssn203 icmssn900')
    p_mvast = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                  help_text='icmssn201 icmssn202 icmssn203 icmssn900')
    p_red_bcst = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                     help_text='icmssn201 icmssn202 icmssn203 icmssn900')
    p_icmsst = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                   help_text='icmssn201 icmssn202 icmssn203 icmssn900')
    p_red_bc = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                   help_text='icmssn201 icmssn202 icmssn203 icmssn900')
    p_icms = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True,
                                 help_text='icmssn201 icmssn202 icmssn203 icmssn900')
    grupo_fiscal = models.ForeignKey(
        'fiscal.GrupoFiscal', related_name="icms_sn_padrao", on_delete=models.CASCADE, null=True, blank=True)

    # Calculo do imposto
    icmssn_incluido_preco = models.BooleanField(
        default=False, help_text='calculo-icmssn')
    icmssnst_incluido_preco = models.BooleanField(
        default=False, help_text='calculo-icmssn')


class IPI(models.Model):
    cst = models.CharField(
        max_length=2, choices=CST_IPI_ESCOLHAS, null=True, blank=True)
    cl_enq = models.CharField(max_length=5, null=True, blank=True)
    c_enq = models.CharField(max_length=3, null=True, blank=True)
    cnpj_prod = models.CharField(max_length=32, null=True, blank=True)
    tipo_ipi = models.CharField(max_length=1, choices=TIPO_IPI, default='2')
    p_ipi = models.DecimalField(max_digits=6, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    valor_fixo = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                     MinValueValidator(Decimal('0.00'))], null=True, blank=True)  # Caso IPI for valor fixo
    grupo_fiscal = models.ForeignKey(
        'fiscal.GrupoFiscal', related_name="ipi_padrao", on_delete=models.CASCADE, null=True, blank=True)

    # Calculo do imposto
    ipi_incluido_preco = models.BooleanField(
        default=False, help_text='calculo-ipi')
    incluir_bc_icms = models.BooleanField(
        default=False, help_text='calculo-ipi')
    incluir_bc_icmsst = models.BooleanField(
        default=False, help_text='calculo-ipi')

    def get_cnpj_prod_apenas_digitos(self):
        return re.sub('[./-]', '', self.cnpj_prod)


class PIS(models.Model):
    cst = models.CharField(
        max_length=2, choices=CST_PIS_COFINS_ESCOLHAS, null=True, blank=True)
    p_pis = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    valiq_pis = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                    MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    grupo_fiscal = models.ForeignKey(
        'fiscal.GrupoFiscal', related_name="pis_padrao", on_delete=models.CASCADE, null=True, blank=True)


class COFINS(models.Model):
    cst = models.CharField(
        max_length=2, choices=CST_PIS_COFINS_ESCOLHAS, null=True, blank=True)
    p_cofins = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                   MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    valiq_cofins = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                       MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    grupo_fiscal = models.ForeignKey(
        'fiscal.GrupoFiscal', related_name="cofins_padrao", on_delete=models.CASCADE, null=True, blank=True)


# class ISSQN(models.Model):
