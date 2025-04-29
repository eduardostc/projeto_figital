from django.urls import path
from . import views
from .views import exportar_escalao_excel, exportar_transformacao_excel, excluir_registro_escalao

urlpatterns = [
    path('', views.index, name='index'),  # Alterado de 'home' para 'index'
    path('registros/', views.index_autenticado, name='index_autenticado'), 
    path('primeiro-escalao/', views.primeiro_escalao, name='primeiro_escalao'),
    path('rede-transformacao/', views.rede_transformacao, name='rede_transformacao'),
    path('login/', views.login_view, name='login'),
    path('visualizar-escalao/', views.visualizar_escalao, name='visualizar_escalao'),
    path('visualizar-transformacao/', views.visualizar_transformacao, name='visualizar_transformacao'),

    path('exportar-escalao/', exportar_escalao_excel, name='exportar_escalao'),
    path('exportar-transformacao/', exportar_transformacao_excel, name='exportar_transformacao'),

    path('excluir-escalao/<int:registro_id>', views.excluir_registro_escalao, name='excluir_registro_escalao'),
    path('excluir-transformacao/<int:registro_id>', views.excluir_registro_transformacao, name='excluir_registro_transformacao'),
    
]
