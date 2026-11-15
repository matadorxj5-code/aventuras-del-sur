from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier
from unittest import skipUnless

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.db import IntegrityError, close_old_connections, connection, transaction
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from cuentas.roles import GRUPO_GUIA, GRUPO_TURISTA
from .forms import ExperienciaForm
from .models import Categoria, Experiencia, Reserva


class ExperienciaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('configurar_roles', verbosity=0)
        cls.guia = User.objects.create_user('guia_prueba')
        cls.guia.groups.add(Group.objects.get(name=GRUPO_GUIA))
        cls.turista = User.objects.create_user('turista_prueba')
        cls.turista.groups.add(Group.objects.get(name=GRUPO_TURISTA))
        cls.categoria = Categoria.objects.create(nombre='Trekking', descripcion='Senderos')
        cls.experiencia = Experiencia.objects.create(
            titulo='Caminata', descripcion='Sendero guiado', precio=2500,
            cupo_maximo=2, fecha_hora=timezone.now() + timedelta(days=10),
            categoria=cls.categoria, creador=cls.guia,
        )

    def datos(self, cupo=2):
        return {
            'titulo': self.experiencia.titulo, 'descripcion': 'Sendero guiado',
            'precio': 2500, 'cupo_maximo': cupo, 'categoria': self.categoria.pk,
            'fecha_hora': timezone.localtime(self.experiencia.fecha_hora).strftime('%Y-%m-%dT%H:%M'),
            'estado': 'on',
        }

    def test_cupo_cero_rechazado_en_formulario(self):
        form = ExperienciaForm(self.datos(0))
        self.assertFalse(form.is_valid())
        self.assertIn('cupo_maximo', form.errors)

    def test_cupo_cero_rechazado_en_base(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Experiencia.objects.filter(pk=self.experiencia.pk).update(cupo_maximo=0)

    def test_no_reduce_cupo_por_debajo_de_reservas(self):
        otro = User.objects.create_user('otro_turista')
        for usuario in [self.turista, otro]:
            Reserva.objects.create(usuario=usuario, experiencia=self.experiencia)
        self.client.force_login(self.guia)
        response = self.client.post(reverse('experiencia_editar', args=[self.experiencia.pk]), self.datos(1))
        self.assertEqual(response.status_code, 200)
        self.assertIn('cupo_maximo', response.context['formulario'].errors)
        self.experiencia.refresh_from_db()
        self.assertEqual(self.experiencia.cupo_maximo, 2)
        self.assertTrue(ExperienciaForm(self.datos(2), instance=self.experiencia).is_valid())

    def test_catalogo_publico_y_filtros(self):
        self.assertEqual(self.client.get(reverse('inicio')).status_code, 200)
        url = reverse('catalogo_experiencias')
        self.assertContains(self.client.get(url), 'Caminata')
        for cambios in [{'estado': False}, {'fecha_hora': timezone.now() - timedelta(days=1)}]:
            with transaction.atomic():
                Experiencia.objects.filter(pk=self.experiencia.pk).update(**cambios)
                self.assertNotContains(self.client.get(url), 'Caminata')
                transaction.set_rollback(True)
        self.categoria.estado = False
        self.categoria.save()
        self.assertNotContains(self.client.get(url), 'Caminata')

    def test_reserva_inactiva_rechazada_y_reservas_anteriores_conservadas(self):
        Reserva.objects.create(usuario=self.guia, experiencia=self.experiencia)
        self.experiencia.estado = False
        self.experiencia.save()
        self.client.force_login(self.turista)
        self.client.post(reverse('reserva_crear', args=[self.experiencia.pk]))
        self.assertEqual(self.experiencia.reservas.count(), 1)
        self.assertFalse(self.experiencia.reservas.filter(usuario=self.turista).exists())

    def test_guia_no_edita_experiencia_ajena(self):
        otro = User.objects.create_user('otro_guia')
        otro.groups.add(Group.objects.get(name=GRUPO_GUIA))
        self.client.force_login(otro)
        url = reverse('experiencia_editar', args=[self.experiencia.pk])
        self.assertEqual(self.client.post(url, self.datos()).status_code, 404)

    def test_anonimo_no_reserva(self):
        response = self.client.post(reverse('reserva_crear', args=[self.experiencia.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reserva.objects.count(), 0)

    def test_reserva_duplicada_y_sin_cupo(self):
        self.experiencia.cupo_maximo = 1
        self.experiencia.save()
        self.client.force_login(self.turista)
        url = reverse('reserva_crear', args=[self.experiencia.pk])
        self.client.post(url)
        self.client.post(url)
        otro = User.objects.create_user('otro_turista')
        otro.groups.add(Group.objects.get(name=GRUPO_TURISTA))
        self.client.force_login(otro)
        self.client.post(url)
        self.assertEqual(self.experiencia.reservas.count(), 1)


@skipUnless(connection.vendor == 'mysql', 'Requiere bloqueos de MySQL')
class ConcurrenciaReservasTests(TransactionTestCase):
    def test_dos_turistas_compiten_por_un_cupo(self):
        call_command('configurar_roles', verbosity=0)
        guia = User.objects.create_user('guia_concurrencia')
        categoria = Categoria.objects.create(nombre='Kayak', descripcion='Agua')
        experiencia = Experiencia.objects.create(
            titulo='Ultimo cupo', descripcion='Prueba', precio=2500, cupo_maximo=1,
            fecha_hora=timezone.now() + timedelta(days=10), categoria=categoria, creador=guia,
        )
        clientes = []
        for numero in range(2):
            usuario = User.objects.create_user(f'turista_concurrencia_{numero}')
            usuario.groups.add(Group.objects.get(name=GRUPO_TURISTA))
            cliente = Client()
            cliente.force_login(usuario)
            clientes.append(cliente)
        barrera = Barrier(2)

        def reservar(cliente):
            close_old_connections()
            try:
                barrera.wait(timeout=10)
                return cliente.post(reverse('reserva_crear', args=[experiencia.pk])).status_code
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as executor:
            resultados = list(executor.map(reservar, clientes))
        self.assertEqual(resultados, [302, 302])
        self.assertEqual(experiencia.reservas.count(), 1)
