# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse

from djangosige.apps.base.custom_views import CustomView, CustomCreateView, CustomListView, CustomUpdateView, CustomTemplateView
from djangosige.apps.base.views_mixins import FormValidationMessageMixin

from djangosige.apps.fiscal.forms import NotaFiscalSaidaForm, NotaFiscalEntradaForm, AutXMLFormSet, ConfiguracaoNotaFiscalForm, EmissaoNotaFiscalForm, CancelamentoNotaFiscalForm, \
    ConsultarCadastroForm, InutilizarNotasForm, ConsultarNotaForm, BaixarNotaForm, ManifestacaoDestinatarioForm
from djangosige.apps.fiscal.models import NotaFiscalSaida, NotaFiscalEntrada, NotaFiscal, ConfiguracaoNotaFiscal, AutXML, ErrosValidacaoNotaFiscal, RespostaSefazNotaFiscal
from djangosige.apps.cadastro.models import MinhaEmpresa
from djangosige.apps.login.models import Usuario
from djangosige.apps.vendas.models import PedidoVenda, ItensVenda

try:
    from .processador_nf import ProcessadorNotaFiscal
except ImportError:
    pass

from decimal import Decimal
from datetime import datetime


class NotaFiscalViewMixin(object):

    def atualizar_campos(self, post_data):
        values_dict = {}
        itens_id = []
        decimal_fields = ['vq_bcpis', 'vq_bccofins',
                          'vpis', 'vcofins', 'vicms_deson', ]
        string_fields = ['inf_ad_prod', ]

        for key, value in post_data.items():
            if key == 'pk_item':
                itens_id.append(value)
            if key.startswith('editable_field_'):
                values_dict[key] = value

        for id in itens_id:
            item = ItensVenda.objects.get(pk=id)
            for key, value in values_dict.items():
                if value:
                    for dfield in decimal_fields:
                        if key.endswith(dfield + '_' + str(id)):
                            setattr(item, dfield, Decimal(
                                value.replace(',', '.')))

                    for sfield in string_fields:
                        if key.endswith(sfield + '_' + str(id)):
                            setattr(item, sfield, value)

            item.save()


class AdicionarNotaFiscalView(CustomCreateView, NotaFiscalViewMixin):

    def get_context_data(self, **kwargs):
        context = super(AdicionarNotaFiscalView,
                        self).get_context_data(**kwargs)
        return self.view_context(context)

    def get_success_message(self, cleaned_data):
        if isinstance(self.object, NotaFiscalSaida):
            return self.success_message % dict(cleaned_data, n_nf=self.object.n_nf_saida)
        else:
            return self.success_message % dict(cleaned_data, n_nf=self.object.n_nf_entrada)

    def get(self, request, form_class, *args, **kwargs):
        self.object = None

        form = self.get_form(form_class)
        form = self.set_form_initial_data(form, request.user)

        aut_form = AutXMLFormSet(prefix='aut_form')

        return self.render_to_response(self.get_context_data(form=form, aut_form=aut_form,))

    def post(self, request, form_class, *args, **kwargs):
        self.object = None

        # Remover separados de milhar .
        req_post = request.POST.copy()
        for key in req_post:
            if ('v_' in key):
                req_post[key] = req_post[key].replace('.', '')
        request.POST = req_post

        form = self.get_form(form_class)
        aut_form = AutXMLFormSet(request.POST, prefix='aut_form')

        if (form.is_valid() and aut_form.is_valid()):
            self.object = form.save(commit=False)
            if isinstance(self.object, NotaFiscalSaida):
                self.atualizar_campos(request.POST)
            self.object.save()

            return self.form_valid(form)

        return self.form_invalid(form=form, aut_form=aut_form)


