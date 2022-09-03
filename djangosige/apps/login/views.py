# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.views.generic import View, TemplateView, FormView, ListView, DeleteView
from django.views.generic.edit import UpdateView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.models import Permission

from django.db import DatabaseError
from django.db.models.query_utils import Q
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader

from djangosige.apps.base.views_mixins import SuperUserRequiredMixin

from .forms import UserLoginForm, UserRegistrationForm, PasswordResetForm, SetPasswordForm, PerfilUsuarioForm
from .models import Usuario
from djangosige.configs.settings import DEFAULT_FROM_EMAIL

from djangosige.apps.cadastro.forms import MinhaEmpresaForm
from djangosige.apps.cadastro.models import MinhaEmpresa

import operator
from functools import reduce


DEFAULT_PERMISSION_MODELS = ['cliente', 'fornecedor', 'produto',
                             'empresa', 'transportadora', 'unidade', 'marca', 'categoria', 'orcamentocompra', 'pedidocompra', 'condicaopagamento', 'orcamentovenda', 'pedidovenda',
                             'naturezaoperacao', 'notafiscalentrada', 'notafiscalsaida', 'grupofiscal', 'lancamento', 'planocontasgrupo', 'localestoque', 'movimentoestoque', ]

CUSTOM_PERMISSIONS = ['configurar_nfe', 'emitir_notafiscal', 'cancelar_notafiscal', 'gerar_danfe', 'consultar_cadastro', 'inutilizar_notafiscal', 'consultar_notafiscal',
                      'baixar_notafiscal', 'manifestacao_destinatario', 'faturar_pedidovenda', 'faturar_pedidocompra', 'acesso_fluxodecaixa', 'consultar_estoque', ]


class UserFormView(View):
    form_class = UserLoginForm
    template_name = 'login/login.html'

    def get(self, request):
        form = self.form_class(None)

        if request.user.is_authenticated:
            return redirect('djangosige.apps.base:index')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if request.POST and form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = form.authenticate_user(username=username, password=password)
            if user:
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                login(request, user)
                return redirect('djangosige.apps.base:index')

        return render(request, self.template_name, {'form': form})


class UserRegistrationFormView(SuperUserRequiredMixin, SuccessMessageMixin, FormView):
    form_class = UserRegistrationForm
    template_name = 'login/registrar.html'
    success_url = reverse_lazy('djangosige.apps.login:usuariosview')
    success_message = "Novo usuário <b>%(username)s</b> criado com sucesso."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, username=cleaned_data['username'])

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['confirm']
            if password == password_confirm:
                user.set_password(password)
                user.save()
                return self.form_valid(form)
            else:
                form.add_error('password', 'Senhas diferentes.')
                return self.form_invalid(form)

            return redirect("djangosige.apps.login:usuariosview")

        return render(request, self.template_name, {'form': form})


class UserLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("djangosige.apps.login:loginview")


