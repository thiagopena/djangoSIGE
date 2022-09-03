# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.template.defaultfilters import date

from decimal import Decimal
import os
import re

from djangosige.configs.settings import MEDIA_ROOT, APP_ROOT


IND_PAG_ESCOLHAS = (
    (u'0', u'Pagamento à vista'),
    (u'1', u'Pagamento a prazo'),
    (u'2', u'Outros'),
)

MOD_NFE_ESCOLHAS = (
    (u'55', u'NF-e (55)'),
    (u'65', u'NFC-e (65)'),
)

TP_NFE_ESCOLHAS = (
    (u'0', u'Entrada'),
    (u'1', u'Saída'),
)

IDDEST_ESCOLHAS = (
    (u'1', u'Operação interna'),
    (u'2', u'Operação interestadual'),
    (u'3', u'Operação com exterior'),
)

TP_IMP_ESCOLHAS = (
    (u'0', u'Sem geração de DANFE'),
    (u'1', u'DANFE normal, Retrato'),
    (u'2', u'DANFE normal, Paisagem'),
    (u'4', u'DANFE NFC-e'),
)

TP_EMIS_ESCOLHAS = (
    (u'1', u'Emissão normal'),
    (u'2', u'Emissão em contingência'),
)

TP_AMB_ESCOLHAS = (
    (u'1', 'Produção'),
    (u'2', 'Homologação'),
)

FIN_NFE_ESCOLHAS = (
    (u'1', u'NF-e normal'),
    (u'2', u'NF-e complementar'),
    (u'3', u'NF-e de ajuste'),
    (u'4', u'Devolução de mercadoria'),
)

IND_FINAL_ESCOLHAS = (
    (u'0', u'0 - Não'),
    (u'1', u'1 - Sim'),
)

IND_PRES_ESCOLHAS = (
    (u'0', u'Não se aplica'),
    (u'1', u'Operação presencial'),
    (u'2', u'Operação não presencial, pela Internet'),
    (u'3', u'Operação não presencial, Teleatendimento'),
    (u'4', u'NFC-e em operação com entrega a domicílio'),
    (u'5', u'Operação presencial, fora do estabelecimento'),
    (u'9', u'Operação não presencial, outros.'),
)

VERSOES = (
    ('4.00', 'v4.00'),
)

ORIENTACAO_LOGO_DANFE = (
    (u'H', u'Horizontal'),
    (u'V', u'Vertical'),
)

STATUS_NFE_ESCOLHAS = (
    (u'0', u'Assinada'),
    (u'1', u'Autorizada'),
    (u'2', u'Denegada'),
    (u'3', u'Em Digitação'),
    (u'4', u'Em Processamento na SEFAZ'),
    (u'5', u'Rejeitada'),
    (u'6', u'Validada'),
    (u'7', u'Pendente'),
    (u'8', u'Cancelada'),
    (u'9', u'Importada por XML')
)

ERROS_NFE_TIPOS = (
    (u'0', 'Erro'),
    (u'1', 'Alerta'),
)

RETORNO_SEFAZ_TIPOS = (
    (u'0', u'Erro'),
    (u'1', u'Resultado do processamento'),
    (u'2', u'Rejeição'),
    (u'3', u'Motivo denegação'),
    (u'4', u'Alerta'),
)


def arquivo_proc_path(instance, filename):
    return 'ArquivosXML/ProcNFeUpload/{0}'.format(filename)


