from django import forms
from .form_utils import aplicar_estilos_bootstrap
from .models import ConfiguracionParque


class ConfiguracionParqueForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionParque
        fields = ['nombre', 'descripcion', 'contacto']
        labels = {'descripcion': 'Descripcion', 'contacto': 'Correo de contacto'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_estilos_bootstrap(self)
