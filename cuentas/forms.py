from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django.contrib.auth.models import Group, User

from core.form_utils import aplicar_estilos_bootstrap

from .roles import (
    GRUPO_ADMINISTRADOR,
    GRUPO_GUIA,
    GRUPO_TURISTA,
)


NOMBRES_GRUPOS = [
    GRUPO_ADMINISTRADOR,
    GRUPO_GUIA,
    GRUPO_TURISTA,
]


class MiPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Nombres', 'last_name': 'Apellidos', 'email': 'Correo'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_estilos_bootstrap(self)


class InicioSesionForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        aplicar_estilos_bootstrap(self)

        self.fields['username'].label = 'Nombre de usuario'
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Ingresa tu nombre de usuario',
            'autocomplete': 'username',
        })

        self.fields['password'].label = 'Contraseña'
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'current-password',
        })


class UsuarioCrearForm(UserCreationForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.filter(
            name__in=NOMBRES_GRUPOS
        ).order_by('name'),
        empty_label='Seleccione un rol',
        label='Rol'
    )

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'grupo',
        ]

        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electronico',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        aplicar_estilos_bootstrap(self)

        self.fields['username'].widget.attrs[
            'placeholder'
        ] = 'Ejemplo: juan.perez'

        self.fields['first_name'].widget.attrs[
            'placeholder'
        ] = 'Nombres del usuario'

        self.fields['last_name'].widget.attrs[
            'placeholder'
        ] = 'Apellidos del usuario'

        self.fields['email'].widget.attrs[
            'placeholder'
        ] = 'correo@ejemplo.cl'

    def save(self, commit=True):
        usuario = super().save(commit=commit)

        if commit:
            grupo = self.cleaned_data['grupo']
            usuario.groups.set([grupo])

        return usuario


class UsuarioEditarForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.filter(
            name__in=NOMBRES_GRUPOS
        ).order_by('name'),
        empty_label='Seleccione un rol',
        label='Rol'
    )

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'grupo',
            'is_active',
        ]

        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electronico',
            'is_active': 'Usuario activo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        aplicar_estilos_bootstrap(self)

        if self.instance.pk:
            grupo_actual = self.instance.groups.first()

            if grupo_actual:
                self.fields['grupo'].initial = grupo_actual

    def save(self, commit=True):
        usuario = super().save(commit=commit)

        if commit:
            grupo = self.cleaned_data['grupo']
            usuario.groups.set([grupo])

        return usuario
