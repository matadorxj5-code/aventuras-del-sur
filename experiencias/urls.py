from django.urls import path

from . import views
from . import recorridos


urlpatterns = [
    path('calendario/', recorridos.calendario, name='calendario'),
    path('<int:experiencia_id>/detalle/', recorridos.experiencia_detalle, name='experiencia_detalle'),
    path('<int:experiencia_id>/grupo/', recorridos.grupo, name='grupo'),
    path('reservas/<int:reserva_id>/asistencia/', recorridos.registrar_visitante, name='registrar_visitante'),
    path('reservas/<int:reserva_id>/ticket/', recorridos.ticket, name='ticket'),
    path('reservas/<int:reserva_id>/valorar/', recorridos.valorar, name='valorar'),
                
    path(
        'categorias/',
        views.categoria_lista,
        name='categoria_lista'
    ),

    path(
        'categorias/crear/',
        views.categoria_crear,
        name='categoria_crear'
    ),

    path(
        'categorias/<int:categoria_id>/editar/',
        views.categoria_editar,
        name='categoria_editar'
    ),

    path(
        'categorias/<int:categoria_id>/eliminar/',
        views.categoria_eliminar,
        name='categoria_eliminar'
    ),

                  
    path(
        '',
        views.experiencia_lista,
        name='experiencia_lista'
    ),

    path(
        'crear/',
        views.experiencia_crear,
        name='experiencia_crear'
    ),

    path(
        '<int:experiencia_id>/editar/',
        views.experiencia_editar,
        name='experiencia_editar'
    ),

    path(
        '<int:experiencia_id>/eliminar/',
        views.experiencia_eliminar,
        name='experiencia_eliminar'
    ),


    path(
        'catalogo/',
        views.catalogo_experiencias,
        name='catalogo_experiencias'
    ),
    

    path(
        'reservas/',
        views.reserva_lista,
        name='reserva_lista'
    ),

    path(
        'reservas/crear/<int:experiencia_id>/',
        views.reserva_crear,
        name='reserva_crear'
    ),

    path(
        'reservas/<int:reserva_id>/estado/',
        views.reserva_cambiar_estado,
        name='reserva_cambiar_estado'
    ),

    path(
        'reservas/<int:reserva_id>/eliminar/',
        views.reserva_eliminar,
        name='reserva_eliminar'
    ),
]
