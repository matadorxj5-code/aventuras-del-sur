from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from cuentas.roles import (
    GRUPO_ADMINISTRADOR,
    GRUPO_GUIA,
    GRUPO_TURISTA,
)


class Command(BaseCommand):
    help = 'Crea los grupos del sistema y les asigna sus permisos'

    def handle(self, *args, **options):
        administrador, _ = Group.objects.get_or_create(
            name=GRUPO_ADMINISTRADOR
        )

        guia, _ = Group.objects.get_or_create(
            name=GRUPO_GUIA
        )

        turista, _ = Group.objects.get_or_create(
            name=GRUPO_TURISTA
        )

        administrador.permissions.clear()
        guia.permissions.clear()
        turista.permissions.clear()

        permisos_administrador = Permission.objects.filter(
            content_type__app_label__in=[
                'auth',
                'experiencias',
            ],
            content_type__model__in=[
                'user',
                'categoria',
                'experiencia',
                'reserva',
            ]
        )

        permisos_guia = Permission.objects.filter(
            content_type__app_label='experiencias',
            codename__in=[
                'add_experiencia',
                'view_experiencia',
                'change_experiencia',
            ]
        )

        permisos_turista = Permission.objects.filter(
            content_type__app_label='experiencias',
            codename__in=[
                'add_reserva',
                'view_reserva',
                'delete_reserva',
            ]
        )

        administrador.permissions.set(
            permisos_administrador
        )

        guia.permissions.set(
            permisos_guia
        )

        turista.permissions.set(
            permisos_turista
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Los grupos y permisos fueron configurados correctamente.'
            )
        )