class AdicionarNotaFiscalSaidaView(AdicionarNotaFiscalView):
    form_class = NotaFiscalSaidaForm
    template_name = "fiscal/nota_fiscal/nota_fiscal_add.html"
    success_url = reverse_lazy('djangosige.apps.fiscal:listanotafiscalsaidaview')
    success_message = "Nota fiscal N°<b>%(n_nf)s </b>gerada com sucesso."
    permission_codename = 'add_notafiscalsaida'

    def view_context(self, context):
        context['title_complete'] = 'GERAR NOTA FISCAL'
        context['return_url'] = reverse_lazy('djangosige.apps.fiscal:listanotafiscalsaidaview')
        context['saida'] = True
        return context

    def set_form_initial_data(self, form, user):
        form.initial['dhemi'] = datetime.now().strftime("%d/%m/%Y %H:%M")

        try:
            form.initial['emit_saida'] = MinhaEmpresa.objects.get(
                m_usuario=Usuario.objects.get(user=user)).m_empresa
        except:
            pass

        try:
            conf_nfe = ConfiguracaoNotaFiscal.objects.all()[:1].get()
        except ConfiguracaoNotaFiscal.DoesNotExist:
            conf_nfe = ConfiguracaoNotaFiscal.objects.create()

        form.initial['serie'] = conf_nfe.serie_atual
        form.initial['tp_amb'] = conf_nfe.ambiente
        form.initial['tp_imp'] = conf_nfe.imp_danfe
        form.initial['status_nfe'] = u'3'

        try:
            nnfe_max = NotaFiscalSaida.objects.latest('n_nf_saida').n_nf_saida
            nnfe_max = int(nnfe_max) + 1
        except NotaFiscalSaida.DoesNotExist:
            nnfe_max = 1

        form.initial['n_nf_saida'] = nnfe_max

        return form

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarNotaFiscalSaidaView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarNotaFiscalSaidaView, self).post(request, form_class, *args, **kwargs)


class NotaFiscalListView(CustomListView, NotaFiscalViewMixin):

    def get_context_data(self, **kwargs):
        context = super(NotaFiscalListView, self).get_context_data(**kwargs)
        return self.view_context(context)


class NotaFiscalSaidaListView(NotaFiscalListView):
    template_name = 'fiscal/nota_fiscal/nota_fiscal_list.html'
    model = NotaFiscalSaida
    context_object_name = 'all_notas'
    success_url = reverse_lazy('djangosige.apps.fiscal:listanotafiscalsaidaview')
    permission_codename = 'view_notafiscalsaida'

    def view_context(self, context):
        context['title_complete'] = 'NOTAS FISCAIS'
        context['add_url'] = reverse_lazy('djangosige.apps.fiscal:addnotafiscalsaidaview')
        context['importar_nota_url'] = reverse_lazy(
            'djangosige.apps.fiscal:importarnotafiscalsaida')
        context['saida'] = True
        return context


class NotaFiscalEntradaListView(NotaFiscalListView):
    template_name = 'fiscal/nota_fiscal/nota_fiscal_list.html'
    model = NotaFiscalEntrada
    context_object_name = 'all_notas'
    success_url = reverse_lazy('djangosige.apps.fiscal:listanotafiscalentradaview')
    permission_codename = 'view_notafiscalentrada'

    def view_context(self, context):
        context[
            'title_complete'] = 'NOTAS FISCAIS DE FORNECEDORES (ENTRADA DE MATERIAL)'
        context['add_url'] = reverse_lazy('djangosige.apps.fiscal:addnotafiscalentradaview')
        context['importar_nota_url'] = reverse_lazy(
            'djangosige.apps.fiscal:importarnotafiscalentrada')
        context['entrada'] = True
        return context


class EditarNotaFiscalView(CustomUpdateView, NotaFiscalViewMixin):

    def get_context_data(self, **kwargs):
        context = super(EditarNotaFiscalView, self).get_context_data(**kwargs)
        context['edit_nfe'] = True
        return self.view_context(context)

    def get_success_message(self, cleaned_data):
        if isinstance(self.object, NotaFiscalSaida):
            return self.success_message % dict(cleaned_data, n_nf=self.object.n_nf_saida)
        else:
            return self.success_message % dict(cleaned_data, n_nf=self.object.n_nf_entrada)


