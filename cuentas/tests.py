from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase

from .forms import UsuarioCrearForm, UsuarioEditarForm
from .models import Perfil
from .roles import GRUPO_ADMINISTRADOR, GRUPO_GUIA, GRUPO_TURISTA


class PerfilTests(TestCase):
    def setUp(self):
        call_command('configurar_roles', verbosity=0)

    def test_perfil_sigue_creacion_y_edicion_del_rol(self):
        turista = Group.objects.get(name=GRUPO_TURISTA)
        guia = Group.objects.get(name=GRUPO_GUIA)
        form = UsuarioCrearForm({'username': 'nuevo_usuario', 'grupo': turista.pk,
                                 'password1': 'Ejemplo-fuerte-8721', 'password2': 'Ejemplo-fuerte-8721'})
        self.assertTrue(form.is_valid(), form.errors)
        usuario = form.save()
        self.assertEqual(usuario.perfil.rol_id, turista.pk)
        form = UsuarioEditarForm({'username': usuario.username, 'grupo': guia.pk, 'is_active': 'on'}, instance=usuario)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        usuario.perfil.refresh_from_db()
        self.assertEqual(usuario.perfil.rol_id, guia.pk)
        self.assertEqual(list(usuario.groups.values_list('pk', flat=True)), [guia.pk])

    def test_cambios_de_grupo_sincronizan_perfil(self):
        usuario = User.objects.create_user('prueba_rol')
        grupo = Group.objects.get(name=GRUPO_TURISTA)
        grupo.user_set.add(usuario)
        self.assertEqual(Perfil.objects.get(usuario=usuario).rol_id, grupo.pk)
        grupo.user_set.clear()
        self.assertIsNone(Perfil.objects.get(usuario=usuario).rol_id)
        usuario.groups.add(grupo)
        usuario.groups.clear()
        self.assertIsNone(Perfil.objects.get(usuario=usuario).rol_id)

    def test_superusuario_tiene_perfil_administrador(self):
        usuario = User.objects.create_superuser('admin_prueba', password='Ejemplo-fuerte-8721')
        self.assertEqual(usuario.perfil.rol.name, GRUPO_ADMINISTRADOR)
