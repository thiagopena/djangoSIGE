# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.contrib import messages

from djangosige.apps.base.custom_views import CustomListView

from djangosige.apps.financeiro.models import MovimentoCaixa

from datetime import datetime


class FluxoCaixaView(CustomListView):
    template_name = "financeiro/fluxo_de_caixa/fluxo.html"
    success_url = reverse_lazy('djangosige.apps.financeiro:fluxodecaixaview')
    context_object_name = 'movimentos'
    permission_codename = 'acesso_fluxodecaixa'

    def get_queryset(self):
        try:
            data_inicial = self.request.GET.get('from')
            data_final = self.request.GET.get('to')

            if data_inicial and data_final:
                data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y')
                data_final = datetime.strptime(data_final, '%d/%m/%Y')
            elif data_inicial:
                data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y')
                data_final = data_inicial
            elif data_final:
                data_final = datetime.strptime(data_final, '%d/%m/%Y')
                data_inicial = data_final
            else:
                data_final = data_inicial = datetime.today().strftime('%Y-%m-%d')

        except ValueError:
            data_final = data_inicial = datetime.today().strftime('%Y-%m-%d')
            messages.error(
                self.request, 'Formato de data incorreto, deve ser no formato DD/MM/AAAA')

        return MovimentoCaixa.objects.filter(data_movimento__range=(data_inicial, data_final))
