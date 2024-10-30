import requests
import json
import time


# Função para ler o refresh_token de um arquivo JSON
def ler_refresh_token(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        dados = json.load(arquivo)
        return dados.get('refresh_token')


# Função para obter um novo access_token usando o refresh_token
def obter_novo_access_token(refresh_token, client_id, client_secret):
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token'], token_data['refresh_token']
    else:
        raise Exception(f"Erro ao obter novo access_token: {response.status_code} - {response.text}")


# Função para salvar o novo refresh_token em um arquivo JSON
def salvar_refresh_token(caminho_arquivo, refresh_token):
    with open(caminho_arquivo, 'w') as arquivo:
        json.dump({'refresh_token': refresh_token}, arquivo)


# Função para verificar se o access_token é válido
def verificar_token(access_token):
    url = "https://api.mercadolibre.com/users/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200


# Função para atualizar o preço e o estoque de um item no Mercado Livre
def meli_paylod(access_token, mlb_id,preco = float, estoque = int):
    """
    Função para atualizar o preço e o estoque de um item no Mercado Livre.

    :param access_token: Token de acesso à API do Mercado Livre.
    :param mlb_id: ID do item (ex: 'MLB123456789').
    :param novo_preco: Novo preço do item.
    :param nova_quantidade: Nova quantidade em estoque do item.
    """
    url = f"https://api.mercadolibre.com/items/{mlb_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {}
    if preco:
        # adicionar o preço ao payload
        payload['price'] = preco
    if estoque:
        # adicionar a quantidade ao payload
        payload['available_quantity'] = estoque

    # # Definindo o payload para atualizar preço e estoque
    # payload = {
    #     "price": novo_preco,
    #     "available_quantity": nova_quantidade
    # }

    # Fazendo a requisição PUT para atualizar o item
    response = requests.put(url, headers=headers, data=json.dumps(payload))

    # Verificando a resposta
    if response.status_code == 200:
        print(f"Item {mlb_id} atualizado com sucesso!")
    else:
        print(f"Erro ao atualizar o item {mlb_id}: {response.status_code} - {response.text}")


# Exemplo de uso
if __name__ == "__main__":
    # Substitua pelos seus valores reais
    client_id = "SEU_CLIENT_ID"
    client_secret = "SEU_CLIENT_SECRET"
    caminho_arquivo_token = "token_meli.json"
    mlb_id = "MLB123456789"  # Exemplo de ID do item
    novo_preco = 150.00  # Novo preço desejado
    nova_quantidade = 20  # Nova quantidade em estoque

    # Lendo o refresh_token do arquivo
    refresh_token = ler_refresh_token(caminho_arquivo_token)

    # Obtendo um novo access_token
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

        # Atualizando o preço e o estoque
        meli_paylod(access_token, mlb_id, preco=10, estoque=10)
    except Exception as e:
        print(str(e))
