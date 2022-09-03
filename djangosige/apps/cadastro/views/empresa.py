# -*- coding: utf-8 -*-

from django.urls import reverse_lazy

from djangosige.apps.cadastro.forms import EmpresaForm
from djangosige.apps.cadastro.models import Empresa

from .base import AdicionarPessoaView, PessoasListView, EditarPessoaView


class AdicionarEmpresaView(AdicionarPessoaView):
    template_name = "cadastro/pessoa_add.html"
    success_url = reverse_lazy('djangosige.apps.cadastro:listaempresasview')
    success_message = "Empresa <b>%(nome_razao_social)s </b>adicionada com sucesso."
    permission_codename = 'add_empresa'

    def get_context_data(self, **kwargs):
        context = super(AdicionarEmpresaView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CADASTRAR EMPRESA'
        context['return_url'] = reverse_lazy('djangosige.apps.cadastro:listaempresasview')
        context['tipo_pessoa'] = 'empresa'
        return context

    def get(self, request, *args, **kwargs):
        form = EmpresaForm(prefix='empresa_form')
        return super(AdicionarEmpresaView, self).get(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = EmpresaForm(request.POST, request.FILES,
                           prefix='empresa_form', request=request)
        return super(AdicionarEmpresaView, self).post(request, form, *args, **kwargs)


class EmpresasListView(PessoasListView):
    template_name = 'cadastro/pessoa_list.html'
    model = Empresa
    context_object_name = 'all_empresas'
    success_url = reverse_lazy('djangosige.apps.cadastro:listaempresasview')
    permission_codename = 'view_empresa'

    def get_context_data(self, **kwargs):
        context = super(EmpresasListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'EMPRESAS CADASTRADAS'
        context['add_url'] = reverse_lazy('djangosige.apps.cadastro:addempresaview')
        context['tipo_pessoa'] = 'empresa'
        return context


class EditarEmpresaView(EditarPessoaView):
    form_class = EmpresaForm
    model = Empresa
    template_name = "cadastro/pessoa_edit.html"
    success_url = reverse_lazy('djangosige.apps.cadastro:listaempresasview')
    success_message = "Empresa <b>%(nome_razao_social)s </b>editada com sucesso."
    permission_codename = 'change_empresa'

    def get_context_data(self, **kwargs):
        context = super(EditarEmpresaView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('djangosige.apps.cadastro:listaempresasview')
        context['tipo_pessoa'] = 'empresa'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form_class.prefix = "empresa_form"
        form = self.get_form(form_class)

        logo_file = Empresa.objects.get(pk=self.object.pk).logo_file
        return super(EditarEmpresaView, self).get(request, form, logo_file=logo_file, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES,
                          prefix='empresa_form', instance=self.object, request=request)
        logo_file = Empresa.objects.get(pk=self.object.pk).logo_file
        return super(EditarEmpresaView, self).post(request, form, logo_file=logo_file, *args, **kwargs)
