from django.shortcuts import render
from .models import Produto

def painel_estoque(request):
    # Busca todos os produtos no banco de dados
    produtos = Produto.objects.all()
    # Renderiza o template HTML e passa os produtos para o contexto
    return render(request, 'estoque/painel.html', {'produtos': produtos})
