import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiencias', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='experiencia',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='experiencia',
            name='cupo_maximo',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddConstraint(
            model_name='experiencia',
            constraint=models.CheckConstraint(condition=models.Q(('cupo_maximo__gte', 1)), name='experiencia_cupo_positivo'),
        ),
    ]
