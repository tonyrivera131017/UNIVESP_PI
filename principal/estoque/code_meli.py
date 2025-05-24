import requests

url = "https://api.mercadolibre.com/oauth/token"
payload = {
    "grant_type": "authorization_code",
    "client_id": "7264778803525107",
    "client_secret": "VY6R5bH0n6h6MU34QwhcWcPXRJ0uRXR8",
    "code": "TG-68320d927678190001d4063b-346820711",
    "redirect_uri": "https://imparcialista.github.io/imparcialista/code",
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.post(url, data=payload, headers=headers)
print(response.status_code)
print(response.json())
