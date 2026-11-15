                                             

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.TextField()),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Experiencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.PositiveIntegerField()),
                ('cupo_maximo', models.PositiveIntegerField()),
                ('fecha_hora', models.DateTimeField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experiencias', to='experiencias.categoria')),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experiencias_creadas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['fecha_hora'],
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inscripcion', models.DateTimeField(auto_now_add=True)),
                ('estado_pago', models.CharField(choices=[('pendiente', 'Pendiente'), ('confirmado', 'Confirmado')], default='pendiente', max_length=15)),
                ('experiencia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservas', to='experiencias.experiencia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha_inscripcion'],
                'constraints': [models.UniqueConstraint(fields=('usuario', 'experiencia'), name='reserva_unica_por_usuario_y_experiencia')],
            },
        ),
    ]
