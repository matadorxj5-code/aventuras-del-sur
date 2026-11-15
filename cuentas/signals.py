from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .models import Perfil
from .roles import GRUPO_ADMINISTRADOR, GRUPO_GUIA, GRUPO_TURISTA


def sincronizar_perfil(usuario, using):
    nombres = [GRUPO_ADMINISTRADOR, GRUPO_GUIA, GRUPO_TURISTA]
    grupos = dict(usuario.groups.using(using).filter(name__in=nombres).values_list('name', 'pk'))
    rol_id = next((grupos[nombre] for nombre in nombres if nombre in grupos), None)
    if usuario.is_superuser:
        rol_id = Group.objects.using(using).get_or_create(name=GRUPO_ADMINISTRADOR)[0].pk
    perfil, _ = Perfil.objects.using(using).update_or_create(usuario=usuario, defaults={'rol_id': rol_id})
    usuario.perfil = perfil


@receiver(post_save, sender=get_user_model())
def crear_perfil(sender, instance, raw, using, **kwargs):
    if not raw:
        sincronizar_perfil(instance, using)


@receiver(m2m_changed, sender=get_user_model().groups.through)
def actualizar_rol(sender, instance, action, reverse, pk_set, using, **kwargs):
    if reverse and action == 'pre_clear':
        instance._usuarios_perfil = list(instance.user_set.using(using).values_list('pk', flat=True))
    if action not in {'post_add', 'post_remove', 'post_clear'}:
        return
    if reverse:
        ids = pk_set if pk_set is not None else getattr(instance, '_usuarios_perfil', [])
        for usuario in get_user_model().objects.using(using).filter(pk__in=ids):
            sincronizar_perfil(usuario, using)
    else:
        sincronizar_perfil(instance, using)