class EditarNotaFiscalSaidaView(EditarNotaFiscalView):
    form_class = NotaFiscalSaidaForm
    model = NotaFiscalSaida
    template_name = "fiscal/nota_fiscal/nota_fiscal_edit.html"
    success_url = reverse_lazy('djangosige.apps.fiscal:listanotafiscalsaidaview')
    success_message = "Nota fiscal N°<b>%(n_nf)s </b>editada com sucesso."
    permission_codename = 'change_notafiscalsaida'

    def view_context(self, context):
        context['title_complete'] = 'EDITAR NOTA FISCAL DE SAÍDA ' + \
            str(self.object.serie) + '/' + str(self.object.n_nf_saida)
        context['return_url'] = reverse_lazy('djangosige.apps.fiscal:listanotafiscalsaidaview')
        context['saida'] = True
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        aut_form = AutXMLFormSet(instance=self.object, prefix='aut_form')

        if AutXML.objects.filter(nfe=self.object.pk).count():
            aut_form.extra = 0

        errors_validacao = ErrosValidacaoNotaFiscal.objects.filter(
            nfe=self.object)
        resposta_sefaz = RespostaSefazNotaFiscal.objects.filter(
            nfe=self.object)

        return self.render_to_response(self.get_context_data(form=form, aut_form=aut_form, errors_validacao=errors_validacao, resposta_sefaz=resposta_sefaz,))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()

        # Remover separados de milhar .
        req_post = request.POST.copy()
        req_post['v_orig'] = req_post['v_orig'].replace('.', '')
        req_post['v_desc'] = req_post['v_desc'].replace('.', '')
        req_post['v_liq'] = req_post['v_liq'].replace('.', '')
        request.POST = req_post

        form = form_class(request.POST, request.FILES, instance=self.object)
        aut_form = AutXMLFormSet(
            request.POST, prefix='aut_form', instance=self.object)

        if (form.is_valid() and aut_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.status_nfe = u'3'
            self.atualizar_campos(request.POST)
            self.object.save()

            return self.form_valid(form)

        return self.form_invalid(form=form, aut_form=aut_form)

    def form_invalid(self, form, aut_form):
        errors_validacao = ErrosValidacaoNotaFiscal.objects.filter(
            nfe=self.object)
        resposta_sefaz = RespostaSefazNotaFiscal.objects.filter(
            nfe=self.object)
        return self.render_to_response(self.get_context_data(form=form, aut_form=aut_form, errors_validacao=errors_validacao, resposta_sefaz=resposta_sefaz,))


class EditarNotaFiscalEntradaView(EditarNotaFiscalView):
    form_class = NotaFiscalEntradaForm
    model = NotaFiscalEntrada
    template_name = "fiscal/nota_fiscal/nota_fiscal_edit.html"
    success_url = reverse_lazy('djangosige.apps.fiscal:listanotafiscalentradaview')
    success_message = "Nota fiscal N°<b>%(n_nf)s </b>editada com sucesso."
    permission_codename = 'change_notafiscalentrada'

    def view_context(self, context):
        context['title_complete'] = 'EDITAR NOTA FISCAL DE ENTRADA ' + \
            str(self.object.serie) + '/' + str(self.object.n_nf_entrada)
        context['return_url'] = reverse_lazy(
            'djangosige.apps.fiscal:listanotafiscalentradaview')
        context['entrada'] = True
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form,))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()

        form = form_class(request.POST, instance=self.object)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()

            return self.form_valid(form)

        return self.form_invalid(form=form)


# Gerar nota fiscal a partir de um pedido de venda
class GerarNotaFiscalSaidaView(CustomView):
    permission_codename = ['add_notafiscalsaida', 'change_notafiscalsaida']

    def get(self, request, *args, **kwargs):
        pedido_id = kwargs.get('pk', None)
        pedido = PedidoVenda.objects.get(id=pedido_id)

        nova_nota = NotaFiscalSaida()

        nova_nota.tpnf = u'1'  # Saida

        try:
            conf_nfe = ConfiguracaoNotaFiscal.objects.all()[:1].get()
        except ConfiguracaoNotaFiscal.DoesNotExist:
            conf_nfe = ConfiguracaoNotaFiscal.objects.create()

        nova_nota.serie = conf_nfe.serie_atual
        nova_nota.tp_amb = conf_nfe.ambiente
        nova_nota.tp_imp = conf_nfe.imp_danfe
        nova_nota.status_nfe = u'3'
        nova_nota.dhemi = datetime.now().strftime("%Y-%m-%d %H:%M")

        if pedido.ind_final:
            nova_nota.ind_final = u'1'
            nova_nota.mod = u'65'

        if pedido.cond_pagamento:
            if pedido.cond_pagamento.n_parcelas > 1:
                nova_nota.indpag = u'1'
            else:
                nova_nota.indpag = u'0'
        else:
            nova_nota.indpag = u'2'

        nova_nota.venda = pedido

        try:
            nnfe_max = NotaFiscalSaida.objects.latest('n_nf_saida').n_nf_saida
            nnfe_max = int(nnfe_max) + 1
        except NotaFiscal.DoesNotExist:
            nnfe_max = 1

        nova_nota.n_nf_saida = nnfe_max

        try:
            nova_nota.emit_saida = MinhaEmpresa.objects.get(
                m_usuario=Usuario.objects.get(user=request.user)).m_empresa
        except:
            pass

        nova_nota.dest_saida = pedido.cliente
        nova_nota.save()

        return redirect(reverse_lazy('djangosige.apps.fiscal:editarnotafiscalsaidaview', kwargs={'pk': nova_nota.id}))


