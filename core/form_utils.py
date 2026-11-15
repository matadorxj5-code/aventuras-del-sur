from django import forms


def aplicar_estilos_bootstrap(formulario):
    for campo in formulario.fields.values():
        widget = campo.widget

        if isinstance(widget, forms.HiddenInput):
            continue

        if isinstance(widget, forms.CheckboxInput):
            clase = 'form-check-input'

        elif isinstance(widget, forms.Select):
            clase = 'form-select'

        else:
            clase = 'form-control'

        clases_actuales = widget.attrs.get(
            'class',
            ''
        )

        widget.attrs['class'] = (
            f'{clases_actuales} {clase}'.strip()
        )

        if isinstance(widget, forms.Textarea):
            widget.attrs.setdefault('rows', 4)
