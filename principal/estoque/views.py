from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets

from .forms import MercadoLivreAdForm, ProdutoForm
from .models import MercadoLivreAd, Produto
from .serializers import ProdutoSerializer
from .services import (
    ler_refresh_token,
    meli_paylod,
    obter_novo_access_token,
    salvar_refresh_token,
)


def produtos(request):
    # Busca todos os produtos no banco de dados
    produtos = Produto.objects.all()
    # Renderiza o template HTML e passa os produtos para o contexto
    return render(request, "estoque/produtos.html", {"produtos": produtos})


def grafico_produtos(request):
    # Obtendo os 5 produtos com maior quantidade
    produtos = Produto.objects.order_by("-quantidade")[:5]

    # Extraindo os dados necessários para o gráfico
    nomes = [produto.nome for produto in produtos]
    quantidades = [produto.quantidade for produto in produtos]

    # Renderizando o template com os dados
    return render(request, "estoque/home.html", {"nomes": nomes, "quantidades": quantidades})


def produto_anuncios(request, produto_id):
    # Obtém o produto pelo ID
    produto = get_object_or_404(Produto, pk=produto_id)
    # Busca os anúncios associados a esse produto
    anuncios = produto.anuncios.all()
    for anuncio in anuncios:
        anuncio.mlb_id_formatado = anuncio.mlb_id[:3] + "-" + anuncio.mlb_id[3:]
    # Renderiza o template HTML e passa os anúncios para o contexto
    return render(request, "estoque/produtos.html", {"produto": produto, "anuncios": anuncios})


def home(request):
    # Obter os 5 produtos com maior estoque
    produtos = Produto.objects.order_by("-quantidade")[:5]
    nomes = [produto.nome for produto in produtos]
    quantidades = [produto.quantidade for produto in produtos]

    return render(
        request,
        "estoque/home.html",
        {
            "nomes": nomes,
            "quantidades": quantidades,
        },
    )


def cadastrar(request):
    return render(request, "estoque/cadastrar.html")


def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)

    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            # Salva os campos do Produto (nome, quantidade, preco)
            produto_atualizado = form.save()

            mlb_id_do_form = form.cleaned_data.get("mlb_id_vinculado", "").strip()
            primeiro_anuncio = produto_atualizado.anuncios.first()

            mlb_id_para_atualizar_api = None

            if mlb_id_do_form:  # Se um MLB ID foi fornecido no formulário
                if primeiro_anuncio:
                    if primeiro_anuncio.mlb_id != mlb_id_do_form:
                        # MLB ID mudou, atualiza o MLB ID do anúncio existente
                        primeiro_anuncio.mlb_id = mlb_id_do_form
                        primeiro_anuncio.save()
                    mlb_id_para_atualizar_api = mlb_id_do_form
                else:
                    # Não havia anúncio, cria um novo
                    novo_anuncio = MercadoLivreAd.objects.create(produto=produto_atualizado, mlb_id=mlb_id_do_form)
                    mlb_id_para_atualizar_api = novo_anuncio.mlb_id
            elif primeiro_anuncio:  # Se o campo MLB ID do formulário está vazio, mas existia um anúncio
                # Desvincula/remove o anúncio existente
                primeiro_anuncio.delete()
                # Não há mlb_id_para_atualizar_api neste caso, pois foi desvinculado.

            # Atualizando no Mercado Livre se um MLB ID estiver ativo
            if mlb_id_para_atualizar_api:
                novo_preco = produto_atualizado.preco
                nova_quantidade = produto_atualizado.quantidade
                try:
                    refresh_token = ler_refresh_token(settings.MELI_REFRESH_TOKEN_FILE)
                    access_token, novo_refresh_token_para_salvar = obter_novo_access_token(
                        refresh_token, settings.MELI_CLIENT_ID, settings.MELI_CLIENT_SECRET
                    )
                    salvar_refresh_token(settings.MELI_REFRESH_TOKEN_FILE, novo_refresh_token_para_salvar)

                    preco_formatado = float(novo_preco)
                    quantidade_formatada = int(nova_quantidade)
                    meli_paylod(
                        access_token,
                        mlb_id_para_atualizar_api,
                        preco=preco_formatado,
                        estoque=quantidade_formatada,
                    )
                except Exception as e:
                    # Idealmente, adicionar uma mensagem para o usuário aqui (e.g., usando django.contrib.messages)
                    print(f"Erro ao atualizar o anúncio {mlb_id_para_atualizar_api} no Mercado Livre: {str(e)}")

            return redirect("produtos")
    else:  # GET request
        form = ProdutoForm(instance=produto)

    return render(request, "estoque/editar_produto.html", {"form": form, "produto": produto})


def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)  # Obtém o produto pelo ID
    if request.method == "POST":
        produto.delete()
        return redirect("produtos")  # Redireciona para a página principal do estoque após excluir
    return render(request, "estoque/excluir_produto.html", {"produto": produto})


def adicionar_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("produtos")  # Redireciona para a página principal do estoque após salvar
    else:
        form = ProdutoForm()

    return render(request, "estoque/adicionar_produto.html", {"form": form})


def cadastrar_anuncio(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if request.method == "POST":
        form = MercadoLivreAdForm(request.POST)
        if form.is_valid():
            # Verifica se já existe um anúncio com este mlb_id para evitar duplicatas
            # ou decide como lidar com isso (ex: atualizar o produto do anúncio existente)
            mlb_id_novo = form.cleaned_data["mlb_id"]
            anuncio_existente = MercadoLivreAd.objects.filter(mlb_id=mlb_id_novo).first()

            if anuncio_existente:
                # Se já existe, apenas associa ao produto atual se for diferente
                if anuncio_existente.produto != produto:
                    anuncio_existente.produto = produto
                    anuncio_existente.save()
                # Ou mostrar uma mensagem de erro/aviso
            else:
                anuncio = form.save(commit=False)
                anuncio.produto = produto
                anuncio.save()
            return redirect("produto_anuncios", produto_id=produto.id)
    else:
        form = MercadoLivreAdForm()
    return render(request, "estoque/cadastrar_anuncio.html", {"form": form, "produto": produto})


# API Views
class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint que permite que produtos sejam visualizados.
    """

    queryset = Produto.objects.all().order_by("-id")
    serializer_class = ProdutoSerializer
