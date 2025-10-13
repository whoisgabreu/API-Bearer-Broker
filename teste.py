import requests


url = "https://n8n.v4lisboatech.com.br/webhook-test/c35b4549-aa1a-410a-8c09-0b60d42e8747" 

payload = {
    "empresa": "Estecc",
    "socio": "Lucas",
    "uf": "RS"
}

requests.post(url = url, json = payload)