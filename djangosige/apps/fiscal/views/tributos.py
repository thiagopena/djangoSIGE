# -*- coding: utf-8 -*-

from django.urls import reverse_lazy

from djangosige.apps.base.custom_views import CustomCreateView, CustomListView, CustomUpdateView

from djangosige.apps.fiscal.forms import GrupoFiscalForm, ICMSForm, ICMSSNForm, ICMSUFDestForm, IPIForm, PISForm, COFINSForm
from djangosige.apps.fiscal.models import GrupoFiscal, ICMS, ICMSSN, ICMSUFDest, IPI
from djangosige.apps.cadastro.models import MinhaEmpresa
from djangosige.apps.login.models import Usuario


class AdicionarGrupoFiscalView(CustomCreateView):
    form_class = GrupoFiscalForm
    template_name = "fiscal/grupo_fiscal/grupo_fiscal_add.html"
    success_url = reverse_lazy('djangosige.apps.fiscal:listagrupofiscalview')
    success_message = "Grupo fiscal <b>%(descricao)s </b>adicionado com sucesso."
    permission_codename = 'add_grupofiscal'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(AdicionarGrupoFiscalView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR GRUPO FISCAL'
        context['return_url'] = reverse_lazy('djangosige.apps.fiscal:listagrupofiscalview')
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form = GrupoFiscalForm()

        # Dados iniciais da situação fiscal da MinhaEmpresa
        try:
            user_empresa = MinhaEmpresa.objects.get(
                m_usuario=Usuario.objects.get(user=request.user)).m_empresa
            if user_empresa.pessoa_jur_info.sit_fiscal in ('LR', 'LP'):
                form.initial = {'regime_trib': '0'}
            else:
                form.initial = {'regime_trib': '1'}
        except:
            pass

        icms_form = ICMSForm(prefix='icms_form')
        icmssn_form = ICMSSNForm(prefix='icmssn_form')
        icms_dest_form = ICMSUFDestForm(prefix='icms_dest_form')
        ipi_form = IPIForm(prefix='ipi_form')
        pis_form = PISForm(prefix='pis_form')
        cofins_form = COFINSForm(prefix='cofins_form')

        return self.render_to_response(self.get_context_data(form=form,
                                                             icms_form=icms_form,
                                                             icmssn_form=icmssn_form,
                                                             icms_dest_form=icms_dest_form,
                                                             ipi_form=ipi_form,
                                                             pis_form=pis_form,
                                                             cofins_form=cofins_form))

    def post(self, request, *args, **kwargs):
        self.object = None

        req_post = request.POST.copy()
        for key in req_post:
            if ('valor' in key or
                    'valiq' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        form = GrupoFiscalForm(request.POST)

        # Tributação normal
        if request.POST['regime_trib'] == '0':
            novo_icms_form = ICMSForm(request.POST, prefix='icms_form')
        # Simples nacional
        elif request.POST['regime_trib'] == '1':
            novo_icms_form = ICMSSNForm(request.POST, prefix='icmssn_form')

        icms_dest_form = ICMSUFDestForm(request.POST, prefix='icms_dest_form')
        ipi_form = IPIForm(request.POST, prefix='ipi_form')
        pis_form = PISForm(request.POST, prefix='pis_form')
        cofins_form = COFINSForm(request.POST, prefix='cofins_form')

        if (form.is_valid() and
            novo_icms_form.is_valid() and
            icms_dest_form.is_valid() and
            ipi_form.is_valid() and
            pis_form.is_valid() and
                cofins_form.is_valid()):

            self.object = form.save(commit=False)
            self.object.save()

            novo_icms_form.instance.grupo_fiscal = self.object
            novo_icms_form.save()
            icms_dest_form.instance.grupo_fiscal = self.object
            icms_dest_form.save()
            ipi_form.instance.grupo_fiscal = self.object
            ipi_form.save()
            pis_form.instance.grupo_fiscal = self.object
            pis_form.save()
            cofins_form.instance.grupo_fiscal = self.object
            cofins_form.save()

            return self.form_valid(form)

        icms_form = ICMSForm(request.POST, prefix='icms_form')
        icmssn_form = ICMSSNForm(request.POST, prefix='icmssn_form')

        return self.form_invalid(form=form,
                                 icms_form=icms_form,
                                 icmssn_form=icmssn_form,
                                 icms_dest_form=icms_dest_form,
                                 ipi_form=ipi_form,
                                 pis_form=pis_form,
                                 cofins_form=cofins_form)


class GrupoFiscalListView(CustomListView):
    template_name = 'fiscal/grupo_fiscal/grupo_fiscal_list.html'
    model = GrupoFiscal
    context_object_name = 'all_grupos'
    success_url = reverse_lazy('djangosige.apps.fiscal:listagrupofiscalview')
    permission_codename = 'view_grupofiscal'

    def get_context_data(self, **kwargs):
        context = super(GrupoFiscalListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'GRUPOS FISCAIS CADASTRADOS'
        context['add_url'] = reverse_lazy('djangosige.apps.fiscal:addgrupofiscalview')
        return context


class EditarGrupoFiscalView(CustomUpdateView):
    form_class = GrupoFiscalForm
    model = GrupoFiscal
    template_name = "fiscal/grupo_fiscal/grupo_fiscal_edit.html"
    success_url = reverse_lazy('djangosige.apps.fiscal:listagrupofiscalview')
    success_message = "Grupo fiscal <b>%(descricao)s </b>editado com sucesso."
    permission_codename = 'change_grupofiscal'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(EditarGrupoFiscalView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('djangosige.apps.fiscal:listagrupofiscalview')
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if self.object.regime_trib == '0':
            icms_form = ICMSForm(grupo_fiscal=self.object, prefix='icms_form')
            icmssn_form = ICMSSNForm(prefix='icmssn_form')
        elif self.object.regime_trib == '1':
            icms_form = ICMSForm(prefix='icms_form')
            icmssn_form = ICMSSNForm(
                grupo_fiscal=self.object, prefix='icmssn_form')

        if ICMSUFDest.objects.filter(grupo_fiscal=self.object).count():
            icms_dest_form = ICMSUFDestForm(
                grupo_fiscal=self.object, prefix='icms_dest_form')
        else:
            icms_dest_form = ICMSUFDestForm(prefix='icms_dest_form')

        if IPI.objects.filter(grupo_fiscal=self.object).count():
            ipi_form = IPIForm(grupo_fiscal=self.object, prefix='ipi_form')
        else:
            ipi_form = IPIForm(prefix='ipi_form')

        if ICMSUFDest.objects.filter(grupo_fiscal=self.object).count():
            pis_form = PISForm(grupo_fiscal=self.object, prefix='pis_form')
        else:
            pis_form = PISForm(prefix='pis_form')

        if ICMSUFDest.objects.filter(grupo_fiscal=self.object).count():
            cofins_form = COFINSForm(
                grupo_fiscal=self.object, prefix='cofins_form')
        else:
            cofins_form = COFINSForm(prefix='cofins_form')

        return self.render_to_response(self.get_context_data(form=form,
                                                             icms_form=icms_form,
                                                             icmssn_form=icmssn_form,
                                                             icms_dest_form=icms_dest_form,
                                                             ipi_form=ipi_form,
                                                             pis_form=pis_form,
                                                             cofins_form=cofins_form))

    def post(self, request, *args, **kwargs):
        req_post = request.POST.copy()
        for key in req_post:
            if ('valor' in key or
                    'valiq' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, instance=self.object)

        if ICMSUFDest.objects.filter(grupo_fiscal=self.object).count():
            icms_dest_form = ICMSUFDestForm(
                request.POST, prefix='icms_dest_form', grupo_fiscal=self.object)
        else:
            icms_dest_form = ICMSUFDestForm(
                request.POST, prefix='icms_dest_form')

        if IPI.objects.filter(grupo_fiscal=self.object).count():
            ipi_form = IPIForm(request.POST, prefix='ipi_form',
                               grupo_fiscal=self.object)
        else:
            ipi_form = IPIForm(request.POST, prefix='ipi_form')

        if ICMSUFDest.objects.filter(grupo_fiscal=self.object).count():
            pis_form = PISForm(request.POST, prefix='pis_form',
                               grupo_fiscal=self.object)
        else:
            pis_form = PISForm(request.POST, prefix='pis_form')

        if ICMSUFDest.objects.filter(grupo_fiscal=self.object).count():
            cofins_form = COFINSForm(
                request.POST, prefix='cofins_form', grupo_fiscal=self.object)
        else:
            cofins_form = COFINSForm(request.POST, prefix='cofins_form')

        if form.is_valid():
            self.object = form.save(commit=False)
            if self.object.regime_trib == '0':
                novo_icms_form = ICMSForm(request.POST, prefix='icms_form')
            elif self.object.regime_trib == '1':
                novo_icms_form = ICMSSNForm(request.POST, prefix='icmssn_form')

            if (novo_icms_form.is_valid() and
                icms_dest_form.is_valid() and
                ipi_form.is_valid() and
                pis_form.is_valid() and
                    cofins_form.is_valid()):

                self.object = form.save(commit=False)
                self.object.save()

                # Mais facil deletar e recriar as entradas.
                ICMSSN.objects.filter(grupo_fiscal=self.object).delete()
                ICMS.objects.filter(grupo_fiscal=self.object).delete()

                novo_icms_form.instance.grupo_fiscal = self.object
                novo_icms_form.save()
                icms_dest_form.save()
                ipi_form.save()
                pis_form.save()
                cofins_form.save()

                return self.form_valid(form)

        icms_form = ICMSForm(request.POST, prefix='icms_form')
        icmssn_form = ICMSSNForm(request.POST, prefix='icmssn_form')

        return self.form_invalid(form=form,
                                 icms_form=icms_form,
                                 icmssn_form=icmssn_form,
                                 icms_dest_form=icms_dest_form,
                                 ipi_form=ipi_form,
                                 pis_form=pis_form,
                                 cofins_form=cofins_form)
