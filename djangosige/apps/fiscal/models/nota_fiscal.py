import os
import re
from decimal import Decimal

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.template.defaultfilters import date

from djangosige.configs.settings import APP_ROOT, MEDIA_ROOT

IND_PAG_ESCOLHAS = (
    ("0", "Pagamento à vista"),
    ("1", "Pagamento a prazo"),
    ("2", "Outros"),
)

MOD_NFE_ESCOLHAS = (
    ("55", "NF-e (55)"),
    ("65", "NFC-e (65)"),
)

TP_NFE_ESCOLHAS = (
    ("0", "Entrada"),
    ("1", "Saída"),
)

IDDEST_ESCOLHAS = (
    ("1", "Operação interna"),
    ("2", "Operação interestadual"),
    ("3", "Operação com exterior"),
)

TP_IMP_ESCOLHAS = (
    ("0", "Sem geração de DANFE"),
    ("1", "DANFE normal, Retrato"),
    ("2", "DANFE normal, Paisagem"),
    ("4", "DANFE NFC-e"),
)

TP_EMIS_ESCOLHAS = (
    ("1", "Emissão normal"),
    ("2", "Emissão em contingência"),
)

TP_AMB_ESCOLHAS = (
    ("1", "Produção"),
    ("2", "Homologação"),
)

FIN_NFE_ESCOLHAS = (
    ("1", "NF-e normal"),
    ("2", "NF-e complementar"),
    ("3", "NF-e de ajuste"),
    ("4", "Devolução de mercadoria"),
)

IND_FINAL_ESCOLHAS = (
    ("0", "0 - Não"),
    ("1", "1 - Sim"),
)

IND_PRES_ESCOLHAS = (
    ("0", "Não se aplica"),
    ("1", "Operação presencial"),
    ("2", "Operação não presencial, pela Internet"),
    ("3", "Operação não presencial, Teleatendimento"),
    ("4", "NFC-e em operação com entrega a domicílio"),
    ("5", "Operação presencial, fora do estabelecimento"),
    ("9", "Operação não presencial, outros."),
)

VERSOES = (("3.10", "v3.10"),)

ORIENTACAO_LOGO_DANFE = (
    ("H", "Horizontal"),
    ("V", "Vertical"),
)

STATUS_NFE_ESCOLHAS = (
    ("0", "Assinada"),
    ("1", "Autorizada"),
    ("2", "Denegada"),
    ("3", "Em Digitação"),
    ("4", "Em Processamento na SEFAZ"),
    ("5", "Rejeitada"),
    ("6", "Validada"),
    ("7", "Pendente"),
    ("8", "Cancelada"),
    ("9", "Importada por XML"),
)

ERROS_NFE_TIPOS = (
    ("0", "Erro"),
    ("1", "Alerta"),
)

RETORNO_SEFAZ_TIPOS = (
    ("0", "Erro"),
    ("1", "Resultado do processamento"),
    ("2", "Rejeição"),
    ("3", "Motivo denegação"),
    ("4", "Alerta"),
)


def arquivo_proc_path(instance, filename):
    return f"ArquivosXML/ProcNFeUpload/{filename}"


class NotaFiscal(models.Model):
    chave = models.CharField(max_length=44)
    versao = models.CharField(max_length=4, choices=VERSOES, default="3.10")
    natop = models.CharField(max_length=60)
    indpag = models.CharField(max_length=1, choices=IND_PAG_ESCOLHAS)
    mod = models.CharField(max_length=2, choices=MOD_NFE_ESCOLHAS, default="55")
    serie = models.CharField(max_length=3)
    dhemi = models.DateTimeField()
    dhsaient = models.DateTimeField(null=True, blank=True)
    iddest = models.CharField(max_length=1, choices=IDDEST_ESCOLHAS)
    tp_imp = models.CharField(max_length=1, choices=TP_IMP_ESCOLHAS)
    tp_emis = models.CharField(max_length=1, choices=TP_EMIS_ESCOLHAS, default="1")
    tp_amb = models.CharField(max_length=1, choices=TP_AMB_ESCOLHAS)
    fin_nfe = models.CharField(max_length=1, choices=FIN_NFE_ESCOLHAS, default="1")
    ind_final = models.CharField(max_length=1, choices=IND_FINAL_ESCOLHAS, default="0")
    ind_pres = models.CharField(max_length=1, choices=IND_PRES_ESCOLHAS, default="0")

    inf_ad_fisco = models.CharField(max_length=2000, null=True, blank=True)
    inf_cpl = models.CharField(max_length=5000, null=True, blank=True)

    status_nfe = models.CharField(max_length=1, choices=STATUS_NFE_ESCOLHAS)
    arquivo_proc = models.FileField(
        max_length=2055, upload_to=arquivo_proc_path, null=True, blank=True
    )
    numero_lote = models.CharField(max_length=16, null=True, blank=True)
    numero_protocolo = models.CharField(max_length=16, null=True, blank=True)
    just_canc = models.CharField(max_length=255, null=True, blank=True)

    @property
    def consumidor(self):
        if self.mod == "65":
            return True
        else:
            return False

    @property
    def contingencia(self):
        if self.tp_emis == "1":
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
            return ""

    def format_data_emissao(self):
        return "%s" % date(self.dhemi.date(), "d/m/Y")


