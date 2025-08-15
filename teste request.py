import base64
from tkinter import filedialog

file_path = filedialog.askopenfilename(filetypes = [("DOCX", "*.docx")])

# Ler o arquivo e converter para base64
with open(file_path, "rb") as f:
    docx_base64 = base64.b64encode(f.read()).decode("utf-8")


import requests


url = "https://api.v4lisboatech.com.br/convert/docx"


header = {
    "X-API-KEY": "ccf9d74a30dc58035c50d1d0cb19dd20"
}


payload = {
    "file_base64": docx_base64
}

response = requests.post(url=url, headers = header,json = payload)

print(response.json())

# Caminho do arquivo PDF de saída
output_path = "saida.pdf"

# Converter base64 -> arquivo PDF
with open(output_path, "wb") as f:
    f.write(base64.b64decode(response.json()["pdf_base64"]))