# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.shortcuts import redirect

from djangosige.apps.base.custom_views import CustomCreateView, CustomUpdateView, CustomTemplateView

from djangosige.apps.financeiro.models import PlanoContasGrupo, PlanoContasSubgrupo
from djangosige.apps.financeiro.forms import PlanoContasGrupoForm, PlanoContasSubgrupoFormSet


class PlanoContasView(CustomTemplateView):
    template_name = "financeiro/plano/plano.html"
    success_url = reverse_lazy('djangosige.apps.financeiro:planocontasview')
    permission_codename = 'view_planocontasgrupo'

    def get_context_data(self, **kwargs):
        context = super(PlanoContasView, self).get_context_data(**kwargs)
        grupo_entrada = []
        grupo_saida = []

        for grupo in PlanoContasGrupo.objects.all():
            if grupo.tipo_grupo == '0' and '.' not in grupo.codigo:
                grupo_entrada.append(grupo)
            elif grupo.tipo_grupo == '1' and '.' not in grupo.codigo:
                grupo_saida.append(grupo)

        context['all_grupos_entrada'] = grupo_entrada
        context['all_grupos_saida'] = grupo_saida
        return context

    # Remover items selecionados da database
    def post(self, request, *args, **kwargs):
        if self.check_user_delete_permission(request, PlanoContasGrupo):
            for key, value in request.POST.items():
                if value == 'on':
                    grupo = None
                    subgrupo = False
                    tipo = None
                    try:
                        instance = PlanoContasSubgrupo.objects.get(id=key)
                        grupo = instance.grupo
                        subgrupo = True
                    except PlanoContasGrupo.DoesNotExist:
                        instance = PlanoContasGrupo.objects.get(id=key)
                        grupo = instance

                    tipo = instance.tipo_grupo
                    instance.delete()

                    # Reordenar codigos dos subgrupos
                    if grupo and subgrupo:
                        for i, obj in enumerate(PlanoContasSubgrupo.objects.filter(grupo=grupo), start=1):
                            obj.codigo = str(grupo.codigo) + '.' + str(i)
                            obj.save()
                    # Reordenar codigos dos grupos e subgrupos
                    else:
                        id_list = []
                        for g in PlanoContasGrupo.objects.filter(tipo_grupo=tipo):
                            if not PlanoContasSubgrupo.objects.filter(id=g.id).count():
                                id_list.append(g.id)

                        for i, obj in enumerate(PlanoContasGrupo.objects.filter(pk__in=id_list), start=1):
                            obj.codigo = str(i)
                            obj.save()
                            for j, subobj in enumerate(PlanoContasSubgrupo.objects.filter(grupo=obj), start=1):
                                subobj.codigo = str(obj.codigo) + '.' + str(j)
                                subobj.save()

        return redirect(self.success_url)


class AdicionarGrupoPlanoContasView(CustomCreateView):
    form_class = PlanoContasGrupoForm
    template_name = "financeiro/plano/grupo_add.html"
    success_url = reverse_lazy('djangosige.apps.financeiro:planocontasview')
    success_message = "Grupo <b>%(descricao)s </b>adicionado com sucesso."
    permission_codename = 'add_planocontasgrupo'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get(self, request, *args, **kwargs):
        self.object = None
        form = PlanoContasGrupoForm(prefix='grupo_form')

        subgrupo_form = PlanoContasSubgrupoFormSet(prefix='subgrupo_form')
        subgrupo_form.can_delete = False

        return self.render_to_response(self.get_context_data(form=form, formset=subgrupo_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = PlanoContasGrupoForm(request.POST, prefix='grupo_form')

        subgrupo_form = PlanoContasSubgrupoFormSet(
            request.POST, prefix='subgrupo_form')

        if (form.is_valid() and subgrupo_form.is_valid()):
            self.object = form.save(commit=False)
            n_subgrupos = PlanoContasSubgrupo.objects.filter(
                tipo_grupo=self.object.tipo_grupo).count()
            n_grupos = PlanoContasGrupo.objects.filter(
                tipo_grupo=self.object.tipo_grupo).count()

            self.object.codigo = n_grupos - n_subgrupos + 1
            self.object.save()

            subgrupo_form.instance = self.object
            objs = subgrupo_form.save()

            for i, obj in enumerate(objs, start=1):
                obj.codigo = str(self.object.codigo) + '.' + str(i)
                obj.tipo_grupo = self.object.tipo_grupo
                obj.save()

            return self.form_valid(form)

        return self.form_invalid(form=form, subgrupo_form=subgrupo_form)


class EditarGrupoPlanoContasView(CustomUpdateView):
    form_class = PlanoContasGrupoForm
    model = PlanoContasGrupo
    template_name = "financeiro/plano/grupo_edit.html"
    success_url = reverse_lazy('djangosige.apps.financeiro:planocontasview')
    success_message = "Grupo <b>%(descricao)s </b>editado com sucesso."
    permission_codename = 'change_planocontasgrupo'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        subgrupo_form = PlanoContasSubgrupoFormSet(
            instance=self.object, prefix='subgrupo_form')
        subgrupos = PlanoContasSubgrupo.objects.filter(grupo=self.object)

        if len(subgrupos):
            subgrupo_form.extra = 0

        return self.render_to_response(self.get_context_data(form=form, formset=subgrupo_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        subgrupo_form = PlanoContasSubgrupoFormSet(
            request.POST, prefix='subgrupo_form', instance=self.object)

        if (form.is_valid() and subgrupo_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()

            subgrupo_form.instance = self.object
            subgrupo_form.save()

            for i, obj in enumerate(PlanoContasSubgrupo.objects.filter(grupo=self.object), start=1):
                obj.codigo = str(self.object.codigo) + '.' + str(i)
                obj.tipo_grupo = self.object.tipo_grupo
                obj.save()

            return self.form_valid(form)

        return self.form_invalid(form=form, subgrupo_form=subgrupo_form)