class ForgotPasswordView(FormView):
    template_name = "login/esqueceu_senha.html"
    success_url = reverse_lazy('djangosige.apps.login:loginview')
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not DEFAULT_FROM_EMAIL:
            form.add_error(
                field=None, error=u"Envio de email não configurado.")
            return self.form_invalid(form)

        if form.is_valid():
            data = form.cleaned_data["email_or_username"]
            associated_user = User.objects.filter(
                Q(email=data) | Q(username=data)).first()

            if associated_user:
                try:
                    if associated_user.email:
                        c = {
                            'email': associated_user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'djangoSIGE',
                            'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)).decode(encoding="utf-8"),
                            'user': associated_user,
                            'token': default_token_generator.make_token(associated_user),
                            'protocol': 'http://',
                        }
                        subject = u"Redefinir sua senha - DjangoSIGE"
                        email_template_name = 'login/trocar_senha_email.html'
                        email_mensagem = loader.render_to_string(
                            email_template_name, c)
                        sended = send_mail(subject, email_mensagem, DEFAULT_FROM_EMAIL, [
                                           associated_user.email, ], fail_silently=False)

                        if sended == 1:
                            messages.success(request, u'Um email foi enviado para ' + data +
                                             u'. Aguarde o recebimento da mensagem para trocar sua senha.')
                            return self.form_valid(form)
                        else:
                            form.add_error(
                                field=None, error=u"Erro ao enviar email de verificação.")
                            return self.form_invalid(form)
                    else:
                        form.add_error(
                            field=None, error=u"Este usuário não cadastrou um email.")
                        return self.form_invalid(form)

                except Exception as e:
                    form.add_error(field=None, error=e)
                    return self.form_invalid(form)

            else:
                form.add_error(
                    field=None, error=u"Usuário/Email: {} não foi encontrado na database.".format(data))
                return self.form_invalid(form)

        form.add_error(field=None, error="Entrada inválida.")
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "login/trocar_senha.html"
    success_url = reverse_lazy('djangosige.apps.login:loginview')
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        userModel = get_user_model()
        form = self.form_class(request.POST)

        if uidb64 is None or token is None:
            form.add_error(
                field=None, error=u"O link usado para a troca de senha não é válido ou expirou, por favor tente enviar novamente.")
            return self.form_invalid(form)

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = userModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, userModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                new_password_confirm = form.cleaned_data[
                    'new_password_confirm']
                if new_password == new_password_confirm:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, u"Senha trocada com sucesso")
                    return self.form_valid(form)
                else:
                    form.add_error(field=None, error=u"Senhas diferentes.")
                    return self.form_invalid(form)
            else:
                form.add_error(
                    field=None, error=u"Não foi possivel trocar a senha. Formulário inválido.")
                return self.form_invalid(form)
        else:
            form.add_error(
                field=None, error=u"O link usado para a troca de senha não é válido ou expirou, por favor tente enviar novamente.")
            return self.form_invalid(form)


class MeuPerfilView(TemplateView):
    model = Usuario
    template_name = 'login/perfil.html'


