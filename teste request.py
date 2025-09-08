import base64
from tkinter import filedialog

# file_path = filedialog.askopenfilename(filetypes = [("DOCX", "*.docx")])

# # Ler o arquivo e converter para base64
# with open(file_path, "rb") as f:
#     docx_base64 = base64.b64encode(f.read()).decode("utf-8")


# import requests


# url = "https://api.v4lisboatech.com.br/convert/docx"


# header = {
#     "X-API-KEY": "ccf9d74a30dc58035c50d1d0cb19dd20"
# }


# payload = {
#     "file_base64": docx_base64
# }

# response = requests.post(url=url, headers = header,json = payload)

# # Salva o PDF de resposta
# if response.status_code == 200:
#     with open("saida.pdf", "wb") as f:
#         f.write(response.content)
#     print("PDF salvo como 'saida.pdf'")
# # else:
#     print("Erro:", response.status_code, response.text)



# import requests
# # url = "https://api.v4lisboatech.com.br/analise/lead"
# url = "https://n8n.v4lisboatech.com.br/webhook-test/c35b4549-aa1a-410a-8c09-0b60d42e8747"

# params = {
#     "empresa": "SB Flex",
#     "socio": "MATHEUS ARISTIDES FELICIO"
# }

# header = {
#    "X-API-KEY": "ccf9d74a30dc58035c50d1d0cb19dd20"
# }


# # response = requests.get(url = url, params = params, headers = header)
# response = requests.post(url = url, json = params)


# print(response.json())


# import requests
# import json


# url = "http://api.v4lisboatech.com.br/ml/lead"

# body = {
#         "faturamento": "De 401 mil à 1 milhão",
#         "cargo": "Sócio",
#         "nivel_urgencia": "Em até três meses",
#         "tem_site": "Não",
#         "tem_anuncio": "Não",
#         "segmento": "E-commerce"
#     }

# r = requests.post(url = url, json = body)

# print(json.dumps(r.json(), indent = 2, ensure_ascii = False))

# import requests

# _id = "68ae0696832178f0c221bc44"

# url = "https://n8n.v4lisboatech.com.br/webhook-test/92893a17-18a3-4db8-abe3-de253c2128d4"

# payload = {
#     "_id": _id
# }

# r = requests.post(url = url, json = payload)

# print(r.json())


import requests
import json

