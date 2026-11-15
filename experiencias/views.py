from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.db import transaction
from django.db.models import (
    Count,
    Exists,
    ExpressionWrapper,
    F,
    IntegerField,
    OuterRef,
)
from django.db.models.deletion import ProtectedError
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    CategoriaForm,
    ExperienciaForm,
)
from .models import (
    Categoria,
    Experiencia,
    Reserva,
)



@login_required
@permission_required(
    'experiencias.view_categoria',
    raise_exception=True
)
def categoria_lista(request):
    categorias = Categoria.objects.all()

    return render(
        request,
        'experiencias/categoria_lista.html',
        {
            'categorias': categorias,
        }
    )


@login_required
@permission_required(
    'experiencias.add_categoria',
    raise_exception=True
)
def categoria_crear(request):
    if request.method == 'POST':
        formulario = CategoriaForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                'La categoria fue creada correctamente.'
            )

            return redirect('categoria_lista')
    else:
        formulario = CategoriaForm()

    return render(
        request,
        'experiencias/categoria_formulario.html',
        {
            'formulario': formulario,
            'titulo': 'Crear categoria',
        }
    )


@login_required
@permission_required(
    'experiencias.change_categoria',
    raise_exception=True
)
def categoria_editar(request, categoria_id):
    categoria = get_object_or_404(
        Categoria,
        pk=categoria_id
    )

    if request.method == 'POST':
        formulario = CategoriaForm(
            request.POST,
            instance=categoria
        )

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                'La categoria fue actualizada correctamente.'
            )

            return redirect('categoria_lista')
    else:
        formulario = CategoriaForm(
            instance=categoria
        )

    return render(
        request,
        'experiencias/categoria_formulario.html',
        {
            'formulario': formulario,
            'titulo': 'Editar categoria',
        }
    )


@login_required
@permission_required(
    'experiencias.delete_categoria',
    raise_exception=True
)
@require_POST
def categoria_eliminar(request, categoria_id):
    categoria = get_object_or_404(
        Categoria,
        pk=categoria_id
    )

    try:
        categoria.delete()

        messages.success(
            request,
            'La categoria fue eliminada correctamente.'
        )

    except ProtectedError:
        messages.error(
            request,
            (
                'La categoria no se puede eliminar porque '
                'tiene experiencias asociadas.'
            )
        )

    return redirect('categoria_lista')



@login_required
@permission_required(
    'experiencias.view_experiencia',
    raise_exception=True
)
def experiencia_lista(request):
    experiencias = (
        Experiencia.objects
        .select_related('categoria', 'creador')
    )

    es_administrador = request.user.has_perm(
        'experiencias.delete_experiencia'
    )

    if not es_administrador:
        experiencias = experiencias.filter(
            creador=request.user
        )

    return render(
        request,
        'experiencias/experiencia_lista.html',
        {
            'experiencias': experiencias,
        }
    )


@login_required
@permission_required(
    'experiencias.add_experiencia',
    raise_exception=True
)
def experiencia_crear(request):
    if request.method == 'POST':
        formulario = ExperienciaForm(request.POST)

        if formulario.is_valid():
            experiencia = formulario.save(
                commit=False
            )

            experiencia.creador = request.user
            experiencia.save()

            messages.success(
                request,
                'La experiencia fue creada correctamente.'
            )

            return redirect('experiencia_lista')
    else:
        formulario = ExperienciaForm()

    return render(
        request,
        'experiencias/experiencia_formulario.html',
        {
            'formulario': formulario,
            'titulo': 'Crear experiencia',
        }
    )


@login_required
@permission_required(
    'experiencias.change_experiencia',
    raise_exception=True
)
@transaction.atomic
def experiencia_editar(request, experiencia_id):
    experiencias_permitidas = Experiencia.objects.select_for_update()

    es_administrador = request.user.has_perm(
        'experiencias.delete_experiencia'
    )

    if not es_administrador:
        experiencias_permitidas = (
            experiencias_permitidas.filter(
                creador=request.user
            )
        )

    experiencia = get_object_or_404(
        experiencias_permitidas,
        pk=experiencia_id
    )

    if request.method == 'POST':
        formulario = ExperienciaForm(
            request.POST,
            instance=experiencia
        )

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                'La experiencia fue actualizada correctamente.'
            )

            return redirect('experiencia_lista')
    else:
        formulario = ExperienciaForm(
            instance=experiencia
        )

    return render(
        request,
        'experiencias/experiencia_formulario.html',
        {
            'formulario': formulario,
            'titulo': 'Editar experiencia',
        }
    )


@login_required
@permission_required(
    'experiencias.delete_experiencia',
    raise_exception=True
)
@require_POST
def experiencia_eliminar(request, experiencia_id):
    experiencia = get_object_or_404(
        Experiencia,
        pk=experiencia_id
    )

    try:
        experiencia.delete()

        messages.success(
            request,
            'La experiencia fue eliminada correctamente.'
        )

    except ProtectedError:
        messages.error(
            request,
            (
                'La experiencia no se puede eliminar porque '
                'tiene reservas asociadas.'
            )
        )

    return redirect('experiencia_lista')


