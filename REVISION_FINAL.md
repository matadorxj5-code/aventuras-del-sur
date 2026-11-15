# Revision de entrega - 15 de noviembre de 2026

Proyecto revisado: evaluacion3/evaluacion3. Se conserva el caso Ecoparque y Reserva Natural Aventuras del Sur y el proyecto Django inventarioAventura.

## Requisitos escritos

| Requisito | Implementacion y verificacion |
|---|---|
| Django y apps core, cuentas, experiencias | Configuradas y verificadas con manage.py check |
| Inicio y bienvenida publicos | / muestra la bienvenida a visitantes |
| Perfil relacionado con User | cuentas.Perfil, OneToOne con usuario y FK a su grupo; sincronizacion al cambiar rol |
| Categoria: nombre, descripcion, estado | Modelo y CRUD del administrador |
| Experiencia: titulo, descripcion, precio, cupo, fecha/hora, categoria y creador | Modelo y formularios; creador asignado en servidor |
| Reserva: usuario, experiencia, fecha de inscripcion y estado de pago | Relaciones, fecha automatica y estados Pendiente/Confirmado |
| CSS moderno | CoreUI local y estilos propios |
| DataTables: busqueda, ordenamiento y paginacion | Verificados en navegador; no se quitaron los controles exigidos por la pauta |
| Administrador | CRUD de usuarios/categorias/experiencias y todas las reservas |
| Guia | Crea, consulta y modifica solo sus experiencias; no elimina ni administra categorias |
| Turista | Catalogo publico, reserva autenticada e historial y cancelacion de reservas propias |
| Sesiones y acceso por rol | Login, logout POST, CSRF, permisos y aislamiento por usuario |
| Experiencias activas | Estado individual, categoria activa y fecha futura para catalogo y nuevas reservas |
| Cupos | Minimo 1, no se reducen bajo reservas existentes, bloqueo MySQL al editar/reservar |
| Administrador de prueba | lamineyamal |
| Dos guias con cuatro experiencias cada uno | pedrigonzalez: 4; ferminlopez: 4 |
| Dos turistas con tres reservas cada uno | ericgarcia: 3; daniolmo: 3 |
| MySQL | Conexion real y migraciones aplicadas en MySQL 8.0.46 |
| Respaldo | aventura_db.sql regenerado y restaurado en otra base temporal; conteos y migraciones correctos |
| Credenciales | Archivo user_pass, claves verificadas; configuracion MySQL local separada |
| Codigo y migraciones | Incluidos junto con requirements.txt, configuracion de ejemplo e instrucciones |
| Git | Repositorio local preparado; falta el enlace remoto del equipo si la entrega se realiza por URL |

Los registros relacionados se protegen contra eliminacion para conservar integridad. Las actividades pueden desactivarse sin borrar sus reservas.

## Recorridos del diagrama

| Nodo | Acceso implementado |
|---|---|
| Home / Login | Inicio publico e Iniciar sesion |
| Panel de control | Inicio del administrador |
| Gestion de usuarios | Usuarios: crear, editar, desactivar, eliminar registros sin dependencias |
| Gestion de guias | Acceso dedicado al listado de usuarios filtrado por guia |
| Gestion de rutas/actividades | Experiencias |
| Configuracion del ecoparque | Configuracion, aplicada a la bienvenida |
| Reportes globales | Totales, pagos pendientes/confirmados y ocupacion por actividad |
| Mi perfil | Nombres, apellidos y correo del usuario actual |
| Calendario de actividades | Calendario mensual con enlaces a los grupos de las actividades propias |
| Mis tours asignados | Experiencias propias; la autoria es la relacion de guia definida en el modelo escrito |
| Detalle del grupo | Inscritos de la actividad propia |
| Registrar visitantes | Registro de asistencia de visitantes previamente inscritos |
| Actualizar estado de ruta | Estado activo/inactivo en editar experiencia |
| Catalogo / elegir ruta | Catalogo publico y detalle de experiencia |
| Reservar ticket | Reserva autenticada y comprobante privado con numero de reserva |
| Mis reservas | Historial propio |
| Confirmacion de pago | Estado actualizado por administrador y visible en el comprobante; sin pasarela bancaria |
| Detalle del evento | Pagina de detalle; historial accesible al titular aun si la actividad ya no es publica |
| Valorar experiencia | Puntuacion 1 a 5 y comentario, solo en reserva propia despues de la fecha de inicio |
| Logout de cada rol | Menu de cuenta, cierre por POST |

Las interpretaciones de tours, asistencia y pago se hacen explicitas porque el diagrama no describe reglas adicionales para esas cajas. No se presenta una asignacion independiente del creador ni una pasarela de pagos como si estuvieran implementadas.

## Evidencia

- 19 pruebas automatizadas satisfactorias en una base MySQL separada, incluidas dos solicitudes simultaneas para el ultimo cupo.
- 130 comprobaciones satisfactorias de la auditoria funcional sobre SQLite en memoria: CRUD, permisos, sesiones, validaciones, plantillas, recursos y credenciales del respaldo.
- 32 recorridos de paginas en navegador Edge, a 1440 px y 390 px. Respuestas correctas, sin errores JavaScript ni desborde de la pagina tras completar las transiciones. Las tablas anchas conservan desplazamiento horizontal dentro de su contenedor.
- Busqueda, ordenamiento, paginacion y modal de reserva comprobados en navegador. Para probar varias paginas con ocho experiencias se uso temporalmente una longitud de tres filas en la sesion del navegador; la configuracion entregada conserva diez.
- Respaldo restaurado en otra base MySQL: 6 usuarios, 6 perfiles, 8 experiencias, 6 reservas y 0 sesiones activas incluidas. La base temporal se elimino al terminar.
- Sin cambios de modelos pendientes ni migraciones sin aplicar.

## Limites de la entrega

El trabajo local queda preparado. La publicacion del repositorio remoto y la entrega en la plataforma del curso no se han realizado. La fecha oficial de entrega y la evaluacion del docente no se pueden verificar desde el codigo. Este informe no asigna nota ni promete ausencia absoluta de errores.
