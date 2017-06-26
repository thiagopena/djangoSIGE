# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy

from djangosige.apps.cadastro.forms import ClienteForm
from djangosige.apps.cadastro.models import Cliente

from .base import AdicionarPessoaView, PessoasListView, EditarPessoaView


class AdicionarClienteView(AdicionarPessoaView):
    template_name = "cadastro/pessoa_add.html"
    success_url = reverse_lazy('cadastro:listaclientesview')
    success_message = "Cliente <b>%(nome_razao_social)s </b>adicionado com sucesso."
    
    def get_context_data(self, **kwargs):
        context = super(AdicionarClienteView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CADASTRAR CLIENTE'
        context['return_url'] = reverse_lazy('cadastro:listaclientesview')
        context['tipo_pessoa'] = 'cliente'
        return context
    
    def get(self, request, *args, **kwargs):
        form = ClienteForm(prefix='cliente_form')
        return super(AdicionarClienteView, self).get(request, form, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST['cliente_form-limite_de_credito'] = request.POST['cliente_form-limite_de_credito'].replace('.','')
        form = ClienteForm(request.POST, request.FILES, prefix='cliente_form', request=request)
        return super(AdicionarClienteView, self).post(request, form, *args, **kwargs)
        

class ClientesListView(PessoasListView):
    template_name = 'cadastro/pessoa_list.html'
    model = Cliente
    context_object_name = 'all_clientes'
    success_url = reverse_lazy('cadastro:listaclientesview')
    
    def get_context_data(self, **kwargs):
        context = super(ClientesListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CLIENTES CADASTRADOS'
        context['add_url'] = reverse_lazy('cadastro:addclienteview')
        context['tipo_pessoa'] = 'cliente'
        return context
   
    def get_queryset(self):
        return super(ClientesListView, self).get_queryset(object=Cliente)
    
    def post(self, request, *args, **kwargs):
        return super(ClientesListView, self).post(request, Cliente)
        
        
class EditarClienteView(EditarPessoaView):
    form_class = ClienteForm
    model = Cliente
    template_name = "cadastro/pessoa_edit.html"
    success_url = reverse_lazy('cadastro:listaclientesview')
    success_message = "Cliente <b>%(nome_razao_social)s </b>editado com sucesso."
    
    def get_context_data(self, **kwargs):
        context = super(EditarClienteView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('cadastro:listaclientesview')
        context['tipo_pessoa'] = 'cliente'
        return context
            
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form_class.prefix = "cliente_form"
        form = self.get_form(form_class)
        
        return super(EditarClienteView, self).get(request, form, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        request.POST['cliente_form-limite_de_credito'] = request.POST['cliente_form-limite_de_credito'].replace('.','')
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES, prefix='cliente_form', instance=self.object, request=request)
        return super(EditarClienteView, self).post(request, form, *args, **kwargs)
        