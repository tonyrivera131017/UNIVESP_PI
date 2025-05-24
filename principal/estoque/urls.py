from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"produtos", views.ProdutoViewSet, basename="produto")

urlpatterns = [
    path("home/", views.home, name="home"),
    path("produtos/", views.produtos, name="produtos"),
    path("cadastrar/", views.cadastrar, name="cadastrar"),
    path("editar/<int:produto_id>/", views.editar_produto, name="editar_produto"),  # Nova rota para editar
    # Adicione uma URL no seu urls.py para tratar a exclusão:
    path("excluir/<int:produto_id>/", views.excluir_produto, name="excluir_produto"),
    # Adicione uma URL no seu urls.py para tratar a adição:
    path("adicionar/", views.adicionar_produto, name="adicionar_produto"),
    path("produtos/<int:produto_id>/cadastrar-anuncio/", views.cadastrar_anuncio, name="cadastrar_anuncio"),
    path("produtos/<int:produto_id>/anuncios/", views.produto_anuncios, name="produto_anuncios"),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
