from django.shortcuts import render,get_object_or_404,redirect
from .models import Produto,MercadoLivreAd
from .forms import ProdutoForm  # Precisamos criar esse formulário em breve
from .services import *  # Importe a função que criamos para atualizar no Mercado Livre
caminho_arquivo_token = './refresh_token.json'
def produtos(request):
    # Busca todos os produtos no banco de dados
    produtos = Produto.objects.all()
    # Renderiza o template HTML e passa os produtos para o contexto
    return render(request, 'estoque/produtos.html', {'produtos': produtos})


def home(request):
    return render(request, 'estoque/home.html')


def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)  # Obtém o produto pelo ID

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()

            # Obtém todos os anúncios vinculados ao produto
            anuncios = MercadoLivreAd.objects.filter(produto=produto)

            # Atualizando no Mercado Livre após salvar localmente
            novo_preco = produto.preco
            nova_quantidade = produto.quantidade
            refresh_token = ler_refresh_token(caminho_arquivo_token)
            client_id = "7264778803525107"
            client_secret = "VY6R5bH0n6h6MU34QwhcWcPXRJ0uRXR8"
            try:
                # Verifica se o token atual é válido, caso contrário, renova
                access_token = None
                if 'access_token' in globals() and verificar_token(access_token):
                    print("Access token válido.")
                else:
                    print("Access token inválido ou não encontrado. Renovando token...")
                    access_token, novo_refresh_token = obter_novo_access_token(refresh_token, client_id, client_secret)
                    # Salvando o novo refresh_token no arquivo
                    salvar_refresh_token(caminho_arquivo_token, novo_refresh_token)

                # Atualizando todos os anúncios vinculados
                # Atualizando todos os anúncios vinculados
                for anuncio in anuncios:
                    mlb_id = anuncio.mlb_id
                    # Convertendo o valor Decimal para float para ser JSON serializável
                    preco_atualizado = float(novo_preco)
                    quantidade_atualizada = int(nova_quantidade)  # Certifique-se de que a quantidade é um valor int

                    # Atualizando o preço e o estoque para cada anúncio
                    meli_paylod(access_token, mlb_id, preco=preco_atualizado, estoque=quantidade_atualizada)


            except Exception as e:
                print(str(e), 'ERRRRROOOO')

            return redirect('produtos')  # Redireciona após salvar
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