class ConfiguracaoNotaFiscalView(FormValidationMessageMixin, CustomTemplateView):
    template_name = 'fiscal/nota_fiscal/nota_fiscal_config.html'
    success_url = reverse_lazy('djangosige.apps.fiscal:configuracaonotafiscal')
    success_message = "Emissão de NF-e configurada"
    permission_codename = 'configurar_nfe'

    def get_context_data(self, **kwargs):
        context = super(ConfiguracaoNotaFiscalView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONFIGURAÇÃO DE EMISSÃO DE NOTAS FISCAIS'
        return context

    def get_object(self):
        try:
            conf_nfe = ConfiguracaoNotaFiscal.objects.all()[:1].get()
        except ConfiguracaoNotaFiscal.DoesNotExist:
            conf_nfe = ConfiguracaoNotaFiscal.objects.create()

        return conf_nfe

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ConfiguracaoNotaFiscalForm(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, object=self.object,))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ConfiguracaoNotaFiscalForm(
            request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, object=self.object,))


class ValidarNotaView(CustomView):
    permission_codename = 'change_notafiscalsaida'

    def get(self, request, *args, **kwargs):
        processador_nota = ProcessadorNotaFiscal()
        nfe_id = kwargs.get('pk', None)
        nota_obj = NotaFiscalSaida.objects.get(id=nfe_id)
        processador_nota.validar_nota(nota_obj)

        if processador_nota.erro:
            messages.error(self.request, processador_nota.message)
        else:
            messages.success(self.request, processador_nota.message)

        return redirect(reverse_lazy('djangosige.apps.fiscal:editarnotafiscalsaidaview', kwargs={'pk': nfe_id}))


class EmitirNotaView(CustomTemplateView):
    template_name = 'fiscal/nota_fiscal/nota_fiscal_sefaz.html'
    permission_codename = ['change_notafiscalsaida', 'emitir_notafiscal']

    def emitir_nota(self):
        processador_nota = ProcessadorNotaFiscal()
        processador_nota.emitir_nota(self.object)

        if processador_nota.erro:
            messages.error(self.request, processador_nota.message)
        else:
            messages.success(self.request, processador_nota.message)

        return redirect(reverse_lazy('djangosige.apps.fiscal:editarnotafiscalsaidaview', kwargs={'pk': self.object.id}))

    def get_context_data(self, **kwargs):
        context = super(EmitirNotaView, self).get_context_data(**kwargs)
        context['title_complete'] = 'EMISSÃO DE NOTA FISCAL'
        context['btn_text'] = 'ENVIAR NOTA'
        context['form_id'] = 'emitir_nota_form'
        context['saida'] = True
        context['return_url'] = reverse_lazy(
            'djangosige.apps.fiscal:editarnotafiscalsaidaview', kwargs={'pk': self.object.pk})
        return context

    def get_object(self, pk):
        nota = NotaFiscalSaida.objects.get(pk=pk)
        return nota

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(kwargs['pk'])
        form = EmissaoNotaFiscalForm(instance=self.object)
        form.initial['dhemi'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        return self.render_to_response(self.get_context_data(form=form, object=self.object,))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(kwargs['pk'])
        form = EmissaoNotaFiscalForm(request.POST, instance=self.object)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            self.emitir_nota()
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        return redirect(reverse_lazy('djangosige.apps.fiscal:editarnotafiscalsaidaview', kwargs={'pk': self.object.pk}))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, object=self.object,))


