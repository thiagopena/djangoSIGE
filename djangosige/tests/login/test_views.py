# -*- coding: utf-8 -*-

from djangosige.tests.test_case import BaseTestCase, TEST_USERNAME, TEST_PASSWORD
from djangosige.apps.cadastro.models import Empresa, MinhaEmpresa
from djangosige.apps.login.models import Usuario

from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q


class UserFormViewTestCase(BaseTestCase):

    def test_user_logged_in_redirect(self):
        url = reverse('djangosige.apps.login:loginview')

        # Assert login redirect se usuario logado
        response = self.client.get(url)
        self.assertEqual(response.url, '/')

        # Assert abre pagina se usuario nao logado
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')

    def test_user_login(self):
        url = reverse('djangosige.apps.login:loginview')
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
        url = reverse('djangosige.apps.login:registrarview')
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/registrar.html')

    def test_user_registration(self):
        url = reverse('djangosige.apps.login:registrarview')
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

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
        url = reverse('djangosige.apps.login:registrarview')
        # Assert usuario redirect para index se nao e administrador
        self.user.is_superuser = False
        self.user.save()
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

        response = self.client.get(url)
        self.assertEqual(response.url, '/')


class UserLogoutViewTestCase(BaseTestCase):

    def test_user_logout_redirect(self):
        url = reverse('djangosige.apps.login:logoutview')
        response = self.client.get(url)
        self.assertEqual(response.url, '/login/')


class ForgotPasswordViewTestCase(BaseTestCase):

    def test_forgot_view_get_request(self):
        url = reverse('djangosige.apps.login:esqueceuview')

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
        url = reverse('djangosige.apps.login:perfilview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class EditarPerfilViewTestCase(BaseTestCase):

    def test_editar_perfil_view(self):
        url = reverse('djangosige.apps.login:editarperfilview')
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


class SelecionarMinhaEmpresaViewTestCase(BaseTestCase):

    def test_selecionar_empresa_view(self):
        url = reverse('djangosige.apps.login:selecionarempresaview')
        m_empresa = Empresa.objects.create()
        usuario = Usuario.objects.get(user=self.user)
        MinhaEmpresa.objects.filter(m_usuario=usuario).delete()

        # Usuario sem MinhaEmpresa
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'login/selecionar_minha_empresa.html')

        data = {'m_empresa': m_empresa.pk, }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(usuario.empresa_usuario.all()[
                         0].m_empresa.pk, m_empresa.pk)

        # Usuario com MinhaEmpresa
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'login/selecionar_minha_empresa.html')

        m_empresa = Empresa.objects.filter(~Q(id=m_empresa.pk)).first()
        data = {'m_empresa': m_empresa.pk, }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(usuario.empresa_usuario.all()[
                         0].m_empresa.pk, m_empresa.pk)


class UsuariosListViewTestCase(BaseTestCase):

    def test_deletar_usuario(self):
        url = reverse('djangosige.apps.login:usuariosview')
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

        # Testar GET request lista
        obj = User.objects.create()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(obj in response.context['object_list'])
        self.assertTemplateUsed(response, 'login/lista_users.html')

        # Deletar objeto criado por POST request
        data = {
            obj.pk: 'on',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(obj in response.context['object_list'])


class UsuarioDetailViewTestCase(BaseTestCase):

    def test_usuario_detail_get_request(self):
        url = reverse('djangosige.apps.login:usuariodetailview', kwargs={'pk': self.user.pk})
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/detalhe_users.html')


class DeletarUsuarioViewTestCase(BaseTestCase):

    def test_deletar_usuario_view(self):
        new_user = User.objects.create()
        url = reverse('djangosige.apps.login:deletarusuarioview', kwargs={'pk': new_user.pk})
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(new_user in response.context['object_list'])
