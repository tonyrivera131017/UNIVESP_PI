from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel_estoque, name='painel_estoque'),
]
