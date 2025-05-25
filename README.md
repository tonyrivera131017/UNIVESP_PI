# Projeto Integrador: SISControl - Sistema de Controle de Estoque

Este projeto foi desenvolvido como parte do Projeto Integrador, com o objetivo de criar um software de controle de estoque que atenda a diversos requisitos técnicos e funcionais.

## Tecnologias e Requisitos Abordados

A seguir, detalhamos como cada um dos requisitos propostos foi implementado no SISControl:

### 1. Framework Web
O SISControl é construído utilizando **Django**, um framework web de alto nível em Python. Django foi escolhido por sua robustez, segurança e pela vasta quantidade de bibliotecas e ferramentas que facilitam o desenvolvimento rápido e organizado de aplicações web complexas.
- **Estrutura do Projeto:** O projeto segue a organização padrão do Django, com uma aplicação principal (`principal`) e uma aplicação dedicada à lógica de negócio do estoque (`estoque`).
- **Templates e Views:** Utiliza o sistema de templates do Django para renderizar as páginas HTML e as views baseadas em funções e classes para controlar a lógica de apresentação.

### 2. Banco de Dados
O sistema utiliza **PostgreSQL** como banco de dados relacional. A configuração do banco de dados pode ser encontrada em `principal/settings.py`. O ORM (Object-Relational Mapper) do Django é empregado para interagir com o banco de dados, abstraindo as queries SQL e facilitando a manipulação dos dados através de modelos Python (`estoque/models.py`).
- **Modelos:** Foram definidos modelos para `Produto` e `MercadoLivreAd`, representando as entidades principais do sistema.

### 3. Script Web (Javascript)
Javascript é utilizado no front-end para adicionar interatividade e melhorar a experiência do usuário.
- **Manipulação do DOM e Eventos:** Scripts como `estoque/static/js/produtos.js` (se existente para funcionalidades específicas de produtos) e `estoque/static/js/accessibility.js` (para o modo de alto contraste) interagem com os elementos da página.
- **Bibliotecas Externas:** O projeto utiliza Chart.js para a visualização de gráficos de análise de dados na página inicial (`estoque/templates/estoque/home.html`).
- **Admin Django:** O painel de administração do Django também faz uso extensivo de Javascript para suas funcionalidades.

### 4. Acessibilidade
Foram implementadas funcionalidades para tornar o sistema mais acessível:
- **Modo de Alto Contraste:** Um alternador de modo de alto contraste foi adicionado (`estoque/static/js/accessibility.js` e `estoque/static/css/style.css`), permitindo que usuários com baixa visão ou sensibilidade a cores possam utilizar o sistema com maior conforto. A preferência é salva no `localStorage`.
- **Estrutura Semântica:** Busca-se utilizar HTML semântico para melhorar a navegação e compreensão por tecnologias assistivas.
- **Foco Visível:** Estilos foram aplicados para garantir que elementos focáveis tenham um indicador visual claro.

### 5. Controle de Versão
O desenvolvimento do projeto é gerenciado utilizando **Git**. O código-fonte é versionado, permitindo o rastreamento de alterações, colaboração e a possibilidade de reverter para versões anteriores caso necessário. Recomenda-se o uso de um repositório remoto (como GitHub, GitLab) para backup e colaboração.

### 6. Testes
- Foram criados testes unitários em `estoque/tests.py` usando `django.test.TestCase`.
- **Views:** `SimpleViewsTests` verifica que as páginas principais (`home`, `produtos`, `cadastrar`) retornam HTTP 200 e usam o template esperado.
- **Modelo:** `ProdutoModelSimpleTest` valida que o método `__str__` do modelo `Produto` retorna o nome correto.

### 7. Uso e Fornecimento de API

#### a. Uso de API Externa
O sistema consome a API do **Mercado Livre** para buscar detalhes de anúncios e potencialmente integrá-los aos produtos cadastrados no estoque. A lógica de interação com esta API está implementada em `estoque/services.py`.

#### b. Fornecimento de API Interna
O SISControl expõe uma API RESTful para fornecer dados dos produtos cadastrados.
- **Django REST framework:** Foi utilizado para construir a API.
- **Endpoints:**
    - `/estoque/api/produtos/`: Lista todos os produtos (somente leitura).
    - `/estoque/api/produtos/<id>/`: Detalha um produto específico (somente leitura).
- **Serializers:** `ProdutoSerializer` (`estoque/serializers.py`) é usado para converter os dados do modelo `Produto` para o formato JSON.
- **Views:** `ProdutoViewSet` (`estoque/views.py`) controla a lógica da API para produtos.

### 8. Análises de Dados
O sistema realiza uma análise básica de dados para fornecer insights sobre o estoque.
- **Gráfico de Produtos:** Na página inicial (`estoque/templates/estoque/home.html`), é exibido um gráfico de barras (utilizando Chart.js) que mostra os 5 produtos com maior quantidade em estoque. A lógica para preparar esses dados está na view `home` em `estoque/views.py`.
