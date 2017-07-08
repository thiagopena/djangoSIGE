from djangosige.tests.test_case import BaseTestCase
from django.core.urlresolvers import reverse

CADASTRO_MODELS = (
    "empresa",
    "cliente",
    "fornecedor",
    "transportadora",
    "produto",
    "categoria",
    "unidade",
    "marca",
)

CADASTRO_MODELS_PLURAL = (
    "empresas",
    "clientes",
    "fornecedores",
    "transportadoras",
    "produtos",
    "categorias",
    "unidades",
    "marcas",
)


class CadastroAdicionarViewsTestCase(BaseTestCase):

    def test_add_views_get_request(self):
        for m in CADASTRO_MODELS:
            url = reverse('cadastro:add{}view'.format(m))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


class CadastroListarViewsTestCase(BaseTestCase):

    def test_list_views_get_request(self):
        for m in CADASTRO_MODELS_PLURAL:
            url = reverse('cadastro:lista{}view'.format(m))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        url = reverse('cadastro:listaprodutosbaixoestoqueview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CadastroEditarViewsTestCase(BaseTestCase):

    def test_edit_views_get_request(self):
        pass
