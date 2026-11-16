from django import forms
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from core.form_utils import aplicar_estilos_bootstrap


class CorreoDemoForm(forms.Form):
    correo = forms.EmailField(label='Correo de prueba', initial='visitante@example.com')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_estilos_bootstrap(self)


class ClaveDemoForm(forms.Form):
    clave = forms.CharField(label='Nueva clave de prueba', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    repetir = forms.CharField(label='Repite la clave de prueba', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_estilos_bootstrap(self)

    def clean_clave(self):
        clave = self.cleaned_data['clave']
        validate_password(clave)
        return clave

    def clean(self):
        datos = super().clean()
        if datos.get('clave') and datos.get('repetir') and datos['clave'] != datos['repetir']:
            self.add_error('repetir', 'Las claves no coinciden.')
        return datos


@require_http_methods(['GET', 'POST'])
def recuperar_demo(request):
    paso = request.session.get('recuperacion_demo_paso', 'correo')
    formulario = None
    if request.method == 'POST' and request.POST.get('accion') == 'reiniciar':
        request.session.pop('recuperacion_demo_paso', None)
        return redirect('recuperar_demo')
    if paso == 'correo':
        formulario = CorreoDemoForm(request.POST if request.method == 'POST' else None)
        if request.method == 'POST' and formulario.is_valid():
            request.session['recuperacion_demo_paso'] = 'enlace'
            return redirect('recuperar_demo')
    elif paso == 'enlace' and request.method == 'POST' and request.POST.get('accion') == 'abrir':
        request.session['recuperacion_demo_paso'] = 'clave'
        return redirect('recuperar_demo')
    elif paso == 'clave':
        formulario = ClaveDemoForm(request.POST if request.method == 'POST' else None)
        if request.method == 'POST' and formulario.is_valid():
            request.session['recuperacion_demo_paso'] = 'completado'
            return redirect('recuperar_demo')
    return render(request, 'registration/recuperacion_demo.html', {'paso': paso, 'formulario': formulario})
