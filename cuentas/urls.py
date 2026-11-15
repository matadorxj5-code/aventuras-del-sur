from django.contrib.auth import views as auth_views
from django.urls import path
from .forms import InicioSesionForm
from . import views


urlpatterns = [
    path('perfil/', views.mi_perfil, name='mi_perfil'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=InicioSesionForm
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'usuarios/',
        views.usuario_lista,
        name='usuario_lista'
    ),

    path(
        'usuarios/crear/',
        views.usuario_crear,
        name='usuario_crear'
    ),

    path(
        'usuarios/<int:usuario_id>/editar/',
        views.usuario_editar,
        name='usuario_editar'
    ),

    path(
        'usuarios/<int:usuario_id>/eliminar/',
        views.usuario_eliminar,
        name='usuario_eliminar'
    ),
]
