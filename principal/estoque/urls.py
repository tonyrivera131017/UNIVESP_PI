from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel_estoque, name='painel_estoque'),
    path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),  # Nova rota para editar
    #Adicione uma URL no seu urls.py para tratar a exclusão:
    path('excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
]