class NotaFiscalSaida(NotaFiscal):
    tpnf = models.CharField(max_length=1, choices=TP_NFE_ESCOLHAS, default="1")
    n_nf_saida = models.CharField(
        max_length=9, validators=[RegexValidator(r"^\d{1,10}$")], unique=True
    )
    venda = models.ForeignKey(
        "vendas.PedidoVenda",
        related_name="venda_nfe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    emit_saida = models.ForeignKey(
        "cadastro.Empresa",
        related_name="emit_nfe_saida",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    dest_saida = models.ForeignKey(
        "cadastro.Cliente",
        related_name="dest_nfe_saida",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # Cobranca Fatura(NF-e)
    n_fat = models.CharField(max_length=60, null=True, blank=True, unique=True)
    v_orig = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
    )
    v_desc = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
    )
    v_liq = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        null=True,
        blank=True,
    )
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
        return ""

    def get_emit_cmun(self):
        if self.emit_saida:
            if self.emit_saida.endereco_padrao:
                return self.emit_saida.endereco_padrao.cmun
        return ""

    def __unicode__(self):
        s = f"Série {self.serie},  Nº {self.n_nf_saida}, Chave {self.chave}"
        return s

    def __str__(self):
        s = f"Série {self.serie},  Nº {self.n_nf_saida}, Chave {self.chave}"
        return s


class NotaFiscalEntrada(NotaFiscal):
    n_nf_entrada = models.CharField(
        max_length=9, validators=[RegexValidator(r"^\d{1,10}$")]
    )
    compra = models.ForeignKey(
        "compras.PedidoCompra",
        related_name="compra_nfe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    emit_entrada = models.ForeignKey(
        "cadastro.Fornecedor",
        related_name="emit_nfe_entrada",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    dest_entrada = models.ForeignKey(
        "cadastro.Empresa",
        related_name="dest_nfe_entrada",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Nota Fiscal de Fornecedor"

    @property
    def estado(self):
        if self.emit_entrada:
            if self.emit_entrada.endereco_padrao:
                return self.emit_entrada.endereco_padrao.uf
        return ""

    def __unicode__(self):
        s = "Série {},  Nº {}, Chave {}".format(
            self.serie, self.n_nf_entrada, self.chave
        )
        return s

    def __str__(self):
        s = "Série {},  Nº {}, Chave {}".format(
            self.serie, self.n_nf_entrada, self.chave
        )
        return s


class AutXML(models.Model):
    nfe = models.ForeignKey(
        "fiscal.NotaFiscalSaida", related_name="aut_xml", on_delete=models.CASCADE
    )
    cpf_cnpj = models.CharField(max_length=32, null=True, blank=True)

    def get_cpf_cnpj_apenas_digitos(self):
        return re.sub("[./-]", "", self.cpf_cnpj)


class ConfiguracaoNotaFiscal(models.Model):
    arquivo_certificado_a1 = models.FileField(
        upload_to="arquivos/certificado/", null=True, blank=True
    )
    senha_certificado = models.CharField(max_length=255, null=True, blank=True)
    serie_atual = models.CharField(max_length=3, default="101")
    ambiente = models.CharField(max_length=1, choices=TP_AMB_ESCOLHAS, default="2")
    imp_danfe = models.CharField(max_length=1, choices=TP_IMP_ESCOLHAS, default="1")

    inserir_logo_danfe = models.BooleanField(default=True)
    orientacao_logo_danfe = models.CharField(
        max_length=1, choices=ORIENTACAO_LOGO_DANFE, default="H"
    )

    csc = models.CharField(max_length=64, null=True, blank=True)
    cidtoken = models.CharField(max_length=8, null=True, blank=True)

    class Meta:
        default_permissions = ()
        verbose_name = "Configuração NF-e"
        permissions = (("configurar_nfe", "Pode modificar configuração de NF-e"),)

    @property
    def leiaute_logo_vertical(self):
        if self.orientacao_logo_danfe == "H":
            return False
        else:
            return True

    def get_certificado_a1(self):
        return os.path.join(MEDIA_ROOT, self.arquivo_certificado_a1.name)


class ErrosValidacaoNotaFiscal(models.Model):
    nfe = models.ForeignKey(
        "fiscal.NotaFiscalSaida", related_name="erros_nfe", on_delete=models.CASCADE
    )
    tipo = models.CharField(
        max_length=1, choices=ERROS_NFE_TIPOS, null=True, blank=True
    )
    descricao = models.CharField(max_length=255, null=True, blank=True)


class RespostaSefazNotaFiscal(models.Model):
    nfe = models.ForeignKey(
        "fiscal.NotaFiscalSaida",
        related_name="erros_nfe_sefaz",
        on_delete=models.CASCADE,
    )
    tipo = models.CharField(
        max_length=1, choices=RETORNO_SEFAZ_TIPOS, null=True, blank=True
    )
    codigo = models.CharField(max_length=3, null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