class GerarCopiaNotaView(CustomView):
    permission_codename = ['add_notafiscalsaida', 'change_notafiscalsaida']

    def get(self, request, *args, **kwargs):
        nota_id = kwargs.get('pk', None)

        instance = NotaFiscalSaida.objects.get(id=nota_id)
        redirect_url = 'djangosige.apps.fiscal:editarnotafiscalsaidaview'

        aut_xmls = instance.aut_xml.all()

        instance.pk = None
        instance.id = None
        instance.status_nfe = '3'
        instance.numero_lote = None
        instance.numero_protocolo = None

        try:
            nnfe_max = NotaFiscalSaida.objects.latest('n_nf_saida').n_nf_saida
            nnfe_max = int(nnfe_max) + 1
        except NotaFiscal.DoesNotExist:
            nnfe_max = 1

        instance.n_nf_saida = nnfe_max
        instance.n_fat = None
        instance.save()

        for aut in aut_xmls:
            aut.pk = None
            aut.id = None
            aut.save()
            instance.aut_xml.add(aut)

        return redirect(reverse_lazy(redirect_url, kwargs={'pk': instance.id}))


class ImportarNotaView(CustomView):

    def post(self, request, *args, **kwargs):
        if len(request.FILES):
            processador_nota = ProcessadorNotaFiscal()
            try:
                processador_nota.importar_xml(request)
            except Exception as e:
                messages.error(
                    request, 'O seguinte erro foi encontrado ao tentar ler o arquivo XML: ' + str(e))
        else:
            messages.error(request, 'Arquivo XML não selecionado.')

        return self.get_redirect_url()


class ImportarNotaSaidaView(ImportarNotaView):
    permission_codename = ['add_notafiscalsaida',
                           'view_notafiscalsaida', 'change_notafiscalsaida']

    def get_redirect_url(self):
        return redirect(reverse_lazy('djangosige.apps.fiscal:listanotafiscalsaidaview'))


class ImportarNotaEntradaView(ImportarNotaView):
    permission_codename = ['add_notafiscalentrada',
                           'view_notafiscalentrada', 'change_notafiscalentrada']

    def get_redirect_url(self):
        return redirect(reverse_lazy('djangosige.apps.fiscal:listanotafiscalentradaview'))


class CancelarNotaView(CustomTemplateView):
    template_name = 'fiscal/nota_fiscal/nota_fiscal_sefaz.html'
    permission_codename = ['view_notafiscalsaida',
                           'change_notafiscalsaida', 'cancelar_notafiscal']

    def cancelar_nota(self):
        processador_nota = ProcessadorNotaFiscal()
        processador_nota.cancelar_nota(self.object)

        if processador_nota.erro:
            messages.error(self.request, processador_nota.message)
        else:
            messages.success(self.request, processador_nota.message)

        return redirect(reverse_lazy('djangosige.apps.fiscal:editarnotafiscalsaidaview', kwargs={'pk': self.object.id}))

    def get_context_data(self, **kwargs):
        context = super(CancelarNotaView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CANCELAMENTO DE NOTA FISCAL'
        context['btn_text'] = 'CANCELAR NOTA'
        context['form_id'] = 'cancelar_nota_form'
        context['saida'] = True
        context['return_url'] = reverse_lazy(
            'djangosige.apps.fiscal:editarnotafiscalsaidaview', kwargs={'pk': self.object.pk})
        return context

    def get_object(self, pk):
        nota = NotaFiscalSaida.objects.get(pk=pk)
        return nota

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(kwargs['pk'])
        form = CancelamentoNotaFiscalForm(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, object=self.object,))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(kwargs['pk'])
        form = CancelamentoNotaFiscalForm(request.POST, instance=self.object)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            self.cancelar_nota()
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        return redirect(reverse_lazy('djangosige.apps.fiscal:editarnotafiscalsaidaview', kwargs={'pk': self.object.pk}))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, object=self.object,))


