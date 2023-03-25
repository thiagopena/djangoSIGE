from django.db import models

TP_OPERACAO_OPCOES = (
    ("0", "0 - Entrada"),
    ("1", "1 - Saída"),
)

ID_DEST_OPCOES = (
    ("1", "1 - Operação interna"),
    ("2", "2 - Operação interestadual"),
    ("3", "3 - Operação com exterior"),
)


class NaturezaOperacao(models.Model):
    cfop = models.CharField(max_length=5)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    tp_operacao = models.CharField(
        max_length=1, choices=TP_OPERACAO_OPCOES, null=True, blank=True
    )
    id_dest = models.CharField(
        max_length=1, choices=ID_DEST_OPCOES, null=True, blank=True
    )

    class Meta:
        verbose_name = "Natureza da Operação"

    def set_values_by_cfop(self):
        if self.cfop:
            if self.cfop[0] == "1":
                self.tp_operacao = "0"
                self.id_dest = "1"
            elif self.cfop[0] == "2":
                self.tp_operacao = "0"
                self.id_dest = "2"
            elif self.cfop[0] == "3":
                self.tp_operacao = "0"
                self.id_dest = "3"
            elif self.cfop[0] == "4":
                self.tp_operacao = "1"
                self.id_dest = "1"
            elif self.cfop[0] == "5":
                self.tp_operacao = "1"
                self.id_dest = "2"
            elif self.cfop[0] == "6":
                self.tp_operacao = "1"
                self.id_dest = "3"

    def __unicode__(self):
        if self.descricao:
            s = f"{self.cfop} - {self.descricao}"
        else:
            s = "%s" % (self.cfop)
        return s

    def __str__(self):
        if self.descricao:
            s = f"{self.cfop} - {self.descricao}"
        else:
            s = "%s" % (self.cfop)
        return s
