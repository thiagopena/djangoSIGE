# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _
from djangosige.apps.fiscal.models import GrupoFiscal, ICMS, ICMSSN, ICMSUFDest, IPI, PIS, COFINS


class GrupoFiscalForm(forms.ModelForm):

    class Meta:
        model = GrupoFiscal
        fields = ('descricao', 'regime_trib',)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'title': 'Insira uma breve descrição do grupo fiscal, EX: ICMS (Simples Nacional) + IPI'}),
            'regime_trib': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao': _('Descrição'),
            'regime_trib': _('Regime Tributário'),
        }


class ICMSForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = ICMS.objects.get(grupo_fiscal=grupo_fiscal)
            super(ICMSForm, self).__init__(instance=instance, *args, **kwargs)
        else:
            super(ICMSForm, self).__init__(*args, **kwargs)

        self.fields['cst'].required = False

        self.fields['p_icms'].localize = True
        self.fields['p_red_bc'].localize = True
        self.fields['p_mvast'].localize = True
        self.fields['p_red_bcst'].localize = True
        self.fields['p_icmsst'].localize = True
        self.fields['p_dif'].localize = True
        self.fields['p_bc_op'].localize = True

    class Meta:
        model = ICMS
        fields = ('cst', 'mod_bc', 'p_icms', 'p_red_bc', 'mod_bcst', 'p_mvast', 'p_red_bcst', 'p_icmsst', 'mot_des_icms',
                  'p_dif', 'p_bc_op', 'ufst', 'icms_incluido_preco', 'icmsst_incluido_preco', )
        widgets = {
            'cst': forms.Select(attrs={'class': 'form-control'}),
            'mod_bc': forms.Select(attrs={'class': 'form-control'}),
            'p_icms': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_red_bc': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'mod_bcst': forms.Select(attrs={'class': 'form-control'}),
            'p_mvast': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_red_bcst': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_icmsst': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'mot_des_icms': forms.Select(attrs={'class': 'form-control'}),
            'p_dif': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_bc_op': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'ufst': forms.Select(attrs={'class': 'form-control'}),
            'icms_incluido_preco': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'icmsst_incluido_preco': forms.CheckboxInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'cst': _('CST ICMS'),
            'mod_bc': _('Modalidade de determinação da BC do ICMS'),
            'p_icms': _('Alíquota ICMS'),
            'p_red_bc': _('% da Redução de BC'),
            'mod_bcst': _('Modalidade de determinação da BC do ICMS ST'),
            'p_mvast': _('% Margem de valor Adicionado do ICMS ST'),
            'p_red_bcst': _('% da Redução de BC do ICMS ST'),
            'p_icmsst': _('Alíquota ICMS ST'),
            'mot_des_icms': _('Motivo da desoneração do ICMS'),
            'p_dif': _('% do diferimento'),
            'p_bc_op': _('% da BC operação própria'),
            'ufst': _('UF para qual é devido o ICMS ST'),
            'icms_incluido_preco': _('ICMS incluso no preço'),
            'icmsst_incluido_preco': _('ICMS-ST incluso no preço'),
        }


class ICMSSNForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = ICMSSN.objects.get(grupo_fiscal=grupo_fiscal)
            super(ICMSSNForm, self).__init__(
                instance=instance, *args, **kwargs)
        else:
            super(ICMSSNForm, self).__init__(*args, **kwargs)

        self.fields['csosn'].required = False

        self.fields['p_cred_sn'].localize = True
        self.fields['p_icms'].localize = True
        self.fields['p_red_bc'].localize = True
        self.fields['p_mvast'].localize = True
        self.fields['p_red_bcst'].localize = True
        self.fields['p_icmsst'].localize = True

    class Meta:
        model = ICMSSN
        fields = ('csosn', 'p_cred_sn', 'p_icms', 'mod_bcst', 'mod_bc', 'p_red_bc', 'p_mvast', 'p_red_bcst', 'p_icmsst',
                  'icmssn_incluido_preco', 'icmssnst_incluido_preco',)
        widgets = {
            'csosn': forms.Select(attrs={'class': 'form-control'}),
            'p_cred_sn': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'mod_bc': forms.Select(attrs={'class': 'form-control'}),
            'p_icms': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_red_bc': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'mod_bcst': forms.Select(attrs={'class': 'form-control'}),
            'p_mvast': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_red_bcst': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_icmsst': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'icmssn_incluido_preco': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'icmssnst_incluido_preco': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'csosn': _('CSOSN'),
            'p_cred_sn': _('Alíquota aplicável de cálculo do crédito'),
            'mod_bc': _('Modalidade de determinação da BC do ICMS'),
            'p_icms': _('Alíquota ICMS'),
            'p_red_bc': _('% da Redução de BC'),
            'mod_bcst': _('Modalidade de determinação da BC do ICMS ST'),
            'p_mvast': _('% Margem de valor Adicionado do ICMS ST'),
            'p_red_bcst': _('% da Redução de BC do ICMS ST'),
            'p_icmsst': _('Alíquota ICMS ST'),
            'icmssn_incluido_preco': _('ICMS incluso no preço'),
            'icmssnst_incluido_preco': _('ICMS-ST incluso no preço'),
        }


class ICMSUFDestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = ICMSUFDest.objects.get(grupo_fiscal=grupo_fiscal)
            super(ICMSUFDestForm, self).__init__(
                instance=instance, *args, **kwargs)
        else:
            super(ICMSUFDestForm, self).__init__(*args, **kwargs)

        self.fields['p_fcp_dest'].localize = True
        self.fields['p_icms_dest'].localize = True
        self.fields['p_icms_inter'].localize = True
        self.fields['p_icms_inter_part'].localize = True

    class Meta:
        model = ICMSUFDest
        fields = ('p_fcp_dest', 'p_icms_dest',
                  'p_icms_inter', 'p_icms_inter_part', )
        widgets = {
            'p_fcp_dest': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_icms_dest': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'p_icms_inter': forms.Select(attrs={'class': 'form-control'}),
            'p_icms_inter_part': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'p_fcp_dest': _('% do ICMS relativo ao FCP de destino'),
            'p_icms_dest': _('Alíquota interna da UF de destino'),
            'p_icms_inter': _('Alíquota interestadual das UF envolvidas'),
            'p_icms_inter_part': _('% provisório de partilha do ICMS Interestadual'),
        }


class IPIForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = IPI.objects.get(grupo_fiscal=grupo_fiscal)
            super(IPIForm, self).__init__(instance=instance, *args, **kwargs)
        else:
            super(IPIForm, self).__init__(*args, **kwargs)

        self.fields['p_ipi'].localize = True
        self.fields['valor_fixo'].localize = True

    class Meta:
        model = IPI
        fields = ('cst', 'cl_enq', 'c_enq', 'cnpj_prod', 'tipo_ipi', 'p_ipi',
                  'valor_fixo', 'ipi_incluido_preco', 'incluir_bc_icms', 'incluir_bc_icmsst',)
        widgets = {
            'cst': forms.Select(attrs={'class': 'form-control'}),
            'cl_enq': forms.TextInput(attrs={'class': 'form-control'}),
            'c_enq': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj_prod': forms.TextInput(attrs={'class': 'form-control'}),
            'p_ipi': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'tipo_ipi': forms.Select(attrs={'class': 'form-control'}),
            'valor_fixo': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'ipi_incluido_preco': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'incluir_bc_icms': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'incluir_bc_icmsst': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'cst': _('CST IPI'),
            'cl_enq': _('Classe de enquadramento para Cigarros e Bebidas'),
            'c_enq': _('Código de Enquadramento Legal'),
            'cnpj_prod': _('CNPJ do produtor da mercadoria'),
            'p_ipi': _('Alíquota do IPI'),
            'tipo_ipi': _('Tipo de cáculo'),
            'valor_fixo': _('Vl. fixo IPI (por produto)'),
            'ipi_incluido_preco': _('IPI incluso no preço'),
            'incluir_bc_icms': _('Incluir IPI na BC do ICMS'),
            'incluir_bc_icmsst': _('Incluir IPI na BC do ICMS-ST'),
        }


class PISForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = PIS.objects.get(grupo_fiscal=grupo_fiscal)
            super(PISForm, self).__init__(instance=instance, *args, **kwargs)
        else:
            super(PISForm, self).__init__(*args, **kwargs)

        self.fields['p_pis'].localize = True
        self.fields['valiq_pis'].localize = True

    class Meta:
        model = PIS
        fields = ('cst', 'p_pis', 'valiq_pis',)
        widgets = {
            'cst': forms.Select(attrs={'class': 'form-control'}),
            'p_pis': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'valiq_pis': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
        }
        labels = {
            'cst': _('CST PIS'),
            'p_pis': _('Alíquota do PIS (em %)'),
            'valiq_pis': _('Alíquota do PIS por produto (em R$)'),
        }


class COFINSForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'grupo_fiscal' in kwargs:
            grupo_fiscal = kwargs.pop('grupo_fiscal')
            instance = COFINS.objects.get(grupo_fiscal=grupo_fiscal)
            super(COFINSForm, self).__init__(
                instance=instance, *args, **kwargs)
        else:
            super(COFINSForm, self).__init__(*args, **kwargs)

        self.fields['p_cofins'].localize = True
        self.fields['valiq_cofins'].localize = True

    class Meta:
        model = COFINS
        fields = ('cst', 'p_cofins', 'valiq_cofins',)
        widgets = {
            'cst': forms.Select(attrs={'class': 'form-control'}),
            'p_cofins': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'valiq_cofins': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
        }
        labels = {
            'cst': _('CST COFINS'),
            'p_cofins': _('Alíquota do COFINS (em %)'),
            'valiq_cofins': _('Alíquota do COFINS por produto (em R$)'),
        }
