from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import (
    MiPerfilForm,
    UsuarioCrearForm,
    UsuarioEditarForm,
)
from .roles import GRUPO_GUIA


@login_required
def mi_perfil(request):
    formulario = MiPerfilForm(request.POST if request.method == 'POST' else None, instance=request.user)
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        messages.success(request, 'Tu perfil fue actualizado.')
        return redirect('mi_perfil')
    return render(request, 'formulario_general.html', {'formulario': formulario, 'titulo': 'Mi perfil'})


@login_required
@permission_required(
    'auth.view_user',
    raise_exception=True
)
def usuario_lista(request):
    usuarios = (
        User.objects
        .filter(is_superuser=False)
        .prefetch_related('groups')
        .order_by('username')
    )

    if request.GET.get('rol') == 'guia':
        usuarios = usuarios.filter(groups__name=GRUPO_GUIA)

    return render(
        request,
        'cuentas/usuario_lista.html',
        {
            'usuarios': usuarios,
        }
    )


@login_required
@permission_required(
    'auth.add_user',
    raise_exception=True
)
def usuario_crear(request):
    if request.method == 'POST':
        formulario = UsuarioCrearForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                'El usuario fue creado correctamente.'
            )

            return redirect('usuario_lista')
    else:
        formulario = UsuarioCrearForm()

    return render(
        request,
        'cuentas/usuario_formulario.html',
        {
            'formulario': formulario,
            'titulo': 'Crear usuario',
        }
    )


@login_required
@permission_required(
    'auth.change_user',
    raise_exception=True
)
def usuario_editar(request, usuario_id):
    usuario = get_object_or_404(
        User,
        pk=usuario_id,
        is_superuser=False
    )

    if request.method == 'POST':
        formulario = UsuarioEditarForm(
            request.POST,
            instance=usuario
        )

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                'El usuario fue actualizado correctamente.'
            )

            return redirect('usuario_lista')
    else:
        formulario = UsuarioEditarForm(
            instance=usuario
        )

    return render(
        request,
        'cuentas/usuario_formulario.html',
        {
            'formulario': formulario,
            'titulo': 'Editar usuario',
            'usuario_editado': usuario,
        }
    )


@login_required
@permission_required(
    'auth.delete_user',
    raise_exception=True
)
@require_POST
def usuario_eliminar(request, usuario_id):
    usuario = get_object_or_404(
        User,
        pk=usuario_id,
        is_superuser=False
    )

    if usuario == request.user:
        messages.error(
            request,
            'No puedes eliminar tu propio usuario.'
        )

        return redirect('usuario_lista')

    try:
        usuario.delete()

        messages.success(
            request,
            'El usuario fue eliminado correctamente.'
        )

    except ProtectedError:
        messages.error(
            request,
            (
                'El usuario no se puede eliminar porque '
                'tiene experiencias o reservas asociadas.'
            )
        )

    return redirect('usuario_lista')
