from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Q, Sum

from experiencias.models import Experiencia, Reserva
from .forms import ConfiguracionParqueForm
from .models import ConfiguracionParque


def inicio(request):
    if not request.user.is_authenticated:
        return render(request, 'bienvenida.html', {'parque': ConfiguracionParque.objects.first()})

    if request.user.has_perm('auth.view_user'):
        return render(request, 'inicio.html')

    if request.user.has_perm('experiencias.add_experiencia'):
        return redirect('experiencia_lista')

    if request.user.has_perm('experiencias.add_reserva'):
        return redirect('catalogo_experiencias')

    raise PermissionDenied(
        'Tu usuario no tiene un rol configurado.'
    )


@login_required
@permission_required('auth.change_user', raise_exception=True)
def configuracion_parque(request):
    parque = ConfiguracionParque.objects.first() or ConfiguracionParque()
    formulario = ConfiguracionParqueForm(request.POST if request.method == 'POST' else None, instance=parque)
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        messages.success(request, 'Configuracion guardada.')
        return redirect('configuracion_parque')
    return render(request, 'formulario_general.html', {'formulario': formulario, 'titulo': 'Configuracion del ecoparque'})


@login_required
@permission_required('experiencias.change_reserva', raise_exception=True)
def reportes(request):
    resumen = Reserva.objects.aggregate(
        total=Count('id'), confirmadas=Count('id', filter=Q(estado_pago=Reserva.CONFIRMADO)),
        pendientes=Count('id', filter=Q(estado_pago=Reserva.PENDIENTE)),
        importe_confirmado=Sum('experiencia__precio', filter=Q(estado_pago=Reserva.CONFIRMADO)),
    )
    experiencias = Experiencia.objects.select_related('creador').annotate(inscritos=Count('reservas')).order_by('fecha_hora')
    return render(request, 'reportes.html', {'resumen': resumen, 'experiencias': experiencias})
