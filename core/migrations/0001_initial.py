from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionParque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Aventuras del Sur', max_length=100)),
                ('descripcion', models.TextField(default='Disfruta la naturaleza y descubre experiencias al aire libre.')),
                ('contacto', models.EmailField(blank=True, max_length=254)),
            ],
        ),
    ]
