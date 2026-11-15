from django.urls import path

from .views import inicio, configuracion_parque, reportes


urlpatterns = [
    path('', inicio, name='inicio'),
    path('configuracion/', configuracion_parque, name='configuracion_parque'),
    path('reportes/', reportes, name='reportes'),
]