class GerarDanfeView(CustomView):
    permission_codename = ['view_notafiscalsaida',
                           'change_notafiscalsaida', 'gerar_danfe']

    def get(self, request, *args, **kwargs):
        nota_id = kwargs.get('pk', None)
        nota_obj = NotaFiscalSaida.objects.get(pk=nota_id)

        resp = HttpResponse(content_type='application/pdf')

        processador_nota = ProcessadorNotaFiscal()
        danfe_pdf = processador_nota.gerar_danfe(nota_obj)

        if processador_nota.erro:
            messages.error(self.request, processador_nota.message)
            return redirect(reverse_lazy('djangosige.apps.fiscal:editarnotafiscalsaidaview', kwargs={'pk': nota_obj.id}))
        else:
            messages.success(self.request, processador_nota.message)
            resp.write(danfe_pdf)
            return resp


class GerarDanfceView(CustomView):
    permission_codename = ['view_notafiscalsaida',
                           'change_notafiscalsaida', 'gerar_danfe']

    def get(self, request, *args, **kwargs):
        nota_id = kwargs.get('pk', None)
        nota_obj = NotaFiscalSaida.objects.get(pk=nota_id)

        resp = HttpResponse(content_type='application/pdf')

        processador_nota = ProcessadorNotaFiscal()
        danfce_pdf = processador_nota.gerar_danfce(nota_obj)

        if processador_nota.erro:
            messages.error(self.request, processador_nota.message)
            return redirect(reverse_lazy('djangosige.apps.fiscal:editarnotafiscalsaidaview', kwargs={'pk': nota_obj.id}))
        else:
            messages.success(self.request, processador_nota.message)
            resp.write(danfce_pdf)
            return resp


class ConsultarCadastroView(CustomTemplateView):
    template_name = 'fiscal/nota_fiscal/nota_fiscal_sefaz.html'
    permission_codename = ['view_notafiscalsaida', 'consultar_cadastro']

    def consultar_cadastro(self, empresa, salvar_arquivos):
        processador_nota = ProcessadorNotaFiscal()
        processador_nota.consultar_cadastro(empresa, salvar_arquivos)

        if processador_nota.erro:
            messages.error(self.request, processador_nota.message)
        else:
            messages.success(self.request, processador_nota.message)

        return processador_nota.processo

    def get_context_data(self, **kwargs):
        context = super(ConsultarCadastroView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CONSULTAR CADASTRO'
        context['btn_text'] = 'CONSULTAR'
        context['form_id'] = 'consultar_cadastro_form'
        context['saida'] = True
        context['return_url'] = reverse_lazy('djangosige.apps.fiscal:listanotafiscalsaidaview')
        return context

    def get(self, request, *args, **kwargs):
        form = ConsultarCadastroForm()
        return self.render_to_response(self.get_context_data(form=form,))

    def post(self, request, *args, **kwargs):
        form = ConsultarCadastroForm(request.POST)

        if form.is_valid():
            empresa = form.cleaned_data['empresa']
            salvar_arquivos = form.cleaned_data['salvar_arquivos']
            processo = self.consultar_cadastro(empresa, salvar_arquivos)
            return self.form_valid(form, processo)

        return self.form_invalid(form)

    def form_valid(self, form, processo):
        return self.render_to_response(self.get_context_data(form=form, processo=processo,))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,))


class InutilizarNotasView(CustomTemplateView):
    template_name = 'fiscal/nota_fiscal/nota_fiscal_sefaz.html'
    permission_codename = ['view_notafiscalsaida',
                           'change_notafiscalsaida', 'inutilizar_notafiscal']

    def inutilizar_notas(self, empresa, ambiente, modelo, serie, numero_inicial, numero_final, justificativa, salvar_arquivos):
        processador_nota = ProcessadorNotaFiscal()
        processador_nota.inutilizar_notas(
            empresa, ambiente, modelo, serie, numero_inicial, numero_final, justificativa, salvar_arquivos)

        if processador_nota.erro:
            messages.error(self.request, processador_nota.message)
        else:
            messages.success(self.request, processador_nota.message)

        return processador_nota.processo

    def get_context_data(self, **kwargs):
        context = super(InutilizarNotasView, self).get_context_data(**kwargs)
        context['title_complete'] = 'INUTILIZAR NOTAS'
        context['btn_text'] = 'ENVIAR'
        context['form_id'] = 'inutilizar_notas_form'
        context['saida'] = True
        context['return_url'] = reverse_lazy('djangosige.apps.fiscal:listanotafiscalsaidaview')
        return context

    def get(self, request, *args, **kwargs):
        form = InutilizarNotasForm()
        return self.render_to_response(self.get_context_data(form=form,))

    def post(self, request, *args, **kwargs):
        form = InutilizarNotasForm(request.POST)

        if form.is_valid():
            empresa = form.cleaned_data['empresa']
            ambiente = form.cleaned_data['ambiente']
            modelo = form.cleaned_data['modelo']
            serie = form.cleaned_data['serie']
            numero_inicial = form.cleaned_data['numero_inicial']
            numero_final = form.cleaned_data['numero_final']
            justificativa = form.cleaned_data['justificativa']
            salvar_arquivos = form.cleaned_data['salvar_arquivos']

            processo = self.inutilizar_notas(
                empresa, ambiente, modelo, serie, numero_inicial, numero_final, justificativa, salvar_arquivos)
            return self.form_valid(form, processo)

        return self.form_invalid(form)

    def form_valid(self, form, processo):
        return self.render_to_response(self.get_context_data(form=form, processo=processo,))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,))


