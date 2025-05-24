import json
import os

import requests
from django.conf import settings


def ler_refresh_token(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r") as f:
            return json.load(f).get("refresh_token")
    return None


def salvar_refresh_token(caminho_arquivo, refresh_token):
    with open(caminho_arquivo, "w") as f:
        json.dump({"refresh_token": refresh_token}, f)


def verificar_token(access_token):
    url = "https://api.mercadolibre.com/users/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.status_code == 200


def obter_novo_access_token(refresh_token, client_id, client_secret):
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }
    headers = {"accept": "application/json", "content-type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    novo_access_token = data.get("access_token")
    novo_refresh_token = data.get("refresh_token", refresh_token)
    return novo_access_token, novo_refresh_token


def obter_access_token_seguro(client_id, client_secret, token_file):
    refresh_token = ler_refresh_token(token_file)
    try:
        access_token, novo_refresh_token = obter_novo_access_token(refresh_token, client_id, client_secret)
        salvar_refresh_token(token_file, novo_refresh_token)
        return access_token
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            erro = e.response.json()
            if erro.get("error") == "invalid_grant":
                raise Exception(
                    "Refresh token expirado ou inválido. É necessário autorizar novamente no Mercado Livre."
                )
        raise


def meli_paylod(access_token, mlb_id, preco=float, estoque=int):
    url = f"https://api.mercadolibre.com/items/{mlb_id}"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {}
    if preco:
        payload["price"] = preco
    if estoque:
        payload["available_quantity"] = estoque

    response = requests.put(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print(f"Item {mlb_id} atualizado com sucesso!")
    else:
        print(f"Erro ao atualizar o item {mlb_id}: {response.status_code} - {response.text}")


if __name__ == "__main__":
    # Substitua pelos seus valores reais ou importe do settings
    client_id = "7264778803525107"
    client_secret = "VY6R5bH0n6h6MU34QwhcWcPXRJ0uRXR8"
    token_file = r"C:\pycharm-projects\UNIVESP_PI\principal\estoque\refresh_token.json"

    mlb_id = "MLB123456789"  # ID do item no Mercado Livre
    novo_preco = 150.00  # Novo preço
    nova_quantidade = 20  # Nova quantidade em estoque

    try:
        access_token = obter_access_token_seguro(client_id, client_secret, token_file)
        meli_paylod(access_token, mlb_id, preco=novo_preco, estoque=nova_quantidade)
    except Exception as e:
        print(f"Erro: {e}")
