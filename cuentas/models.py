from django.conf import settings
from django.db import models

from .roles import GRUPO_ADMINISTRADOR, GRUPO_GUIA, GRUPO_TURISTA


class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    rol = models.ForeignKey(
        'auth.Group',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'name__in': [GRUPO_ADMINISTRADOR, GRUPO_GUIA, GRUPO_TURISTA]},
    )

    def __str__(self):
        return self.usuario.username
