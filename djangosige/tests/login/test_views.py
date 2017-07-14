# -*- coding: utf-8 -*-

from djangosige.tests.test_case import BaseTestCase, TEST_USERNAME, TEST_PASSWORD
from djangosige.apps.cadastro.models import Empresa
from djangosige.apps.login.models import Usuario

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class UserFormViewTestCase(BaseTestCase):

    def test_user_logged_in_redirect(self):
        url = reverse('login:loginview')

        # Assert login redirect se usuario logado
        response = self.client.get(url)
        self.assertEqual(response.url, '/')

        # Assert abre pagina se usuario nao logado
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')

    def test_user_login(self):
        url = reverse('login:loginview')
        self.client.logout()
        data = {
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD,
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/index.html')


class UserRegistrationFormViewTestCase(BaseTestCase):

    def test_registration_view_get_request(self):
        url = reverse('login:registrarview')
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/registrar.html')

    def test_user_registration(self):
        url = reverse('login:registrarview')
        self.user.is_superuser = True
        self.user.save()
        data = {
            'username': 'newUser',
            'password': 'password1234',
            'confirm': 'password1234',
            'email': 'newUser@email.com',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newUser').exists())

        # Assert form invalido (senhas diferentes)
        data = {
            'username': 'newUser2',
            'password': 'password1234',
            'confirm': 'diferente',
            'email': 'newUser2@email.com',
        }
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'password', 'Senhas diferentes.')

    def test_superuser_required(self):
        url = reverse('login:registrarview')
        # Assert usuario redirect para index se nao e administrador
        self.user.is_superuser = False
        self.user.save()
        response = self.client.get(url)
        self.assertEqual(response.url, '/')


class UserLogoutViewTestCase(BaseTestCase):

    def test_user_logout_redirect(self):
        url = reverse('login:logoutview')
        response = self.client.get(url)
        self.assertEqual(response.url, '/login/')


class ForgotPasswordViewTestCase(BaseTestCase):

    def test_forgot_view_get_request(self):
        url = reverse('login:esqueceuview')

        # Assert login redirect se usuario logado
        response = self.client.get(url)
        self.assertEqual(response.url, '/')

        # Assert abre pagina se usuario nao logado
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/esqueceu_senha.html')


class MeuPerfilViewTestCase(BaseTestCase):

    def test_perfil_get_request(self):
        url = reverse('login:perfilview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class EditarPerfilViewTestCase(BaseTestCase):

    def test_editar_perfil_view(self):
        url = reverse('login:editarperfilview')
        m_empresa = Empresa.objects.create()
        usuario = Usuario.objects.get(user=self.user)

        # Sem MinhaEmpresa cadastrada
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Adicionar MinhaEmpresa pela view
        data = response.context['form'].initial
        data['username'] = response.context['user'].username
        data['first_name'] = response.context['user'].first_name
        data['last_name'] = response.context['user'].last_name
        data['email'] = response.context['user'].email
        data['m_empresa_form-m_empresa'] = m_empresa.pk

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/perfil.html')
        self.assertEqual(usuario.empresa_usuario.all()[
                         0].m_empresa.pk, m_empresa.pk)
