from django import forms
from django.db.models import Q

from core.form_utils import aplicar_estilos_bootstrap

from .models import Categoria, Experiencia, Reserva


class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['valoracion', 'comentario']
        labels = {'valoracion': 'Puntuacion (1 a 5)', 'comentario': 'Tu comentario'}
        widgets = {'valoracion': forms.Select(choices=[(n, str(n)) for n in range(1, 6)])}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valoracion'].required = True
        aplicar_estilos_bootstrap(self)


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria

        fields = [
            'nombre',
            'descripcion',
            'estado',
        ]

        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'estado': 'Categoria activa',
        }

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre de la categoria',
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'placeholder': (
                        'Descripcion de la categoria'
                    ),
                    'rows': 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        aplicar_estilos_bootstrap(self)


class ExperienciaForm(forms.ModelForm):
    fecha_hora = forms.DateTimeField(
        label='Fecha y hora de realizacion',
        input_formats=[
            '%Y-%m-%dT%H:%M',
        ],
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={
                'type': 'datetime-local',
            }
        )
    )

    class Meta:
        model = Experiencia

        fields = [
            'titulo',
            'descripcion',
            'precio',
            'cupo_maximo',
            'fecha_hora',
            'categoria',
            'estado',
        ]

        labels = {
            'titulo': 'Titulo',
            'descripcion': 'Descripcion',
            'precio': 'Precio',
            'cupo_maximo': 'Cupo maximo',
            'categoria': 'Categoria',
            'estado': 'Experiencia activa',
        }

        widgets = {
            'titulo': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre de la experiencia',
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'placeholder': (
                        'Describe la actividad y sus caracteristicas'
                    ),
                    'rows': 5,
                }
            ),
            'precio': forms.NumberInput(
                attrs={
                    'min': 0,
                    'placeholder': 'Precio en pesos',
                }
            ),
            'cupo_maximo': forms.NumberInput(
                attrs={
                    'min': 1,
                    'placeholder': 'Cantidad maxima de participantes',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        categorias_disponibles = Categoria.objects.filter(
            estado=True
        )

        if self.instance.pk and self.instance.categoria_id:
            categorias_disponibles = Categoria.objects.filter(
                Q(estado=True)
                | Q(pk=self.instance.categoria_id)
            )

        self.fields['categoria'].queryset = (
            categorias_disponibles.order_by('nombre')
        )

        aplicar_estilos_bootstrap(self)
