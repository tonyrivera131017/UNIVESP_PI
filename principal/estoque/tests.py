from django.test import TestCase
from django.urls import reverse

from .models import Produto


class SimpleViewsTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_produtos_page_loads(self):
        response = self.client.get(reverse("produtos"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_page_loads(self):
        response = self.client.get(reverse("cadastrar"))
        self.assertEqual(response.status_code, 200)


class ProdutoModelSimpleTest(TestCase):
    def test_str_returns_nome(self):
        produto = Produto.objects.create(nome="TesteProd", quantidade=5, preco=10.50)
        self.assertEqual(str(produto), "TesteProd")
