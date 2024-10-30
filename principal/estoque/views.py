from django.shortcuts import render,get_object_or_404,redirect
from .models import Produto
from .forms import ProdutoForm  # Precisamos criar esse formulário em breve

def produtos(request):
    # Busca todos os produtos no banco de dados
    produtos = Produto.objects.all()
    # Renderiza o template HTML e passa os produtos para o contexto
    return render(request, 'estoque/produtos.html', {'produtos': produtos})


def home(request):
    return render(request, 'estoque/home.html')

def cadastrar(request):
    return render(request, "estoque/cadastrar.html")


def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)  # Obtém o produto pelo ID

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produtos')  # Redireciona para a página principal do estoque após salvar
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'estoque/editar_produto.html', {'form': form})

def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)  # Obtém o produto pelo ID
    if request.method == 'POST':
        produto.delete()
        return redirect('produtos')  # Redireciona para a página principal do estoque após excluir
    return render(request, 'estoque/excluir_produto.html', {'produto': produto})

def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produtos')  # Redireciona para a página principal do estoque após salvar
    else:
        form = ProdutoForm()

    return render(request, 'estoque/adicionar_produto.html', {'form': form})