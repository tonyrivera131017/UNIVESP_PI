from django.db import models

# Modelo para Produto
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

# Modelo para Anúncios do Mercado Livre
class MercadoLivreAd(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="anuncios", null=True, blank=True)
    mlb_id = models.CharField(max_length=50, unique=True)  # ID do anúncio no Mercado Livre
    titulo = models.CharField(max_length=60)  # Nome do produto
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # Preço atual do produto
    quantidade = models.IntegerField()  # Quantidade disponível
    atualizado_em = models.DateTimeField(auto_now=True)  # Data de última atualização

    def __str__(self):
        return f"{self.produto}{self.mlb_id} - {self.titulo}"
