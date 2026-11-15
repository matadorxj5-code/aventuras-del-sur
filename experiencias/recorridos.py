import calendar
from datetime import date, datetime, time

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ValoracionForm
from .models import Experiencia, Reserva


def experiencias_propias(usuario):
    experiencias = Experiencia.objects.all()
    if not usuario.has_perm('experiencias.delete_experiencia'):
        experiencias = experiencias.filter(creador=usuario)
    return experiencias


def experiencia_detalle(request, experiencia_id):
    experiencia = get_object_or_404(Experiencia.objects.select_related('categoria', 'creador'), pk=experiencia_id)
    reserva = None
    if request.user.is_authenticated:
        reserva = experiencia.reservas.filter(usuario=request.user).first()
    publica = experiencia.estado and experiencia.categoria.estado and experiencia.fecha_hora >= timezone.now()
    responsable = request.user.is_authenticated and (request.user.pk == experiencia.creador_id or request.user.has_perm('experiencias.change_reserva'))
    if not publica and not responsable and reserva is None:
        raise Http404
    disponibles = experiencia.cupo_maximo - experiencia.reservas.count()
    puede_reservar = publica and disponibles > 0 and reserva is None and request.user.has_perm('experiencias.add_reserva') and not request.user.has_perm('experiencias.change_reserva')
    return render(request, 'experiencias/detalle.html', {'experiencia': experiencia, 'reserva': reserva, 'disponibles': disponibles, 'puede_reservar': puede_reservar})


@login_required
@permission_required('experiencias.view_experiencia', raise_exception=True)
def calendario(request):
    hoy = timezone.localdate()
    try:
        mes = date.fromisoformat(request.GET.get('mes', hoy.strftime('%Y-%m')) + '-01')
        if not 1901 <= mes.year <= 9998:
            raise ValueError
    except ValueError:
        return HttpResponseBadRequest('Mes invalido.')
    anterior = date(mes.year - 1, 12, 1) if mes.month == 1 else date(mes.year, mes.month - 1, 1)
    siguiente = date(mes.year + 1, 1, 1) if mes.month == 12 else date(mes.year, mes.month + 1, 1)
    eventos = {}
    inicio_mes = timezone.make_aware(datetime.combine(mes, time.min))
    fin_mes = timezone.make_aware(datetime.combine(siguiente, time.min))
    for experiencia in experiencias_propias(request.user).filter(fecha_hora__gte=inicio_mes, fecha_hora__lt=fin_mes):
        dia = timezone.localtime(experiencia.fecha_hora).date()
        eventos.setdefault(dia, []).append(experiencia)
    semanas = [[{'fecha': dia, 'actual': dia.month == mes.month, 'eventos': eventos.get(dia, [])} for dia in semana] for semana in calendar.Calendar().monthdatescalendar(mes.year, mes.month)]
    return render(request, 'experiencias/calendario.html', {'mes': mes, 'anterior': anterior, 'siguiente': siguiente, 'semanas': semanas})


@login_required
@permission_required('experiencias.view_experiencia', raise_exception=True)
def grupo(request, experiencia_id):
    experiencia = get_object_or_404(experiencias_propias(request.user), pk=experiencia_id)
    return render(request, 'experiencias/grupo.html', {'experiencia': experiencia, 'reservas': experiencia.reservas.select_related('usuario')})


@login_required
@permission_required('experiencias.change_experiencia', raise_exception=True)
@require_POST
def registrar_visitante(request, reserva_id):
    reserva = get_object_or_404(Reserva.objects.filter(experiencia__in=experiencias_propias(request.user)), pk=reserva_id)
    valor = request.POST.get('asistencia')
    if valor not in {'si', 'no'}:
        return HttpResponseBadRequest('Estado de asistencia invalido.')
    reserva.asistencia = valor == 'si'
    reserva.save(update_fields=['asistencia'])
    messages.success(request, 'Asistencia actualizada.')
    return redirect('grupo', experiencia_id=reserva.experiencia_id)


@login_required
@permission_required('experiencias.view_reserva', raise_exception=True)
def ticket(request, reserva_id):
    reservas = Reserva.objects.select_related('usuario', 'experiencia')
    if not request.user.has_perm('experiencias.change_reserva'):
        reservas = reservas.filter(usuario=request.user)
    reserva = get_object_or_404(reservas, pk=reserva_id)
    return render(request, 'experiencias/ticket.html', {'reserva': reserva, 'puede_valorar': reserva.usuario_id == request.user.pk and reserva.experiencia.fecha_hora < timezone.now()})


@login_required
@permission_required('experiencias.add_reserva', raise_exception=True)
def valorar(request, reserva_id):
    reserva = get_object_or_404(Reserva.objects.select_related('experiencia'), pk=reserva_id, usuario=request.user)
    if reserva.experiencia.fecha_hora >= timezone.now():
        messages.error(request, 'Podras valorar la experiencia despues de su fecha de inicio.')
        return redirect('ticket', reserva_id=reserva.pk)
    formulario = ValoracionForm(request.POST if request.method == 'POST' else None, instance=reserva)
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        messages.success(request, 'Tu valoracion fue guardada.')
        return redirect('ticket', reserva_id=reserva.pk)
    return render(request, 'formulario_general.html', {'formulario': formulario, 'titulo': 'Valorar ' + reserva.experiencia.titulo})
