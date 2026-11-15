from django.db import models

class ConfiguracionParque(models.Model):
    nombre = models.CharField(max_length=100, default='Aventuras del Sur')
    descripcion = models.TextField(default='Disfruta la naturaleza y descubre experiencias al aire libre.')
    contacto = models.EmailField(blank=True)
