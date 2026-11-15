from django.contrib import admin

from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol')
    readonly_fields = ('usuario', 'rol')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