def catalogo_experiencias(request):
    puede_reservar = request.user.has_perm('experiencias.add_reserva') and not request.user.has_perm(
        'experiencias.change_reserva'
    )

    experiencias = (
        Experiencia.objects
        .filter(
            estado=True,
            categoria__estado=True,
            fecha_hora__gte=timezone.now()
        )
        .select_related('categoria', 'creador')
        .annotate(
            cupos_ocupados=Count('reservas')
        )
        .annotate(
            cupos_disponibles=ExpressionWrapper(
                F('cupo_maximo') - F('cupos_ocupados'),
                output_field=IntegerField()
            )
        )
        .order_by('fecha_hora')
    )

    if puede_reservar:
        reservas_usuario = Reserva.objects.filter(
            usuario=request.user,
            experiencia=OuterRef('pk')
        )

        experiencias = experiencias.annotate(
            ya_reservada=Exists(reservas_usuario)
        )

    return render(
        request,
        'experiencias/catalogo_experiencias.html',
        {
            'experiencias': experiencias,
            'puede_reservar': puede_reservar,
        }
    )


@login_required
@permission_required(
    'experiencias.add_reserva',
    raise_exception=True
)
@require_POST
def reserva_crear(request, experiencia_id):
    with transaction.atomic():
        experiencia = get_object_or_404(
            Experiencia.objects
            .select_for_update()
            .select_related('categoria'),
            pk=experiencia_id
        )

        if not experiencia.estado or not experiencia.categoria.estado:
            messages.error(
                request,
                'La experiencia ya no esta disponible.'
            )

            return redirect('catalogo_experiencias')

        if experiencia.fecha_hora < timezone.now():
            messages.error(
                request,
                'No puedes reservar una experiencia que ya paso.'
            )

            return redirect('catalogo_experiencias')

        reserva_existente = Reserva.objects.filter(
            usuario=request.user,
            experiencia=experiencia
        ).exists()

        if reserva_existente:
            messages.error(
                request,
                'Ya tienes una reserva para esta experiencia.'
            )

            return redirect('catalogo_experiencias')

        cupos_ocupados = Reserva.objects.filter(
            experiencia=experiencia
        ).count()

        if cupos_ocupados >= experiencia.cupo_maximo:
            messages.error(
                request,
                'La experiencia ya no tiene cupos disponibles.'
            )

            return redirect('catalogo_experiencias')

        Reserva.objects.create(
            usuario=request.user,
            experiencia=experiencia
        )

    messages.success(
        request,
        'La reserva fue creada correctamente.'
    )

    return redirect('reserva_lista')


@login_required
@permission_required(
    'experiencias.view_reserva',
    raise_exception=True
)
def reserva_lista(request):
    reservas = (
        Reserva.objects
        .select_related(
            'usuario',
            'experiencia',
            'experiencia__categoria',
        )
    )

    es_administrador = request.user.has_perm(
        'experiencias.change_reserva'
    )

    if not es_administrador:
        reservas = reservas.filter(
            usuario=request.user
        )

    return render(
        request,
        'experiencias/reserva_lista.html',
        {
            'reservas': reservas,
            'es_administrador': es_administrador,
            'estados_pago': Reserva.ESTADOS_PAGO,
        }
    )


@login_required
@permission_required(
    'experiencias.change_reserva',
    raise_exception=True
)
@require_POST
def reserva_cambiar_estado(request, reserva_id):
    reserva = get_object_or_404(
        Reserva,
        pk=reserva_id
    )

    nuevo_estado = request.POST.get(
        'estado_pago'
    )

    estados_validos = {
        valor
        for valor, nombre in Reserva.ESTADOS_PAGO
    }

    if nuevo_estado not in estados_validos:
        messages.error(
            request,
            'El estado de pago seleccionado no es valido.'
        )

        return redirect('reserva_lista')

    reserva.estado_pago = nuevo_estado

    reserva.save(
        update_fields=['estado_pago']
    )

    messages.success(
        request,
        'El estado del pago fue actualizado correctamente.'
    )

    return redirect('reserva_lista')


@login_required
@permission_required(
    'experiencias.delete_reserva',
    raise_exception=True
)
@require_POST
def reserva_eliminar(request, reserva_id):
    reservas_permitidas = Reserva.objects.all()

    es_administrador = request.user.has_perm(
        'experiencias.change_reserva'
    )

    if not es_administrador:
        reservas_permitidas = reservas_permitidas.filter(
            usuario=request.user
        )

    reserva = get_object_or_404(
        reservas_permitidas,
        pk=reserva_id
    )

    reserva.delete()

    messages.success(
        request,
        'La reserva fue eliminada correctamente.'
    )

    return redirect('reserva_lista')
