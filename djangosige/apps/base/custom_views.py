# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from django.shortcuts import redirect

from djangosige.apps.base.views_mixins import CheckPermissionMixin, FormValidationMessageMixin


class CustomView(CheckPermissionMixin, View):

    def __init__(self, *args, **kwargs):
        super(CustomView, self).__init__(*args, **kwargs)


class CustomTemplateView(CheckPermissionMixin, TemplateView):

    def __init__(self, *args, **kwargs):
        super(CustomTemplateView, self).__init__(*args, **kwargs)


class CustomDetailView(CheckPermissionMixin, DetailView):

    def __init__(self, *args, **kwargs):
        super(CustomDetailView, self).__init__(*args, **kwargs)


class CustomCreateView(CheckPermissionMixin, FormValidationMessageMixin, CreateView):

    def __init__(self, *args, **kwargs):
        super(CustomCreateView, self).__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = form.save()
            return redirect(self.success_url)
        return self.form_invalid(form)


class CustomListView(CheckPermissionMixin, ListView):

    def __init__(self, *args, **kwargs):
        super(CustomListView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    # Remover items selecionados da database
    def post(self, request, *args, **kwargs):
        if self.check_user_delete_permission(request, self.model):
            for key, value in request.POST.items():
                if value == "on":
                    instance = self.model.objects.get(id=key)
                    instance.delete()
        return redirect(self.success_url)


class CustomUpdateView(CheckPermissionMixin, FormValidationMessageMixin, UpdateView):

    def __init__(self, *args, **kwargs):
        super(CustomUpdateView, self).__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object = form.save()
            return redirect(self.success_url)
        return self.form_invalid(form)
