from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect


class SuperUserRequiredMixin(object):

    @method_decorator(login_required(login_url='login:loginview'))
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.add_message(
                request,
                messages.WARNING,
                u'Apenas o administrador tem permissão para realizar esta operação.',
                'permission_warning')
            return redirect('base:index')
        return super(SuperUserRequiredMixin, self).dispatch(request, *args, **kwargs)


class CheckPermissionMixin(object):
    permission_codename = ''

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user_permissions(request):
            messages.add_message(
                request,
                messages.WARNING,
                u'Usuário não tem permissão para realizar esta operação.',
                'permission_warning')
            return redirect('base:index')
        return super(CheckPermissionMixin, self).dispatch(request, *args, **kwargs)

    def check_user_permissions(self, request):
        if not isinstance(self.permission_codename, list):
            self.permission_codename = [self.permission_codename]
        perms = []
        for permission in self.permission_codename:
            if '.' not in permission:
                permission = str(
                    request.resolver_match.app_name) + '.' + str(permission)
            perms.append(permission)
        return len(self.permission_codename) and (request.user.is_superuser or request.user.has_perms(perms))

    def check_user_delete_permission(self, request, object):
        codename = str(object._meta.app_label) + '.delete_' + \
            str(object.__name__.lower())
        if not request.user.has_perm(codename):
            messages.add_message(
                request,
                messages.WARNING,
                u'Usuário não tem permissão para realizar esta operação.',
                'permission_warning')
            return False
        return True


class FormValidationMessageMixin(object):
    # Mensagem de sucesso padrao
    success_message = "<b>%(descricao)s </b>adicionado(a) a base de dados com sucesso."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=str(self.object))

    def form_valid(self, form):
        messages.success(
            self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)

    def form_invalid(self, form, **kwargs):
        return self.render_to_response(self.get_context_data(form=form, **kwargs))
