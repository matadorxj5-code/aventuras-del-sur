from django.contrib import admin

from .models import Categoria, Experiencia, Reserva


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'estado',
    )

    list_filter = (
        'estado',
    )

    search_fields = (
        'nombre',
    )


@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'titulo',
        'categoria',
        'precio',
        'cupo_maximo',
        'estado',
        'fecha_hora',
        'creador',
    )

    list_filter = (
        'categoria',
        'fecha_hora',
        'estado',
    )

    search_fields = (
        'titulo',
        'descripcion',
        'creador__username',
    )


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario',
        'experiencia',
        'fecha_inscripcion',
        'estado_pago',
    )

    list_filter = (
        'estado_pago',
        'fecha_inscripcion',
    )

    search_fields = (
        'usuario__username',
        'experiencia__titulo',
    )
