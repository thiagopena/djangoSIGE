# -*- coding: utf-8 -*-

from djangosige.tests.test_case import BaseTestCase, replace_none_values_in_dictionary
from djangosige.apps.cadastro.models import Produto, Unidade, Marca, Categoria, Transportadora, Fornecedor, Cliente, Empresa
from django.urls import reverse


CADASTRO_MODELS = (
    Empresa,
    Cliente,
    Fornecedor,
    Transportadora,
    Produto,
    Categoria,
    Unidade,
    Marca,
)

PESSOA_MODELS = (
    Empresa,
    Cliente,
    Fornecedor,
    Transportadora,
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
        for model in CADASTRO_MODELS:
            model_name = model.__name__.lower()
            url = reverse('djangosige.apps.cadastro:add{}view'.format(model_name))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

            # Testar permissao
            permission_codename = 'add_' + str(model_name)
            self.check_user_get_permission(
                url, permission_codename=permission_codename)

    def test_add_pessoa_post_request(self):
        for model in PESSOA_MODELS:
            model_name = model.__name__.lower()
            url = reverse('djangosige.apps.cadastro:add{}view'.format(model_name))
            pessoa_data = {
                '{}_form-nome_razao_social'.format(model_name): 'Razao Social Qualquer',
                '{}_form-tipo_pessoa'.format(model_name): 'PJ',
                '{}_form-inscricao_municipal'.format(model_name): '',
                '{}_form-informacoes_adicionais'.format(model_name): '',
            }

            if model_name == 'cliente':
                pessoa_data['cliente_form-limite_de_credito'] = '0.00'
                pessoa_data['cliente_form-indicador_ie'] = '1'
                pessoa_data['cliente_form-id_estrangeiro'] = ''
            elif model_name == 'transportadora':
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
            pessoa_data['{}_form-nome_razao_social'.format(model_name)] = ''
            response = self.client.post(url, pessoa_data, follow=True)
            self.assertFormError(
                response, 'form', 'nome_razao_social', 'Este campo é obrigatório.')

    def test_add_produto_post_request(self):
        url = reverse('djangosige.apps.cadastro:addprodutoview')
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
        url = reverse('djangosige.apps.cadastro:addcategoriaview')
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
        url = reverse('djangosige.apps.cadastro:addmarcaview')
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
        url = reverse('djangosige.apps.cadastro:addunidadeview')
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
        for model in CADASTRO_MODELS:
            model_name = model.__name__.lower()
            if model_name == 'fornecedor':
                url = reverse('djangosige.apps.cadastro:listafornecedoresview')
            else:
                url = reverse('djangosige.apps.cadastro:lista{}sview'.format(model_name))

            obj = model.objects.create()
            self.check_list_view_delete(url=url, deleted_object=obj)

        url = reverse('djangosige.apps.cadastro:listaprodutosbaixoestoqueview')
        obj = Produto.objects.create()
        self.check_list_view_delete(url=url, deleted_object=obj)


class CadastroEditarViewsTestCase(BaseTestCase):

    def test_edit_pessoa_get_post_request(self):
        for model in PESSOA_MODELS:
            # Buscar objeto qualquer
            model_name = model.__name__.lower()
            obj = model.objects.order_by('pk').last()
            url = reverse('djangosige.apps.cadastro:editar{}view'.format(model_name),
                          kwargs={'pk': obj.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            data = response.context['form'].initial
            if model_name == 'cliente':
                data['{}-limite_de_credito'.format(response.context['form'].prefix)] = data[
                    'limite_de_credito']
                del data['limite_de_credito']
            elif model_name == 'transportadora':
                data['veiculo_form-TOTAL_FORMS'] = 1
                data['veiculo_form-INITIAL_FORMS'] = 0
                data['veiculo_form-0-descricao'] = 'Veiculo1'
                data['veiculo_form-0-placa'] = 'XXXXXXXX'
                data['veiculo_form-0-uf'] = 'SP'

            # Inserir informacoes adicionais
            data['informacoes_adicionais'] = 'Objeto editado.'
            data.update(INLINE_FORMSET_DATA)
            response = self.client.post(url, data, follow=True)
            self.assertEqual(response.status_code, 200)

            # Assert form invalido
            data[
                '{}_form-nome_razao_social'.format(response.context['form'].prefix)] = ''
            response = self.client.post(url, data, follow=True)
            self.assertFormError(
                response, 'form', 'nome_razao_social', 'Este campo é obrigatório.')

    def test_edit_produto_get_post_request(self):
        # Buscar objeto qualquer
        obj = Produto.objects.order_by('pk').last()
        url = reverse('djangosige.apps.cadastro:editarprodutoview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        replace_none_values_in_dictionary(data)
        data['inf_adicionais'] = 'Produto editado.'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro/produto/produto_list.html')

    def test_edit_categoria_get_post_request(self):
        # Buscar objeto qualquer
        obj = Categoria.objects.order_by('pk').last()
        url = reverse('djangosige.apps.cadastro:editarcategoriaview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        data['categoria_desc'] = 'Categoria Editada'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Assert form invalido
        data['categoria_desc'] = ''
        response = self.client.post(url, data, follow=True)
        self.assertFormError(
            response, 'form', 'categoria_desc', 'Este campo é obrigatório.')

    def test_edit_marca_get_post_request(self):
        # Buscar objeto qualquer
        obj = Marca.objects.order_by('pk').last()
        url = reverse('djangosige.apps.cadastro:editarmarcaview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        data['marca_desc'] = 'Marca Editada'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_unidade_get_post_request(self):
        # Buscar objeto qualquer
        obj = Unidade.objects.order_by('pk').last()
        url = reverse('djangosige.apps.cadastro:editarunidadeview',
                      kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.context['form'].initial
        data['unidade_desc'] = 'Unidade Editada'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)


class CadastroAjaxRequestViewsTestCase(BaseTestCase):

    def test_info_cliente_post_request(self):
        # Buscar objeto qualquer
        obj = Cliente.objects.order_by('pk').last()
        obj_pk = obj.pk
        url = reverse('djangosige.apps.cadastro:infocliente')
        data = {'pessoaId': obj_pk}
        self.check_json_response(url, data, obj_pk, model='cadastro.cliente')

    def test_info_transportadora_post_request(self):
        # Buscar objeto qualquer
        obj = Transportadora.objects.order_by('pk').last()
        obj_pk = obj.pk
        url = reverse('djangosige.apps.cadastro:infotransportadora')
        data = {'transportadoraId': obj_pk}
        self.check_json_response(
            url, data, obj_pk, model='cadastro.transportadora')

    def test_info_fornecedor_post_request(self):
        # Buscar objeto qualquer
        obj = Fornecedor.objects.order_by('pk').last()
        obj_pk = obj.pk
        url = reverse('djangosige.apps.cadastro:infofornecedor')
        data = {'pessoaId': obj_pk}
        self.check_json_response(
            url, data, obj_pk, model='cadastro.fornecedor')

    def test_info_produto_post_request(self):
        # Buscar objeto qualquer
        obj = Produto.objects.order_by('pk').last()
        obj_pk = obj.pk
        url = reverse('djangosige.apps.cadastro:infoproduto')
        data = {'produtoId': obj_pk}
        self.check_json_response(url, data, obj_pk, model='cadastro.produto')
