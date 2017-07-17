# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.views.generic import View

from djangosige.apps.cadastro.forms import FornecedorForm
from djangosige.apps.cadastro.models import Fornecedor

from .base import AdicionarPessoaView, PessoasListView, EditarPessoaView


class AdicionarFornecedorView(AdicionarPessoaView):
    template_name = "cadastro/pessoa_add.html"
    success_url = reverse_lazy('cadastro:listafornecedoresview')
    success_message = "Fornecedor <b>%(nome_razao_social)s </b>adicionado com sucesso."

    def get_context_data(self, **kwargs):
        context = super(AdicionarFornecedorView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CADASTRAR FORNECEDOR'
        context['return_url'] = reverse_lazy('cadastro:listafornecedoresview')
        context['tipo_pessoa'] = 'fornecedor'
        return context

    def get(self, request, *args, **kwargs):
        form = FornecedorForm(prefix='fornecedor_form')
        return super(AdicionarFornecedorView, self).get(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = FornecedorForm(request.POST, request.FILES,
                              prefix='fornecedor_form', request=request)
        return super(AdicionarFornecedorView, self).post(request, form, *args, **kwargs)


class FornecedoresListView(PessoasListView):
    template_name = 'cadastro/pessoa_list.html'
    model = Fornecedor
    context_object_name = 'all_fornecedores'
    success_url = reverse_lazy('cadastro:listafornecedoresview')

    def get_context_data(self, **kwargs):
        context = super(FornecedoresListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'FORNECEDORES CADASTRADOS'
        context['add_url'] = reverse_lazy('cadastro:addfornecedorview')
        context['tipo_pessoa'] = 'fornecedor'
        return context

    def get_queryset(self):
        return super(FornecedoresListView, self).get_queryset(object=Fornecedor)

    def post(self, request, *args, **kwargs):
        return super(FornecedoresListView, self).post(request, Fornecedor)


class EditarFornecedorView(EditarPessoaView):
    form_class = FornecedorForm
    model = Fornecedor
    template_name = "cadastro/pessoa_edit.html"
    success_url = reverse_lazy('cadastro:listafornecedoresview')
    success_message = "Fornecedor <b>%(nome_razao_social)s </b>editado com sucesso."

    def get_context_data(self, **kwargs):
        context = super(EditarFornecedorView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('cadastro:listafornecedoresview')
        context['tipo_pessoa'] = 'fornecedor'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form_class.prefix = "fornecedor_form"
        form = self.get_form(form_class)

        return super(EditarFornecedorView, self).get(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES,
                          prefix='fornecedor_form', instance=self.object, request=request)
        return super(EditarFornecedorView, self).post(request, form, *args, **kwargs)


class InfoFornecedor(View):

    def post(self, request, *args, **kwargs):
        obj_list = []
        pessoa = Pessoa.objects.get(pk=request.POST['pessoaId'])
        fornecedor = Fornecedor.objects.get(pk=request.POST['pessoaId'])
        obj_list.append(fornecedor)

        if pessoa.endereco_padrao:
            obj_list.append(pessoa.endereco_padrao)
        if pessoa.email_padrao:
            obj_list.append(pessoa.email_padrao)
        if pessoa.telefone_padrao:
            obj_list.append(pessoa.telefone_padrao)

        if pessoa.tipo_pessoa == 'PJ':
            obj_list.append(pessoa.pessoa_jur_info)
        elif pessoa.tipo_pessoa == 'PF':
            obj_list.append(pessoa.pessoa_fis_info)

        data = serializers.serialize('json', obj_list, fields=('indicador_ie', 'limite_de_credito', 'cnpj', 'inscricao_estadual', 'responsavel', 'cpf', 'rg', 'id_estrangeiro', 'logradouro', 'numero', 'bairro',
                                                               'municipio', 'cmun', 'uf', 'pais', 'complemento', 'cep', 'email', 'telefone',))

        return HttpResponse(data, content_type='application/json')
