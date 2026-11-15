from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(
        max_length=50,
        unique=True
    )

    descripcion = models.TextField()

    estado = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Experiencia(models.Model):
    titulo = models.CharField(
        max_length=100
    )

    descripcion = models.TextField()

    precio = models.PositiveIntegerField()

    cupo_maximo = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    estado = models.BooleanField(default=True)

    fecha_hora = models.DateTimeField()

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='experiencias'
    )

    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='experiencias_creadas'
    )

    class Meta:
        ordering = ['fecha_hora']
        constraints = [
            models.CheckConstraint(condition=models.Q(cupo_maximo__gte=1), name='experiencia_cupo_positivo'),
        ]

    def clean(self):
        super().clean()
        if self.pk and self.cupo_maximo is not None:
            ocupados = self.reservas.count()
            if self.cupo_maximo < ocupados:
                raise ValidationError({'cupo_maximo': f'El cupo no puede ser menor que las {ocupados} reservas existentes.'})

    def __str__(self):
        return self.titulo


class Reserva(models.Model):
    asistencia = models.BooleanField(default=False)
    valoracion = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True, max_length=1000)
    PENDIENTE = 'pendiente'
    CONFIRMADO = 'confirmado'

    ESTADOS_PAGO = [
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADO, 'Confirmado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reservas'
    )

    experiencia = models.ForeignKey(
        Experiencia,
        on_delete=models.PROTECT,
        related_name='reservas'
    )

    fecha_inscripcion = models.DateTimeField(
        auto_now_add=True
    )

    estado_pago = models.CharField(
        max_length=15,
        choices=ESTADOS_PAGO,
        default=PENDIENTE
    )

    class Meta:
        ordering = ['-fecha_inscripcion']

        constraints = [
            models.CheckConstraint(condition=models.Q(valoracion__isnull=True) | models.Q(valoracion__gte=1, valoracion__lte=5), name='reserva_valoracion_valida'),
            models.UniqueConstraint(
                fields=['usuario', 'experiencia'],
                name='reserva_unica_por_usuario_y_experiencia'
            )
        ]

    def __str__(self):
        return (
            f'{self.usuario.username} - '
            f'{self.experiencia.titulo}'
        )
