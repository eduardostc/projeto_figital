from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PrimeiroEscalao, RedeTransformacaoDigital

# Configuração do modelo de usuário personalizado no Admin
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['email', 'username', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissões', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

# Registrando os modelos no Django Admin
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(PrimeiroEscalao)
admin.site.register(RedeTransformacaoDigital)