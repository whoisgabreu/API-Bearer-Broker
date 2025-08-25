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


import requests

url = "http://192.168.4.102:5000/ml/lead"

body = {
        "faturamento": "De 401 mil à 1 milhão",
        "cargo": "Não Sócio",
        "nivel_urgencia": "Em até três meses",
        "tem_site": "Não",
        "tem_anuncio": "Não",
        "segmento": "Foodservice"
    }

r = requests.post(url = url, json = body)

print(r.json())