url = "http://192.168.0.190:5000/convert/html"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer seu_api_key"
}
data = {
    "html_content": """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentação de Endpoints para Análise de Squads e Clientes</title>
</head>
<body>
    <h1>Documentação de Endpoints para Análise de Squads e Clientes</h1>
    <p>Esta documentação descreve os endpoints e parâmetros necessários para a construção de uma ferramenta de análise de squads, clientes, valores e afins. O objetivo é permitir que o agente IA possa buscar de forma assertiva informações relacionadas a vendas, upsells, churns, entre outros.</p>

    <h2>1. Estrutura de Endpoints</h2>

    <h3>1.1 Endpoints de Filtragem</h3>
    <p>Esses endpoints realizam buscas e filtragens com base em parâmetros como Squad, Cliente, Status, etc.</p>

    <ul>
        <li><strong>/vendas/squad/{squad_id}</strong>: Filtro por <strong>Squad</strong>.  
            Parâmetros: <code>squad_id</code> (ex: "SQ002 - Balneário").
        </li>
        <li><strong>/vendas/cliente/{cliente_id}</strong>: Filtro por <strong>Cliente</strong>.  
            Parâmetros: <code>cliente_id</code> (ex: "Glas Laser").
        </li>
        <li><strong>/vendas/periodo</strong>: Filtro por <strong>Data</strong> em um intervalo de tempo.  
            Parâmetros: <code>data_inicial</code>, <code>data_final</code> (ex: <code>data_inicial=2020-03-01</code>, <code>data_final=2025-12-31</code>).
        </li>
        <li><strong>/vendas/status</strong>: Filtro por <strong>Status</strong> da venda (ex: "Ativo", "Churn").  
            Parâmetros: <code>status</code>.
        </li>
        <li><strong>/vendas/ramo</strong>: Filtro por <strong>Ramo de Atividade</strong>.  
            Parâmetros: <code>ramo_atividade</code> (ex: "Estética").
        </li>
        <li><strong>/vendas/forma_pagamento</strong>: Filtro por <strong>Forma de Pagamento</strong>.  
            Parâmetros: <code>forma_pagamento</code> (ex: "Pix", "Iugu").
        </li>
        <li><strong>/vendas/canal_venda</strong>: Filtro por <strong>Canal de Vendas</strong>.  
            Parâmetros: <code>canal_venda</code> (ex: "Inside Sales").
        </li>
        <li><strong>/vendas/upsell</strong>: Filtro para buscar <strong>Upsells</strong> realizados em um período de tempo.  
            Parâmetros: <code>data_inicio_upsell</code>, <code>data_fim_upsell</code>.
        </li>
        <li><strong>/vendas/downsell</strong>: Filtro para buscar <strong>Downsells</strong> realizados em um período de tempo.  
            Parâmetros: <code>data_inicio_downsell</code>, <code>data_fim_downsell</code>.
        </li>
        <li><strong>/vendas/churn</strong>: Filtro para buscar <strong>Clientes em Churn</strong>.  
            Parâmetros: <code>motivo_churn</code> (ex: "Internalização de equipe").
        </li>
    </ul>

    <h3>1.2 Endpoints de Cálculo e Agregação</h3>
    <p>Esses endpoints realizam cálculos e agregações, como o total de vendas, receita recorrente, etc.</p>

    <ul>
        <li><strong>/vendas/recorrente/squad</strong>: Para calcular a <strong>receita recorrente</strong> de uma Squad.  
            Parâmetros: <code>squad_id</code>, <code>data_inicial</code>, <code>data_final</code>.
        </li>
        <li><strong>/vendas/total/cliente</strong>: Para calcular o <strong>total de vendas</strong> de um cliente, incluindo upsells e downsells.  
            Parâmetros: <code>cliente_id</code>, <code>data_inicial</code>, <code>data_final</code>.
        </li>
        <li><strong>/vendas/total/upsell</strong>: Para calcular o <strong>total de upsells</strong> realizados em um período.  
            Parâmetros: <code>data_inicial</code>, <code>data_final</code>.
        </li>
        <li><strong>/vendas/total/downsell</strong>: Para calcular o <strong>total de downsells</strong> realizados em um período.  
            Parâmetros: <code>data_inicial</code>, <code>data_final</code>.
        </li>
        <li><strong>/vendas/total/churn</strong>: Para calcular a <strong>taxa de churn</strong> de um cliente ou período.  
            Parâmetros: <code>data_inicial</code>, <code>data_final</code>.
        </li>
    </ul>

    <h3>1.3 Endpoints de Relacionamentos e Comunicação</h3>
    <p>Esses endpoints fornecem informações de contato para quem gerencia ou interage com o cliente.</p>

    <ul>
        <li><strong>/contatos/squad/{squad_id}</strong>: Para pegar todos os e-mails dos responsáveis por uma Squad.  
            Parâmetros: <code>squad_id</code> (ex: "SQ002 - Balneário").
        </li>
        <li><strong>/contatos/cliente/{cliente_id}</strong>: Para pegar todos os e-mails dos contatos de um cliente.  
            Parâmetros: <code>cliente_id</code> (ex: "Glas Laser").
        </li>
    </ul>

    <h2>2. Exemplos de Consultas</h2>
    <p>Abaixo estão alguns exemplos de consultas que o agente IA pode fazer utilizando os endpoints mencionados:</p>

    <ul>
        <li><strong>Qual a receita recorrente da Squad Shark?</strong>  
            Chamada ao endpoint <code>/vendas/recorrente/squad</code>, com o parâmetro <code>squad_id="Shark"</code>.
        </li>
        <li><strong>Qual o total de upsells do cliente Glas Laser no ano de 2023?</strong>  
            Chamada ao endpoint <code>/vendas/total/upsell</code>, com os parâmetros <code>cliente_id="Glas Laser"</code>, <code>data_inicial="2023-01-01"</code>, <code>data_final="2023-12-31"</code>.
        </li>
        <li><strong>Quais são os contatos responsáveis pela Squad Balneário?</strong>  
            Chamada ao endpoint <code>/contatos/squad/{squad_id}</code>, com o parâmetro <code>squad_id="SQ002 - Balneário"</code>.
        </li>
        <li><strong>Qual o total de churn do cliente Glas Laser?</strong>  
            Chamada ao endpoint <code>/vendas/total/churn</code>, com os parâmetros <code>cliente_id="Glas Laser"</code> e o intervalo de datas.
        </li>
    </ul>

    <h2>3. Considerações Finais</h2>
    <ul>
        <li><strong>Autenticação e Autorização</strong>: Implementar segurança nos endpoints, como autenticação via JWT, para proteger dados sensíveis.</li>
        <li><strong>Paginação</strong>: Implementar paginação para grandes volumes de dados para evitar sobrecarga no sistema.</li>
        <li><strong>Cache de Resultados</strong>: Usar cache para resultados que não mudam frequentemente, como receita recorrente de uma Squad.</li>
    </ul>
</body>
</html>

"""
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    with open("arquivo.pdf", "wb") as f:
        f.write(response.content)
else:
    print(f"Erro: {response.json()}")