import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiencias', '0002_experiencia_estado_alter_experiencia_cupo_maximo_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='asistencia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reserva',
            name='comentario',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='reserva',
            name='valoracion',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddConstraint(
            model_name='reserva',
            constraint=models.CheckConstraint(condition=models.Q(('valoracion__isnull', True), models.Q(('valoracion__gte', 1), ('valoracion__lte', 5)), _connector='OR'), name='reserva_valoracion_valida'),
        ),
    ]
