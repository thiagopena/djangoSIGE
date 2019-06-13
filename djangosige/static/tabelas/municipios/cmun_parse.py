# -*- coding: utf-8 -*-

import csv
import codecs

import unicodedata
import re

"""
A remoção de acentos foi baseada em uma resposta no Stack Overflow.
http://stackoverflow.com/a/517974/3464573
"""


def removerAcentosECaracteresEspeciais(palavra):

    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join(
        [c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras
    # e espaço
    return re.sub(r"[^a-zA-Z0-9 \\\]", '', palavraSemAcento)


if __name__ == "__main__":
    f = open('codigos_municipios.csv', encoding="utf8")
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        row_list = row[0].split(';')
        estado = row_list[1]
        line = row_list[2] + ',' + \
            removerAcentosECaracteresEspeciais(row_list[3]).title() + '\n'
        f = codecs.open(estado + '.csv', 'a', 'utf-8')
        f.write(line)
        f.close()
