# Aventuras del Sur

Sistema Django del Ecoparque y Reserva Natural Aventuras del Sur. Incluye inicio publico, catalogo, usuarios, categorias, experiencias, reservas y acceso por rol.

## Requisitos

- Python 3.12 o superior. Verificado con Python 3.13.3.
- MySQL 8.0.11 o superior. Verificado con MySQL 8.0.46.
- CoreUI y DataTables ya estan en static/vendor; no hace falta ejecutar npm para abrir el proyecto.

## Instalacion en Windows

Desde la carpeta que contiene manage.py:

```powershell
py -3.13 -m venv .venv_windows
.\.venv_windows\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item database.example.json database.local.json
```

Edita database.local.json con tu usuario y clave de MySQL. La clave de MySQL es distinta de las claves de los usuarios de la pagina. Este archivo es local y esta excluido de Git y del paquete de entrega. Tambien puedes configurar DB_NAME, DB_USER, DB_PASSWORD, DB_HOST y DB_PORT mediante variables de entorno, que tienen prioridad.

En MySQL Workbench, crea una base vacia llamada aventura_db. Abre aventura_db.sql y ejecutalo sobre esa base. El respaldo reemplaza las tablas con el mismo nombre: usalo solamente sobre la base nueva del proyecto. Contiene los datos de ejemplo y las migraciones aplicadas.

```powershell
.\.venv_windows\Scripts\python.exe manage.py migrate
.\.venv_windows\Scripts\python.exe manage.py configurar_roles
.\.venv_windows\Scripts\python.exe manage.py check --database default
.\.venv_windows\Scripts\python.exe manage.py runserver
```

Abre http://127.0.0.1:8000/ en el navegador. No abras las plantillas como archivos HTML. La carpeta .venv de Linux del proyecto original no sirve como entorno de Windows.

## Cuentas de prueba

Las claves estan en el archivo user_pass. Son cuentas de demostracion para la entrega.

| Usuario | Rol | Datos incluidos |
|---|---|---|
| lamineyamal | Administrador | Usuarios, categorias, todas las experiencias y reservas |
| pedrigonzalez | Guia | 4 experiencias propias |
| ferminlopez | Guia | 4 experiencias propias |
| ericgarcia | Turista | 3 reservas propias |
| daniolmo | Turista | 3 reservas propias |

El respaldo tambien conserva el superusuario tecnico admin. Para probar la administracion del sitio utiliza lamineyamal.

Las actividades del respaldo estan fechadas en noviembre de 2026. Si se revisa despues, el catalogo publico ocultara las actividades pasadas; un administrador o su guia puede actualizar las fechas en Experiencias.

## Comportamiento

- Los visitantes ven el inicio y el catalogo sin ingresar. Para reservar necesitan una cuenta de turista.
- El guia crea y modifica solamente sus experiencias; no elimina experiencias ni administra categorias.
- El turista consulta y cancela solamente sus reservas. El administrador gestiona el estado de pago.
- Una experiencia debe estar activa, pertenecer a una categoria activa y tener fecha futura para aparecer en el catalogo.
- Desactivar una experiencia conserva sus reservas. Los registros relacionados se protegen contra eliminaciones que romperian su historial.
- El cupo minimo es 1 y no puede reducirse por debajo de las reservas existentes. Las reservas concurrentes usan bloqueo de la experiencia en MySQL.
- Perfil relaciona cada usuario con su rol. El rol se cambia desde Usuarios y se sincroniza con los grupos y permisos de Django.
- Los listados usan DataTables con busqueda, ordenamiento y paginacion.
- El calendario del guia muestra sus propias actividades. Grupo permite consultar inscritos y registrar o corregir su asistencia.
- Mis reservas enlaza a un comprobante con el estado de pago y al detalle del evento. La valoracion de 1 a 5 se habilita despues de la fecha de inicio y solo para el titular de la reserva.
- Mi perfil modifica nombres y correo, sin permitir cambiar el rol. Administracion dispone de configuracion del parque y reportes globales.

El diagrama de referencia se interpreta asi: los tours del guia son sus experiencias como creador; registrar visitantes significa registrar la asistencia de turistas ya inscritos; confirmar pago significa que administracion marca el pago como confirmado. No se procesa un cobro bancario.

## Pruebas

```powershell
.\.venv_windows\Scripts\python.exe manage.py test
.\.venv_windows\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Las pruebas crean y eliminan una base separada llamada test_aventura_db. El usuario MySQL necesita permisos para crear esa base. No utilizan los datos de aventura_db. Incluyen cupos, disponibilidad, perfiles y dos solicitudes concurrentes por el ultimo cupo.

## Entrega

Comparte el codigo, las migraciones, static, templates, requirements.txt, database.example.json, aventura_db.sql, user_pass y este archivo. No compartas database.local.json, entornos virtuales o node_modules.

El repositorio Git local permite revisar los cambios. Para una entrega por enlace hace falta subirlo al repositorio del equipo y entregar esa URL; un repositorio local no es un enlace remoto.
