import requests
import json


def AIAgentCNPJ(empresa, socio):
    url = "https://n8n.v4lisboatech.com.br/webhook/c35b4549-aa1a-410a-8c09-0b60d42e8747"


    body = {
        "empresa": empresa,
        "socio": socio
    }

    response = requests.post(url = url, json = body)
    return response.json()




    # "empresa": "estecc contabilidade",
    # "socio": "Lucas da Silva Noguez"

# print(AIAgentCNPJ("estecc contabilidade", "Lucas da Silva Noguez"))