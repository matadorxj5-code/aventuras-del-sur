from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cuentas.roles import GRUPO_ADMINISTRADOR, GRUPO_GUIA, GRUPO_TURISTA
from core.models import ConfiguracionParque
from .models import Categoria, Experiencia, Reserva


class RecorridosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('configurar_roles', verbosity=0)
        for atributo, rol in [('administrador', GRUPO_ADMINISTRADOR), ('guia', GRUPO_GUIA), ('otro_guia', GRUPO_GUIA), ('turista', GRUPO_TURISTA), ('otro_turista', GRUPO_TURISTA)]:
            usuario = User.objects.create_user(atributo)
            usuario.groups.add(Group.objects.get(name=rol))
            setattr(cls, atributo, usuario)
        categoria = Categoria.objects.create(nombre='Trekking', descripcion='Senderos')
        cls.experiencia = Experiencia.objects.create(titulo='Actividad propia', descripcion='Sendero', precio=2500, cupo_maximo=20, fecha_hora=timezone.now()+timedelta(days=1), categoria=categoria, creador=cls.guia)
        cls.reserva = Reserva.objects.create(usuario=cls.turista, experiencia=cls.experiencia)

    def test_guia_accede_solo_a_su_grupo_y_asistencia(self):
        url = reverse('grupo', args=[self.experiencia.pk])
        asistencia = reverse('registrar_visitante', args=[self.reserva.pk])
        self.client.force_login(self.otro_guia)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.post(asistencia, {'asistencia': 'si'}).status_code, 404)
        self.client.force_login(self.guia)
        self.assertContains(self.client.get(url), self.turista.username)
        self.assertEqual(self.client.post(asistencia, {'asistencia': 'si'}).status_code, 302)
        self.reserva.refresh_from_db()
        self.assertTrue(self.reserva.asistencia)
        self.client.force_login(self.turista)
        self.assertEqual(self.client.get(url).status_code, 403)
        self.assertEqual(self.client.post(asistencia, {'asistencia': 'no'}).status_code, 403)

    def test_ticket_privado_y_pago_confirmado(self):
        url = reverse('ticket', args=[self.reserva.pk])
        self.client.force_login(self.otro_turista)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.client.force_login(self.turista)
        self.assertContains(self.client.get(url), 'Pendiente')
        self.reserva.estado_pago = Reserva.CONFIRMADO
        self.reserva.save()
        self.assertContains(self.client.get(url), 'El pago de esta reserva esta confirmado.')

    def test_valoracion_solo_propia_y_despues_de_actividad(self):
        url = reverse('valorar', args=[self.reserva.pk])
        self.client.force_login(self.otro_turista)
        self.assertEqual(self.client.post(url, {'valoracion': 5}).status_code, 404)
        self.client.force_login(self.turista)
        self.assertEqual(self.client.post(url, {'valoracion': 5}).status_code, 302)
        self.reserva.refresh_from_db()
        self.assertIsNone(self.reserva.valoracion)
        self.experiencia.fecha_hora = timezone.now()-timedelta(days=1)
        self.experiencia.save()
        self.client.post(url, {'valoracion': 6, 'comentario': 'Prueba'})
        self.reserva.refresh_from_db()
        self.assertIsNone(self.reserva.valoracion)
        self.client.post(url, {'valoracion': 5, 'comentario': 'Buena actividad'})
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.valoracion, 5)

    def test_calendario_solo_actividades_propias(self):
        self.client.force_login(self.guia)
        mes = timezone.localtime(self.experiencia.fecha_hora).strftime('%Y-%m')
        response = self.client.get(reverse('calendario'), {'mes': mes})
        self.assertContains(response, self.experiencia.titulo)
        self.client.force_login(self.otro_guia)
        self.assertNotContains(self.client.get(reverse('calendario'), {'mes': mes}), self.experiencia.titulo)
        self.assertEqual(self.client.get(reverse('calendario'), {'mes': 'invalido'}).status_code, 400)

    def test_perfil_no_permite_cambiar_rol(self):
        self.client.force_login(self.turista)
        self.client.post(reverse('mi_perfil'), {'first_name': 'Nuevo', 'last_name': 'Nombre', 'email': 'prueba@example.test', 'is_superuser': 'on', 'grupo': self.administrador.groups.first().pk})
        self.turista.refresh_from_db()
        self.assertEqual(self.turista.first_name, 'Nuevo')
        self.assertFalse(self.turista.is_superuser)
        self.assertEqual(self.turista.perfil.rol.name, GRUPO_TURISTA)

    def test_configuracion_y_reportes_solo_admin(self):
        for usuario in [self.guia, self.turista]:
            self.client.force_login(usuario)
            self.assertEqual(self.client.get(reverse('configuracion_parque')).status_code, 403)
            self.assertEqual(self.client.get(reverse('reportes')).status_code, 403)
        self.client.force_login(self.administrador)
        self.client.post(reverse('configuracion_parque'), {'nombre': 'Aventuras del Sur', 'descripcion': 'Descripcion actualizada', 'contacto': 'parque@example.test'})
        self.assertEqual(ConfiguracionParque.objects.get().descripcion, 'Descripcion actualizada')
        response = self.client.get(reverse('reportes'))
        self.assertEqual(response.context['resumen']['total'], 1)
        self.client.logout()
        self.assertContains(self.client.get(reverse('inicio')), 'Descripcion actualizada')

    def test_detalle_oculto_solo_para_responsable_o_reserva_propia(self):
        self.experiencia.estado = False
        self.experiencia.save()
        url = reverse('experiencia_detalle', args=[self.experiencia.pk])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.client.force_login(self.otro_turista)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.client.force_login(self.turista)
        self.assertEqual(self.client.get(url).status_code, 200)
