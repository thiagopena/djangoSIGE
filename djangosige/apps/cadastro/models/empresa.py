# -*- coding: utf-8 -*-

import os

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .base import Pessoa
from djangosige.apps.login.models import Usuario
from djangosige.configs.settings import MEDIA_ROOT


def logo_directory_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return 'imagens/empresas/logo_{0}_{1}{2}'.format(instance.nome_razao_social, instance.id, extension)


class Empresa(Pessoa):
    logo_file = models.ImageField(
        upload_to=logo_directory_path, default='imagens/logo.png', blank=True, null=True)
    cnae = models.CharField(max_length=10, blank=True, null=True)
    iest = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = "Empresa"

    @property
    def caminho_completo_logo(self):
        if self.logo_file.name != 'imagens/logo.png':
            return os.path.join(MEDIA_ROOT, self.logo_file.name)
        else:
            return ''

    def save(self, *args, **kwargs):
        # Deletar logo se ja existir um
        try:
            obj = Empresa.objects.get(id=self.id)
            if obj.logo_file != self.logo_file and obj.logo_file != 'imagens/logo.png':
                obj.logo_file.delete(save=False)
        except:
            pass
        super(Empresa, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.nome_razao_social

    def __str__(self):
        return u'%s' % self.nome_razao_social

# Deletar logo quando empresa for deletada


@receiver(post_delete, sender=Empresa)
def logo_post_delete_handler(sender, instance, **kwargs):
    # Nao deletar a imagem default 'logo.png'
    if instance.logo_file != 'imagens/logo.png':
        instance.logo_file.delete(False)


class MinhaEmpresa(models.Model):
    m_empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name='minha_empresa', blank=True, null=True)
    m_usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='empresa_usuario')
