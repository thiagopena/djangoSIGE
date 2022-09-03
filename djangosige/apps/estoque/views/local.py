# -*- coding: utf-8 -*-

from django.urls import reverse_lazy

from djangosige.apps.base.custom_views import CustomCreateView, CustomListView, CustomUpdateView

from djangosige.apps.estoque.forms import LocalEstoqueForm
from djangosige.apps.estoque.models import LocalEstoque


class AdicionarLocalEstoqueView(CustomCreateView):
    form_class = LocalEstoqueForm
    template_name = "base/popup_form.html"
    success_url = reverse_lazy('djangosige.apps.estoque:listalocalview')
    success_message = "Localização de estoque <b>%(descricao)s </b>adicionada com sucesso."
    permission_codename = 'add_localestoque'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(AdicionarLocalEstoqueView,
                        self).get_context_data(**kwargs)
        return self.view_context(context)

    def view_context(self, context):
        context['titulo'] = 'ADICIONAR LOCAL DE ESTOQUE'
        return context


class LocalEstoqueListView(CustomListView):
    template_name = 'estoque/local/local_list.html'
    model = LocalEstoque
    context_object_name = 'all_locais'
    success_url = reverse_lazy('djangosige.apps.estoque:listalocalview')
    permission_codename = 'view_localestoque'

    def view_context(self, context):
        context['title_complete'] = 'LOCAIS DE ESTOQUE'
        context['add_url'] = reverse_lazy('djangosige.apps.estoque:addlocalview')
        return context

    def get_context_data(self, **kwargs):
        context = super(LocalEstoqueListView, self).get_context_data(**kwargs)
        return self.view_context(context)


class EditarLocalEstoqueView(CustomUpdateView):
    form_class = LocalEstoqueForm
    model = LocalEstoque
    template_name = "base/popup_form.html"
    success_url = reverse_lazy('djangosige.apps.estoque:listalocalview')
    success_message = "Localização de estoque <b>%(descricao)s </b>editada com sucesso."
    permission_codename = 'change_localestoque'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def view_context(self, context):
        context['titulo'] = 'Editar local de estoque: ' + str(self.object)
        return context

    def get_context_data(self, **kwargs):
        context = super(EditarLocalEstoqueView,
                        self).get_context_data(**kwargs)
        return self.view_context(context)