class EditarPerfilView(UpdateView):
    form_class = PerfilUsuarioForm
    template_name = 'login/editar_perfil.html'
    success_url = reverse_lazy('djangosige.apps.login:perfilview')
    success_message = "Perfil editado com sucesso."

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_object(self, queryset=None):
        obj = Usuario.objects.get_or_create(user=self.request.user)[0]
        return obj

    def get_success_url(self, *args, **kwargs):
        return self.success_url

    def get(self, request, *args, **kwargs):
        super(EditarPerfilView, self).get(request, *args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        try:
            empresa_instance = MinhaEmpresa.objects.get(
                m_usuario=self.object.id)
            minha_empresa_form = MinhaEmpresaForm(
                instance=empresa_instance, prefix='m_empresa_form')
        except MinhaEmpresa.DoesNotExist:
            minha_empresa_form = MinhaEmpresaForm(prefix='m_empresa_form')

        return self.render_to_response(self.get_context_data(form=form, minha_empresa_form=minha_empresa_form, object=self.object))

    def post(self, request):
        self.object = self.get_object()

        try:
            instance = Usuario.objects.get(user=request.user)
            form = self.form_class(
                request.POST, request.FILES, instance=instance)
        except Usuario.DoesNotExist:
            form = self.form_class(request.POST, request.FILES, instance=None)

        try:
            empresa_instance = MinhaEmpresa.objects.get(
                m_usuario=self.object.id)
            minha_empresa_form = MinhaEmpresaForm(
                request.POST, prefix='m_empresa_form', instance=empresa_instance)
        except MinhaEmpresa.DoesNotExist:
            minha_empresa_form = MinhaEmpresaForm(
                request.POST, prefix='m_empresa_form', instance=None)

        user = User.objects.get(pk=request.user.id)

        if form.is_valid() and minha_empresa_form.is_valid():
            try:
                perfil = form.save(commit=False)
                user.first_name = request.POST.get("first_name")
                user.last_name = request.POST.get("last_name")
                user.username = request.POST.get("username")
                user.email = request.POST.get("email")
                user.full_clean()
                user.save()
                perfil.user = user
                if 'user_foto' in request.FILES:
                    perfil.user_foto = request.FILES['user_foto']
                perfil.save()

                minha_empresa = minha_empresa_form.save(commit=False)
                minha_empresa.m_usuario = perfil
                minha_empresa.save()

                return self.form_valid(form, minha_empresa_form)

            except (DatabaseError, ValidationError) as e:
                form.add_error(field=None, error=e)

        return render(request, self.template_name, {'form': form, 'minha_empresa_form': minha_empresa_form})

    def form_valid(self, form, minha_empresa_form):
        messages.success(
            self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)


class SelecionarMinhaEmpresaView(FormView):
    form_class = MinhaEmpresaForm
    template_name = "login/selecionar_minha_empresa.html"
    success_url = reverse_lazy('djangosige.apps.login:selecionarempresaview')

    def get_form(self, form_class):
        try:
            usuario = Usuario.objects.get(user=self.request.user)
            return form_class(instance=usuario, **self.get_form_kwargs())
        except Usuario.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def get(self, request):
        try:
            usuario = Usuario.objects.get(user=self.request.user)
            empresa_instance = MinhaEmpresa.objects.get(m_usuario=usuario.id)
            form = MinhaEmpresaForm(instance=empresa_instance)
        except MinhaEmpresa.DoesNotExist:
            form = MinhaEmpresaForm()
        except Usuario.DoesNotExist:
            usuario = Usuario.objects.get_or_create(user=self.request.user)[0]
            form = MinhaEmpresaForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        try:
            usuario = Usuario.objects.get(user=self.request.user)
            empresa_instance = MinhaEmpresa.objects.get(m_usuario=usuario.id)
            form = MinhaEmpresaForm(request.POST, instance=empresa_instance)
        except MinhaEmpresa.DoesNotExist:
            form = MinhaEmpresaForm(request.POST, instance=None)

        if form.is_valid():
            usuario = Usuario.objects.get(user=request.user)
            minha_empresa = form.save(commit=False)
            minha_empresa.m_usuario = usuario
            minha_empresa.save()
            return self.form_valid(form)

        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        return redirect(self.success_url)


class UsuariosListView(SuperUserRequiredMixin, ListView):
    template_name = 'login/lista_users.html'
    model = User
    context_object_name = 'all_users'
    success_url = reverse_lazy('djangosige.apps.login:usuariosview')

    def get_queryset(self):
        return User.objects.all()

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if value == "on":
                instance = User.objects.get(id=key)
                instance.delete()
        return redirect(self.success_url)


class UsuarioDetailView(SuperUserRequiredMixin, TemplateView):
    model = User
    template_name = 'login/detalhe_users.html'

    def get_context_data(self, **kwargs):
        context = super(UsuarioDetailView, self).get_context_data(**kwargs)
        try:
            usr = User.objects.get(pk=self.kwargs['pk'])
            context['user_match'] = usr
            context['user_foto'] = Usuario.objects.get(user=usr).user_foto
        except:
            pass
        return context


class DeletarUsuarioView(SuperUserRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('djangosige.apps.login:usuariosview')


class EditarPermissoesUsuarioView(SuperUserRequiredMixin, TemplateView):
    template_name = 'login/editar_permissoes_user.html'

    def get_context_data(self, **kwargs):
        context = super(EditarPermissoesUsuarioView,
                        self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['pk'])
        context['user'] = user
        condition = reduce(operator.or_, [Q(codename__icontains=s) for s in [
                           'add_', 'change_', 'view_', 'delete_']])
        context['default_permissions'] = Permission.objects.filter(
            condition, content_type__model__in=DEFAULT_PERMISSION_MODELS)
        context['custom_permissions'] = Permission.objects.filter(
            codename__in=CUSTOM_PERMISSIONS)
        return context

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        if not user.is_superuser:
            user.user_permissions.clear()
            for nova_permissao_codename in request.POST.getlist('select_permissoes'):
                nova_permissao = Permission.objects.get(
                    codename=nova_permissao_codename)
                user.user_permissions.add(nova_permissao)
        messages.success(
            self.request, 'Permissões do usuário <b>{0}</b> atualizadas com sucesso.'.format(user.username))
        return redirect(reverse_lazy('djangosige.apps.login:usuariodetailview', kwargs={'pk': self.kwargs['pk']}))
