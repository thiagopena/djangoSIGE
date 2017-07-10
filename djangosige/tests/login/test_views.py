from djangosige.tests.test_case import BaseTestCase
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

    def test_editar_perfil_get_request(self):
        url = reverse('login:editarperfilview')

        # Sem MinhaEmpresa cadastrada
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