class ConsultarNotaView(CustomTemplateView):
    template_name = 'fiscal/nota_fiscal/nota_fiscal_sefaz.html'
    permission_codename = ['view_notafiscalsaida',
                           'change_notafiscalsaida', 'consultar_notafiscal']

    def consultar_nota(self, chave, ambiente, salvar_arquivos):
        processador_nota = ProcessadorNotaFiscal()
        processador_nota.consultar_nota(chave, ambiente, salvar_arquivos)

        if processador_nota.erro:
            messages.error(self.request, processador_nota.message)
        else:
            messages.success(self.request, processador_nota.message)

        return processador_nota.processo

    def get_context_data(self, **kwargs):
        context = super(ConsultarNotaView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CONSULTAR NOTA'
        context['btn_text'] = 'ENVIAR'
        context['form_id'] = 'consultar_nota_form'
        context['saida'] = True
        context['return_url'] = reverse_lazy('djangosige.apps.fiscal:listanotafiscalsaidaview')
        return context

    def get(self, request, *args, **kwargs):
        form = ConsultarNotaForm()
        form.initial['nota'] = kwargs.get('pk', None)

        return self.render_to_response(self.get_context_data(form=form,))

    def post(self, request, *args, **kwargs):
        form = ConsultarNotaForm(request.POST)

        if form.is_valid():
            nota = form.cleaned_data['nota']
            chave = form.cleaned_data['chave']
            ambiente = form.cleaned_data['ambiente']
            salvar_arquivos = form.cleaned_data['salvar_arquivos']

            if chave and nota:
                messages.error(
                    self.request, 'Preencha apenas um dos campos (Consultar nota da base de dados ou por chave).')
                return self.form_invalid(form)
            elif not chave and not nota:
                messages.error(
                    self.request, 'Preencha ao menos um dos campos: \'Selecionar nota da base de dados\' ou \'Chave da nota\'.')
                return self.form_invalid(form)
            elif nota:
                chave = nota.chave

            processo = self.consultar_nota(chave, ambiente, salvar_arquivos)
            return self.form_valid(form, processo)

        return self.form_invalid(form)

    def form_valid(self, form, processo):
        return self.render_to_response(self.get_context_data(form=form, processo=processo,))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,))