class NotaFiscal(models.Model):
    chave = models.CharField(max_length=44)
    versao = models.CharField(max_length=4, choices=VERSOES, default='4.00')
    natop = models.CharField(max_length=60)
    indpag = models.CharField(max_length=1, choices=IND_PAG_ESCOLHAS)
    mod = models.CharField(
        max_length=2, choices=MOD_NFE_ESCOLHAS, default=u'55')
    serie = models.CharField(max_length=3)
    dhemi = models.DateTimeField()
    dhsaient = models.DateTimeField(null=True, blank=True)
    iddest = models.CharField(max_length=1, choices=IDDEST_ESCOLHAS)
    tp_imp = models.CharField(max_length=1, choices=TP_IMP_ESCOLHAS)
    tp_emis = models.CharField(
        max_length=1, choices=TP_EMIS_ESCOLHAS, default=u'1')
    tp_amb = models.CharField(max_length=1, choices=TP_AMB_ESCOLHAS)
    fin_nfe = models.CharField(
        max_length=1, choices=FIN_NFE_ESCOLHAS, default=u'1')
    ind_final = models.CharField(
        max_length=1, choices=IND_FINAL_ESCOLHAS, default=u'0')
    ind_pres = models.CharField(
        max_length=1, choices=IND_PRES_ESCOLHAS, default=u'0')

    inf_ad_fisco = models.CharField(max_length=2000, null=True, blank=True)
    inf_cpl = models.CharField(max_length=5000, null=True, blank=True)

    status_nfe = models.CharField(max_length=1, choices=STATUS_NFE_ESCOLHAS)
    arquivo_proc = models.FileField(
        max_length=2055, upload_to=arquivo_proc_path, null=True, blank=True)
    numero_lote = models.CharField(max_length=16, null=True, blank=True)
    numero_protocolo = models.CharField(max_length=16, null=True, blank=True)
    just_canc = models.CharField(max_length=255, null=True, blank=True)

    @property
    def consumidor(self):
        if self.mod == '65':
            return True
        else:
            return False

    @property
    def contingencia(self):
        if self.tp_emis == '1':
            return False
        else:
            return True

    @property
    def caminho_proc_completo(self):
        if self.arquivo_proc:
            if APP_ROOT in self.arquivo_proc.name:
                return self.arquivo_proc.name
            else:
                return os.path.join(APP_ROOT, self.arquivo_proc.url)
        else:
            return ''

    def format_data_emissao(self):
        return '%s' % date(self.dhemi.date(), "d/m/Y")


class NotaFiscalSaida(NotaFiscal):
    tpnf = models.CharField(
        max_length=1, choices=TP_NFE_ESCOLHAS, default=u'1')
    n_nf_saida = models.CharField(max_length=9, validators=[
                                  RegexValidator(r'^\d{1,10}$')], unique=True)
    venda = models.ForeignKey('vendas.PedidoVenda', related_name="venda_nfe",
                              on_delete=models.SET_NULL, null=True, blank=True)
    emit_saida = models.ForeignKey(
        'cadastro.Empresa', related_name="emit_nfe_saida", on_delete=models.SET_NULL, null=True, blank=True)
    dest_saida = models.ForeignKey(
        'cadastro.Cliente', related_name="dest_nfe_saida", on_delete=models.SET_NULL, null=True, blank=True)

    # Cobranca Fatura(NF-e)
    n_fat = models.CharField(max_length=60, null=True, blank=True, unique=True)
    v_orig = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                 MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    v_desc = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                 MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    v_liq = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    grupo_cobr = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Nota Fiscal"
        permissions = (
            ("emitir_notafiscal", "Pode emitir notas fiscais"),
            ("cancelar_notafiscal", "Pode cancelar notas fiscais"),
            ("gerar_danfe", "Pode gerar DANFE/DANFCE"),
            ("consultar_cadastro", "Pode consultar cadastro no SEFAZ"),
            ("inutilizar_notafiscal", "Pode inutilizar notas fiscais"),
            ("consultar_notafiscal", "Pode consultar notas fiscais"),
            ("baixar_notafiscal", "Pode baixar notas fiscais"),
            ("manifestacao_destinatario", "Pode efetuar manifestação do destinatário"),
        )

    @property
    def estado(self):
        if self.emit_saida:
            if self.emit_saida.endereco_padrao:
                return self.emit_saida.endereco_padrao.uf
        return ''

    def get_emit_cmun(self):
        if self.emit_saida:
            if self.emit_saida.endereco_padrao:
                return self.emit_saida.endereco_padrao.cmun
        return ''

    def __unicode__(self):
        s = u'Série %s,  Nº %s, Chave %s' % (
            self.serie, self.n_nf_saida, self.chave)
        return s

    def __str__(self):
        s = u'Série %s,  Nº %s, Chave %s' % (
            self.serie, self.n_nf_saida, self.chave)
        return s


