import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


def user_directory_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return f"imagens/usuarios/fotos_perfil/{instance.user.username}_{instance.user.id}{extension}"


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_foto = models.ImageField(
        upload_to=user_directory_path, default="imagens/user.png", blank=True
    )

    def save(self, *args, **kwargs):
        # Deletar user_foto se ja existir uma
        try:
            obj = Usuario.objects.get(id=self.id)
            if obj.user_foto != self.user_foto and obj.user_foto != "imagens/user.png":
                obj.user_foto.delete(save=False)
        except:
            pass

        super().save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % self.user

    def __str__(self):
        return "%s" % self.user


@receiver(post_delete, sender=Usuario)
def foto_post_delete_handler(sender, instance, **kwargs):
    # Nao deletar a imagem default 'user.png'
    if instance.user_foto != "imagens/user.png":
        instance.user_foto.delete(False)
