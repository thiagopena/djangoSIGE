# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse
from django.core import serializers

from djangosige.apps.cadastro.models import Pessoa, Cliente, Fornecedor, Transportadora, Produto
from djangosige.apps.fiscal.models import ICMS, ICMSSN, IPI, ICMSUFDest


class InfoCliente(View):

    def post(self, request, *args, **kwargs):
        obj_list = []
        pessoa = Pessoa.objects.get(pk=request.POST['pessoaId'])
        cliente = Cliente.objects.get(pk=request.POST['pessoaId'])
        obj_list.append(cliente)

        if pessoa.endereco_padrao:
            obj_list.append(pessoa.endereco_padrao)
        if pessoa.email_padrao:
            obj_list.append(pessoa.email_padrao)
        if pessoa.telefone_padrao:
            obj_list.append(pessoa.telefone_padrao)

        if pessoa.tipo_pessoa == 'PJ':
            obj_list.append(pessoa.pessoa_jur_info)
        elif pessoa.tipo_pessoa == 'PF':
            obj_list.append(pessoa.pessoa_fis_info)

        data = serializers.serialize('json', obj_list, fields=('indicador_ie', 'limite_de_credito', 'cnpj', 'inscricao_estadual', 'responsavel', 'cpf', 'rg', 'id_estrangeiro', 'logradouro', 'numero', 'bairro',
                                                               'municipio', 'cmun', 'uf', 'pais', 'complemento', 'cep', 'email', 'telefone',))

        return HttpResponse(data, content_type='application/json')


class InfoFornecedor(View):

    def post(self, request, *args, **kwargs):
        obj_list = []
        pessoa = Pessoa.objects.get(pk=request.POST['pessoaId'])
        fornecedor = Fornecedor.objects.get(pk=request.POST['pessoaId'])
        obj_list.append(fornecedor)

        if pessoa.endereco_padrao:
            obj_list.append(pessoa.endereco_padrao)
        if pessoa.email_padrao:
            obj_list.append(pessoa.email_padrao)
        if pessoa.telefone_padrao:
            obj_list.append(pessoa.telefone_padrao)

        if pessoa.tipo_pessoa == 'PJ':
            obj_list.append(pessoa.pessoa_jur_info)
        elif pessoa.tipo_pessoa == 'PF':
            obj_list.append(pessoa.pessoa_fis_info)

        data = serializers.serialize('json', obj_list, fields=('indicador_ie', 'limite_de_credito', 'cnpj', 'inscricao_estadual', 'responsavel', 'cpf', 'rg', 'id_estrangeiro', 'logradouro', 'numero', 'bairro',
                                                               'municipio', 'cmun', 'uf', 'pais', 'complemento', 'cep', 'email', 'telefone',))

        return HttpResponse(data, content_type='application/json')


class InfoEmpresa(View):

    def post(self, request, *args, **kwargs):
        pessoa = Pessoa.objects.get(pk=request.POST['pessoaId'])
        obj_list = []
        obj_list.append(pessoa.pessoa_jur_info)

        if pessoa.endereco_padrao:
            obj_list.append(pessoa.endereco_padrao)

        data = serializers.serialize('json', obj_list, fields=('cnpj', 'inscricao_estadual', 'logradouro', 'numero', 'bairro',
                                                               'municipio', 'cmun', 'uf', 'pais', 'complemento', 'cep',))

        return HttpResponse(data, content_type='application/json')


class InfoTransportadora(View):

    def post(self, request, *args, **kwargs):
        veiculos = Transportadora.objects.get(
            pk=request.POST['transportadoraId']).veiculo.all()
        data = serializers.serialize(
            'json', veiculos, fields=('id', 'descricao',))

        return HttpResponse(data, content_type='application/json')


class InfoProduto(View):

    def post(self, request, *args, **kwargs):
        obj_list = []
        pro = Produto.objects.get(pk=request.POST['produtoId'])
        obj_list.append(pro)

        if pro.grupo_fiscal:
            if pro.grupo_fiscal.regime_trib == '0':
                icms, created = ICMS.objects.get_or_create(
                    grupo_fiscal=pro.grupo_fiscal)
            else:
                icms, created = ICMSSN.objects.get_or_create(
                    grupo_fiscal=pro.grupo_fiscal)

            ipi, created = IPI.objects.get_or_create(
                grupo_fiscal=pro.grupo_fiscal)
            icms_dest, created = ICMSUFDest.objects.get_or_create(
                grupo_fiscal=pro.grupo_fiscal)
            obj_list.append(icms)
            obj_list.append(ipi)
            obj_list.append(icms_dest)

        data = serializers.serialize('json', obj_list, fields=('venda', 'controlar_estoque', 'estoque_atual',
                                                               'tipo_ipi', 'p_ipi', 'valor_fixo', 'p_icms', 'p_red_bc', 'p_icmsst', 'p_red_bcst', 'p_mvast',
                                                               'p_fcp_dest', 'p_icms_dest', 'p_icms_inter', 'p_icms_inter_part',
                                                               'ipi_incluido_preco', 'incluir_bc_icms', 'incluir_bc_icmsst', 'icmssn_incluido_preco',
                                                               'icmssnst_incluido_preco', 'icms_incluido_preco', 'icmsst_incluido_preco'))
        return HttpResponse(data, content_type='application/json')