class NotaFiscalEntrada(NotaFiscal):
    n_nf_entrada = models.CharField(max_length=9, validators=[
                                    RegexValidator(r'^\d{1,10}$')])
    compra = models.ForeignKey('compras.PedidoCompra', related_name="compra_nfe",
                               on_delete=models.SET_NULL, null=True, blank=True)
    emit_entrada = models.ForeignKey(
        'cadastro.Fornecedor', related_name="emit_nfe_entrada", on_delete=models.SET_NULL, null=True, blank=True)
    dest_entrada = models.ForeignKey(
        'cadastro.Empresa', related_name="dest_nfe_entrada", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Nota Fiscal de Fornecedor"

    @property
    def estado(self):
        if self.emit_entrada:
            if self.emit_entrada.endereco_padrao:
                return self.emit_entrada.endereco_padrao.uf
        return ''

    def __unicode__(self):
        s = u'Série %s,  Nº %s, Chave %s' % (
            self.serie, self.n_nf_entrada, self.chave)
        return s

    def __str__(self):
        s = u'Série %s,  Nº %s, Chave %s' % (
            self.serie, self.n_nf_entrada, self.chave)
        return s


class AutXML(models.Model):
    nfe = models.ForeignKey('fiscal.NotaFiscalSaida',
                            related_name="aut_xml", on_delete=models.CASCADE)
    cpf_cnpj = models.CharField(max_length=32, null=True, blank=True)

    def get_cpf_cnpj_apenas_digitos(self):
        return re.sub('[./-]', '', self.cpf_cnpj)


class ConfiguracaoNotaFiscal(models.Model):
    arquivo_certificado_a1 = models.FileField(
        upload_to='arquivos/certificado/', null=True, blank=True)
    senha_certificado = models.CharField(max_length=255, null=True, blank=True)
    serie_atual = models.CharField(max_length=3, default='101')
    ambiente = models.CharField(
        max_length=1, choices=TP_AMB_ESCOLHAS, default=u'2')
    imp_danfe = models.CharField(
        max_length=1, choices=TP_IMP_ESCOLHAS, default=u'1')

    inserir_logo_danfe = models.BooleanField(default=True)
    orientacao_logo_danfe = models.CharField(
        max_length=1, choices=ORIENTACAO_LOGO_DANFE, default=u'H')

    csc = models.CharField(max_length=64, null=True, blank=True)
    cidtoken = models.CharField(max_length=8, null=True, blank=True)

    class Meta:
        default_permissions = ()
        verbose_name = "Configuração NF-e"
        permissions = (
            ("configurar_nfe", "Pode modificar configuração de NF-e"),
        )

    @property
    def leiaute_logo_vertical(self):
        if self.orientacao_logo_danfe == 'H':
            return False
        else:
            return True

    def get_certificado_a1(self):
        return os.path.join(MEDIA_ROOT, self.arquivo_certificado_a1.name)


class ErrosValidacaoNotaFiscal(models.Model):
    nfe = models.ForeignKey('fiscal.NotaFiscalSaida',
                            related_name="erros_nfe", on_delete=models.CASCADE)
    tipo = models.CharField(
        max_length=1, choices=ERROS_NFE_TIPOS, null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)


class RespostaSefazNotaFiscal(models.Model):
    nfe = models.ForeignKey('fiscal.NotaFiscalSaida',
                            related_name="erros_nfe_sefaz", on_delete=models.CASCADE)
    tipo = models.CharField(
        max_length=1, choices=RETORNO_SEFAZ_TIPOS, null=True, blank=True)
    codigo = models.CharField(max_length=3, null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
