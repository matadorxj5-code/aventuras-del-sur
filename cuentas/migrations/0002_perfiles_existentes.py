from django.db import migrations


def crear_perfiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    Perfil = apps.get_model('cuentas', 'Perfil')
    database = schema_editor.connection.alias
    nombres = ['Administrador', 'Gu\u00eda', 'Turista']
    administrador, _ = Group.objects.using(database).get_or_create(name='Administrador')
    for usuario in User.objects.using(database).all():
        grupos = dict(usuario.groups.using(database).filter(name__in=nombres).values_list('name', 'pk'))
        rol_id = administrador.pk if usuario.is_superuser else next((grupos[n] for n in nombres if n in grupos), None)
        Perfil.objects.using(database).get_or_create(usuario_id=usuario.pk, defaults={'rol_id': rol_id})


class Migration(migrations.Migration):
    dependencies = [('cuentas', '0001_initial')]
    operations = [migrations.RunPython(crear_perfiles, migrations.RunPython.noop)]
