import requests
import json

# URL da sua rota
url = "http://localhost:5000/analise/lead2"

# Dicionário com as informações a serem enviadas no corpo da requisição
data = {
    "business_info": {
        "nome": "Empresa XYZ",
        "endereco": "Rua Exemplo, 123"
    }
}

# Cabeçalhos da requisição (incluindo a API key no cabeçalho)
headers = {
    "Content-Type": "application/json",  # Informa que o corpo da requisição é JSON
    "Authorization": "sua_api_key_aqui"  # Substitua pela sua chave de API
}

# Enviar a requisição POST
response = requests.post(url, json=data, headers=headers)

# Verificar a resposta
if response.status_code == 200:
    print("Resposta recebida com sucesso!")
    print(response.json())  # Exibe o conteúdo da resposta JSON
else:
    print(f"Erro ao fazer requisição: {response.status_code}")
    print(response.json())  # Exibe o conteúdo da resposta de erro
