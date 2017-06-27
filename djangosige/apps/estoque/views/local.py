# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import redirect

from djangosige.apps.estoque.forms import LocalEstoqueForm
from djangosige.apps.estoque.models import LocalEstoque

class AdicionarLocalEstoqueView(CreateView):
    form_class = LocalEstoqueForm
    template_name = "base/popup_form.html"
    success_url = reverse_lazy('estoque:listalocalview')
    success_message = "Localização de estoque <b>%(descricao)s </b>adicionada com sucesso."

    def view_context(self, context):
        context['titulo'] = 'ADICIONAR LOCAL DE ESTOQUE'
        return context

    def get_context_data(self, **kwargs):
        context = super(AdicionarLocalEstoqueView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def form_valid(self, form):
        super(AdicionarLocalEstoqueView, self).form_valid(form)
        messages.success(self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)


class LocalEstoqueListView(ListView):
    template_name = 'estoque/local/local_list.html'
    model = LocalEstoque
    context_object_name = 'all_locais'
    success_url = reverse_lazy('estoque:listalocalview')

    def view_context(self, context):
        context['title_complete'] = 'LOCAIS DE ESTOQUE'
        context['add_url'] = reverse_lazy('estoque:addlocalview')
        return context

    def get_context_data(self, **kwargs):
        context = super(LocalEstoqueListView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get_queryset(self):
        return LocalEstoque.objects.all()

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if value=="on":
                instance = LocalEstoque.objects.get(id=key)
                instance.delete()
        return redirect(self.success_url)


class EditarLocalEstoqueView(UpdateView):
    form_class = LocalEstoqueForm
    model = LocalEstoque
    template_name = "base/popup_form.html"
    success_url = reverse_lazy('estoque:listalocalview')
    success_message = "Localização de estoque <b>%(descricao)s </b>editada com sucesso."

    def view_context(self, context):
        context['titulo'] = 'Editar local de estoque: ' + str(self.object)
        return context

    def get_context_data(self, **kwargs):
        context = super(EditarLocalEstoqueView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def form_valid(self, form):
        super(EditarLocalEstoqueView, self).form_valid(form)
        messages.success(self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)

