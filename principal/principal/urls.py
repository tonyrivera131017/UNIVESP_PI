from django.contrib import admin
from django.urls import path, include
from estoque import views  # Importando a view diretamente do app estoque

urlpatterns = [
    path('admin/', admin.site.urls),
    path('estoque/', include('estoque.urls')),
    path('', views.home),  # Define uma rota para a URL raiz
]
