import requests

header = {
    "X-API-KEY": "ccf9d74a30dc58035c50d1d0cb19dd20"
}

url = "http://31.97.27.195:5000/analise/lista-fria"

params = {
    "socio": "Atila Lyra",
    "alias": "Mavia"
}

response = requests.get(url = url, headers = header, params = params)


print(response.json())