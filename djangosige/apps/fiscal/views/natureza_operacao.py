# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import redirect

from djangosige.apps.fiscal.forms import NaturezaOperacaoForm
from djangosige.apps.fiscal.models import NaturezaOperacao

class AdicionarNaturezaOperacaoView(CreateView):
    form_class = NaturezaOperacaoForm
    template_name = "fiscal/natureza_operacao/natureza_operacao_add.html"
    success_url = reverse_lazy('fiscal:listanaturezaoperacaoview')
    success_message = "Natureza da operação <b>%(cfop)s </b>adicionada com sucesso."
    
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, cfop=self.object.cfop)
    
    def get_context_data(self, **kwargs):
        context = super(AdicionarNaturezaOperacaoView, self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR NATUREZA DA OPERAÇÃO'
        context['return_url'] = reverse_lazy('fiscal:listanaturezaoperacaoview')
        return context
    
    def form_valid(self, form):
        super(AdicionarNaturezaOperacaoView, self).form_valid(form)
        messages.success(self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)
        
        
class NaturezaOperacaoListView(ListView):
    template_name = 'fiscal/natureza_operacao/natureza_operacao_list.html'
    model = NaturezaOperacao
    context_object_name = 'all_natops'
    success_url = reverse_lazy('fiscal:listanaturezaoperacaoview')
    
    def get_context_data(self, **kwargs):
        context = super(NaturezaOperacaoListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'NATUREZAS DA OPERAÇÃO CADASTRADAS'
        context['add_url'] = reverse_lazy('fiscal:addnaturezaoperacaoview')
        return context
   
    def get_queryset(self):
        return NaturezaOperacao.objects.all()
    
    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if value=="on":
                instance = NaturezaOperacao.objects.get(id=key)
                instance.delete()
        return redirect(self.success_url)
        
        
class EditarNaturezaOperacaoView(UpdateView):
    form_class = NaturezaOperacaoForm
    model = NaturezaOperacao
    template_name = "fiscal/natureza_operacao/natureza_operacao_edit.html"
    success_url = reverse_lazy('fiscal:listanaturezaoperacaoview')
    success_message = "Natureza da operação <b>%(cfop)s </b>editada com sucesso."
        
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, cfop=self.object.cfop)
    
    def get_context_data(self, **kwargs):
        context = super(EditarNaturezaOperacaoView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('fiscal:listanaturezaoperacaoview')
        return context
            
    def form_valid(self, form):
        super(EditarNaturezaOperacaoView, self).form_valid(form)
        messages.success(self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)