class BaixarNotaView(CustomTemplateView):
    template_name = 'fiscal/nota_fiscal/nota_fiscal_sefaz.html'
    permission_codename = ['view_notafiscalsaida',
                           'change_notafiscalsaida', 'baixar_notafiscal']

    def baixar_nota(self, chave, ambiente, ambiente_nacional, salvar_arquivos):
        processador_nota = ProcessadorNotaFiscal()
        processador_nota.baixar_nota(
            chave, ambiente, ambiente_nacional, salvar_arquivos)

        if processador_nota.erro:
            messages.error(self.request, processador_nota.message)
        else:
            messages.success(self.request, processador_nota.message)

        return processador_nota.processo

    def get_context_data(self, **kwargs):
        context = super(BaixarNotaView, self).get_context_data(**kwargs)
        context['title_complete'] = 'BAIXAR NOTA'
        context['btn_text'] = 'ENVIAR'
        context['form_id'] = 'baixar_nota_form'
        context['saida'] = True
        context['return_url'] = reverse_lazy('djangosige.apps.fiscal:listanotafiscalsaidaview')
        return context

    def get(self, request, *args, **kwargs):
        form = BaixarNotaForm()
        form.initial['nota'] = kwargs.get('pk', None)

        return self.render_to_response(self.get_context_data(form=form,))

    def post(self, request, *args, **kwargs):
        form = BaixarNotaForm(request.POST)

        if form.is_valid():
            nota = form.cleaned_data['nota']
            chave = form.cleaned_data['chave']
            ambiente = form.cleaned_data['ambiente']
            ambiente_nacional = form.cleaned_data['ambiente_nacional']
            salvar_arquivos = form.cleaned_data['salvar_arquivos']

            if chave and nota:
                messages.error(
                    self.request, 'Preencha apenas um dos campos (Baixar nota da base de dados ou por chave).')
                return self.form_invalid(form)
            elif not chave and not nota:
                messages.error(
                    self.request, 'Preencha ao menos um dos campos: \'Selecionar nota da base de dados\' ou \'Chave da nota\'.')
                return self.form_invalid(form)
            elif nota:
                chave = nota.chave

            processo = self.baixar_nota(
                chave, ambiente, ambiente_nacional, salvar_arquivos)
            return self.form_valid(form, processo)

        return self.form_invalid(form)

    def form_valid(self, form, processo):
        return self.render_to_response(self.get_context_data(form=form, processo=processo,))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,))


class ManifestacaoDestinatarioView(CustomTemplateView):
    template_name = 'fiscal/nota_fiscal/nota_fiscal_sefaz.html'
    permission_codename = ['view_notafiscalsaida', 'manifestacao_destinatario']

    def efetuar_manifesto(self, chave, cnpj, ambiente, tipo_manifesto, justificativa, ambiente_nacional, salvar_arquivos):
        processador_nota = ProcessadorNotaFiscal()
        processador_nota.efetuar_manifesto(
            chave, cnpj, ambiente, tipo_manifesto, justificativa, ambiente_nacional, salvar_arquivos)

        if processador_nota.erro:
            messages.error(self.request, processador_nota.message)
        else:
            messages.success(self.request, processador_nota.message)

        return processador_nota.processo

    def get_context_data(self, **kwargs):
        context = super(ManifestacaoDestinatarioView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'MANIFESTAÇÃO DO DESTINATÁRIO'
        context['btn_text'] = 'ENVIAR'
        context['form_id'] = 'manifestacao_destinatario_form'
        context['saida'] = True
        context['return_url'] = reverse_lazy('djangosige.apps.fiscal:listanotafiscalsaidaview')
        return context

    def get(self, request, *args, **kwargs):
        form = ManifestacaoDestinatarioForm()
        return self.render_to_response(self.get_context_data(form=form,))

    def post(self, request, *args, **kwargs):
        form = ManifestacaoDestinatarioForm(request.POST)

        if form.is_valid():
            nota = form.cleaned_data['nota']
            cnpj = form.cleaned_data['cnpj']
            chave = form.cleaned_data['chave']
            ambiente = form.cleaned_data['ambiente']
            justificativa = form.cleaned_data['justificativa']
            ambiente_nacional = form.cleaned_data['ambiente_nacional']
            tipo_manifesto = form.cleaned_data['tipo_manifesto']
            salvar_arquivos = form.cleaned_data['salvar_arquivos']

            if tipo_manifesto == '210240' and not justificativa:
                messages.error(
                    self.request, 'Justificativa é obrigatória para manifestação de evento: \'Operação não Realizada\'')
                return self.form_invalid(form)

            if chave and nota:
                messages.error(
                    self.request, 'Preencha apenas um dos campos (Baixar nota da base de dados ou por chave).')
                return self.form_invalid(form)
            elif not chave and not nota:
                messages.error(
                    self.request, 'Preencha ao menos um dos campos: \'Selecionar nota da base de dados\' ou \'Chave da nota\'.')
                return self.form_invalid(form)
            elif nota:
                chave = nota.chave

            processo = self.efetuar_manifesto(
                chave, cnpj, ambiente, tipo_manifesto, justificativa, ambiente_nacional, salvar_arquivos)
            return self.form_valid(form, processo)

        return self.form_invalid(form)

    def form_valid(self, form, processo):
        return self.render_to_response(self.get_context_data(form=form, processo=processo,))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,))
