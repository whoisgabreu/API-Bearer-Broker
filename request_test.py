import requests


url = "http://31.97.27.195:5000/analise/presenca-online?cnpj=32161525000103"

header = {
    "X-API-KEY": "ccf9d74a30dc58035c50d1d0cb19dd20"
}

response = requests.get(url = url, headers = header)

print(response.json())