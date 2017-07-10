from djangosige.tests.test_case import BaseTestCase
from djangosige.apps.cadastro.models import Produto, Unidade, Marca, Categoria, Transportadora, Fornecedor, Cliente, Empresa
from django.core.urlresolvers import reverse, resolve


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

PESSOA_MODELS = (
    "empresa",
    "cliente",
    "fornecedor",
    "transportadora",
)

INLINE_FORMSET_DATA = {
    'endereco_form-0-tipo_endereco': 'UNI',
    'endereco_form-0-logradouro': 'Logradouro Cliente',
    'endereco_form-0-numero': '123',
    'endereco_form-0-bairro': 'Bairro Cliente',
    'endereco_form-0-complemento': '',
    'endereco_form-0-pais': 'Brasil',
    'endereco_form-0-cpais': '1058',
    'endereco_form-0-municipio': 'Municipio',
    'endereco_form-0-cmun': '12345',
    'endereco_form-0-cep': '1234567',
    'endereco_form-0-uf': 'MG',
    'endereco_form-TOTAL_FORMS': 1,
    'endereco_form-INITIAL_FORMS': 0,
    'telefone_form-TOTAL_FORMS': 1,
    'telefone_form-INITIAL_FORMS': 0,
    'email_form-TOTAL_FORMS': 1,
    'email_form-INITIAL_FORMS': 0,
    'site_form-TOTAL_FORMS': 1,
    'site_form-INITIAL_FORMS': 0,
    'banco_form-TOTAL_FORMS': 1,
    'banco_form-INITIAL_FORMS': 0,
    'documento_form-TOTAL_FORMS': 1,
    'documento_form-INITIAL_FORMS': 0,
}


class CadastroAdicionarViewsTestCase(BaseTestCase):

    def test_add_views_get_request(self):
        for m in CADASTRO_MODELS:
            url = reverse('cadastro:add{}view'.format(m))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_add_pessoa_post_request(self):
        for m in PESSOA_MODELS:
            url = reverse('cadastro:add{}view'.format(m))
            pessoa_data = {
                '{}_form-nome_razao_social'.format(m): 'Razao Social Qualquer',
                '{}_form-tipo_pessoa'.format(m): 'PJ',
                '{}_form-inscricao_municipal'.format(m): '',
                '{}_form-informacoes_adicionais'.format(m): '',
            }

            if m == 'cliente':
                pessoa_data['cliente_form-limite_de_credito'] = '0.00'
                pessoa_data['cliente_form-indicador_ie'] = '1'
                pessoa_data['cliente_form-id_estrangeiro'] = ''
            elif m == 'transportadora':
                pessoa_data['veiculo_form-TOTAL_FORMS'] = 1
                pessoa_data['veiculo_form-INITIAL_FORMS'] = 0
                pessoa_data['veiculo_form-0-descricao'] = 'Veiculo1'
                pessoa_data['veiculo_form-0-placa'] = 'XXXXXXXX'
                pessoa_data['veiculo_form-0-uf'] = 'SP'

            pessoa_data.update(INLINE_FORMSET_DATA)

            response = self.client.post(url, pessoa_data, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'cadastro/pessoa_list.html')

            # Assert form invalido
            pessoa_data['{}_form-nome_razao_social'.format(m)] = ''
            response = self.client.post(url, pessoa_data, follow=True)
            self.assertFormError(
                response, 'form', 'nome_razao_social', 'Este campo é obrigatório.')

    def test_add_produto_post_request(self):
        url = reverse('cadastro:addprodutoview')
        produto_data = {
            'codigo': '000000000000010',
            'descricao': 'Produto Teste',
            'origem': '0',
            'venda': '100,00',
            'custo': '50,00',
            'estoque_minimo': '100,00',
            'estoque_atual': '500,00',
            'ncm': '02109100[EX:01]',
            'fornecedor': '2',  # Id Fornecedor1
            'local_dest': '1',  # Id Estoque Padrao
        }

        response = self.client.post(url, produto_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro/produto/produto_list.html')

        # Assert form invalido
        produto_data['codigo'] = ''
        response = self.client.post(url, produto_data, follow=True)
        self.assertFormError(response, 'form', 'codigo',
                             'Este campo é obrigatório.')

    def test_add_categoria_post_request(self):
        url = reverse('cadastro:addcategoriaview')
        data = {
            'categoria_desc': 'Categoria Teste',
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Assert form invalido
        data['categoria_desc'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'categoria_desc', 'Este campo é obrigatório.')

    def test_add_marca_post_request(self):
        url = reverse('cadastro:addmarcaview')
        data = {
            'marca_desc': 'Marca Teste',
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Assert form invalido
        data['marca_desc'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(response, 'form', 'marca_desc',
                             'Este campo é obrigatório.')

    def test_add_unidade_post_request(self):
        url = reverse('cadastro:addunidadeview')
        data = {
            'sigla_unidade': 'UNT',
            'unidade_desc': 'Unidade Teste',
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Assert form invalido
        data['sigla_unidade'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'sigla_unidade', 'Este campo é obrigatório.')


class CadastroListarViewsTestCase(BaseTestCase):

    def test_list_views_deletar_objeto(self):
        for m in CADASTRO_MODELS:
            if m == 'fornecedor':
                url = reverse('cadastro:listafornecedoresview')
            else:
                url = reverse('cadastro:lista{}sview'.format(m))

            # Testar GET request lista
            model_class = eval(m.title())
            obj = model_class.objects.create()
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(obj in response.context['object_list'])

            # Deletar objeto criado por POST request
            data = {
                obj.pk: 'on',
            }
            response = self.client.post(url, data, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(obj in response.context['object_list'])

        url = reverse('cadastro:listaprodutosbaixoestoqueview')

        # Testar GET request lista
        obj = Produto.objects.create()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(obj in response.context['object_list'])

        # Deletar objeto criado por POST request
        data = {
            obj.pk: 'on',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(obj in response.context['object_list'])


class CadastroEditarViewsTestCase(BaseTestCase):

    def test_edit_views_get_request(self):
        for m in CADASTRO_MODELS:
            # Buscar objeto qualquer
            obj = eval(m.title()).objects.order_by('pk').first()
            url = reverse('cadastro:editar{}view'.format(m),
                          kwargs={'pk': obj.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
