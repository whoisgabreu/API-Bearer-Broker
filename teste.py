import requests


API_KEY = "ccf9d74a30dc58035c50d1d0cb19dd20"
header = {
    "X-API-KEY": API_KEY
}

# url = "http://31.97.27.195:5000/broker/extrair_bearer"


url = "http://31.97.27.195:5000/analise/coletar-cnpj?socio=Atila%20Lyra&alias=Mavia"
response = requests.get(url=url, headers=header)

print(response.json())