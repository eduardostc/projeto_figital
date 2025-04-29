from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PrimeiroEscalao, RedeTransformacaoDigital

# Configuração do modelo de usuário personalizado no Admin
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['email', 'username', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        
        ('Permissões', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

# Melhorando a exibição do modelo 1º Escalão no Admin
@admin.register(PrimeiroEscalao)
class PrimeiroEscalaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'secretaria', 'cargo', 'email', 'telefone', 'problema_urgente', 'data_publicacao']
    search_fields = ['nome', 'secretaria', 'cargo']
    list_filter = ['secretaria', 'data_publicacao']
    ordering = ['data_publicacao']

# Melhorando a exibição do modelo Rede de Transformação Digital no Admin
@admin.register(RedeTransformacaoDigital)
class RedeTransformacaoDigitalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'secretaria', 'cargo', 'email', 'telefone', 'chefe_imediato', 'problema_urgente', 'data_publicacao']
    search_fields = ['nome', 'secretaria', 'cargo']
    list_filter = ['secretaria', 'data_publicacao']
    ordering = ['data_publicacao']
