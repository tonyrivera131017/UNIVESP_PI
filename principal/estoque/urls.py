from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('produtos/', views.produtos, name='produtos'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),  # Nova rota para editar
    #Adicione uma URL no seu urls.py para tratar a exclusão:
    path('excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
    #Adicione uma URL no seu urls.py para tratar a adição:
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),

]
