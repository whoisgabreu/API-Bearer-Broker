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

url = "http://127.0.0.1:5000/convert/html"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer seu_api_key",
    "X-API-KEY": "ccf9d74a30dc58035c50d1d0cb19dd20"
}
data = {
    "html_content": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Travel Voucher - Brazil Booking</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Montserrat', Arial, sans-serif; 
            background-color: #f4f4f4; 
            margin: 0; 
            padding: 0; 
        }
        .container { 
            max-width: 700px; 
            margin: 20px auto; 
            background: #ffffff; 
            border-radius: 10px; 
            border: 2px solid #006400; 
            padding: 20px; 
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); 
            position: relative; 
        }
        .header { 
            text-align: center; 
            padding: 20px; 
            background-color: #006400; 
            border-top-left-radius: 10px; 
            border-top-right-radius: 10px; 
        }
        .header img { width: 120px; height: auto; }
        h2 { 
            color: #006400; 
            font-size: 20px; 
            text-align: center; 
            font-weight: 700; 
            margin-top: 10px; 
            margin-bottom: 8px; 
        }
        .voucher-info { 
            text-align: center; 
            font-size: 15px; 
            font-weight: 600; 
            margin-bottom: 8px; 
            color: #333; 
        }
        .details { 
            font-size: 14px; 
            color: #333; 
            line-height: 1.4; 
            padding: 10px; 
            border: 2px solid #006400; 
            border-radius: 6px; 
            background: #f9f9f9; 
            margin-top: 10px; 
        }
        .details p { margin: 5px 0; }
        .section-title { 
            font-weight: 700; 
            color: #006400; 
            margin-top: 22px; 
            font-size: 18px; 
            text-align: center; 
        }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 8px; 
        }
        th, td { 
            border: 1px solid #ccc; 
            padding: 8px; 
            text-align: left; 
            font-size: 14px; 
        }
        th { 
            background: #006400; 
            color: #ffffff; 
            font-weight: 700; 
            text-align: center; 
        }
        .footer { 
            font-size: 12px; 
            color: #444; 
            margin-top: 20px; 
            text-align: center; 
            padding-top: 10px; 
            border-top: 1px solid #ccc; 
        }
        .green-title {
            color: #006400;
            font-weight: 700;
            font-size: 18px;
            margin-top: 15px;
            display: block;
        }
        .bold {
            font-weight: 700;
        }
    </style>
</head>
<body>

<!-- Página 1 -->
<div class="container">
    <div class="header">
        <img src="https://brazilbooking.com/wp-content/uploads/2025/04/brazilbooking_logo.png" alt="Brazil Booking Logo">
    </div>

    <h2>Travel Voucher</h2>
    <div class="voucher-info">
        <p><strong></strong> BB{30.ID_Order}</p>
    </div>

    <div class="details">
        <p><strong>Order Date:</strong> {30.Data_Order}</p>
        <p><strong>Order Total:</strong> {87.currency_symbol} {87.total}</p>
        <p><strong>Customer Name:</strong> {30.Nome_Cliente}</p>
        <p><strong>Address:</strong> {30.Endereço}}</p>
        <p><strong>Phone:</strong> {30.Telefone_Cliente}</p>
        <p><strong>Email:</strong> {30.Email_Cliente}</p>
    </div>

    <div class="section-title">Trip Details</div>
    <table>
        <tr>
           <th style="text-align: center;">Travel Date</th>
        <th style="text-align: center;">Service</th>
  <th style="text-align: center;">Paid</th>
        <th style="text-align: center;">Pax</th>
<th style="text-align: center;">Accomodation</th>
        </tr>

        <tr>
            <td style="text-align: center;">{33.DataAgendada_Produto_1}</td>
            <td style="text-align: center;">{33.Nome_Produto_1}</td>
            <td style="text-align: center;">{33.Preco_Produto_1}</td>
            <td style="text-align: center;">{33.Quantidade_Produto_1}</td>
            <td style="text-align: center;">{33.Acommodation_Produto_1}</td>
        </tr>

        <tr>
            <td style="text-align: center;">{33.DataAgendada_Produto_2}</td>
            <td style="text-align: center;">{33.Nome_Produto_2}</td>
            <td style="text-align: center;">{33.Preco_Produto_2}</td>
            <td style="text-align: center;">{33.Quantidade_Produto_2}</td>
            <td style="text-align: center;">{33.Acommodation_Produto_2}</td>
           
        </tr>

        <tr>
            <td style="text-align: center;">{33.DataAgendada_Produto_3}</td>
            <td style="text-align: center;">{33.Nome_Produto_3}</td>
            <td style="text-align: center;">{33.Preco_Produto_3}</td>
            <td style="text-align: center;">{33.Quantidade_Produto_3}</td>
            <td style="text-align: center;">{33.Acommodation_Produto_3}</td>
        </tr>
    
    </table>

    <div class="section-title">Check-in Informations</div>
    <div class="details">
        <p><strong>Boat & Departure:</strong> Instructions in WhatsApp</p>
      </div>

    <div class="section-title">Cancellation Policy</div>
    <div class="details">
        <ul>
            <li><strong>If your first tour is ON OR AFTER the 7th day</strong> from purchase, you can cancel anytime within <strong>7 days</strong>, until <strong>12:00 PM (GMT) on the last day.</strong></li>

<br>

            <li><strong>If your first tour is BEFORE the 7th day</strong>, you can cancel <strong>up to 1 day  before the first tour</strong>, until <strong>12:00 PM (GMT) on the last day.</strong></li>
         </ul>
    </div>

    <div class="footer">
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td><strong>Amazon Eco Travel</strong><br>Rua Barão do Rio Branco, 1333, Manaus, AM, Brazil<br>Phone: +55 31 98107-9897</td>
                <td><strong>Amazon Eco Travel Inc.</strong><br>5348 Vegas Drive, Las Vegas, NV, USA<br>Phone: +1 307 454-0321</td>
                <td><strong>Amazon Eco Travel Ltd.</strong><br>71-75 Shelton Street, Covent Garden, London, UK</td>
            </tr>
        </table>
    </div>
</div>

<!-- Páginas de Produtos (2 a 6) -->
<div class="container" style="page-break-before: always;">
<div class="section-title">Important Notice</div>
    <div class="details">
        <ul>
            <li><strong>Weather Conditions:</strong> Your safety is our priority! Weather events may affect the tour, leading to itinerary changes and an unusual experience. Refunds are not available due to these adjustments.</li>

            <br>

            <li><strong>Beware of Scams!</strong> Do not accept offers from unauthorized individuals, including those claiming to change your booking during the trip. Refunds will not be provided for cancellations due to third-party arrangements.</li>
        </ul>
    </div>
    
    <h2>General Informations and Trip Schedule</h2>
    <div class="details">
        <span class="green-title"><strong>Product:</strong></span>
        <p class="bold">{76.`3`}</p>
        <p>{76.`5`}</p>
    </div>
</div>

<div class="container" style="page-break-before: always;">
    <h2>General Informations and Trip Schedule</h2>
    <div class="details">
        <span class="green-title"><strong>Product:</strong></span>
        <p class="bold">{77.`3`}</p>
        <p>{77.`5`}</p>
    </div>
</div>

<div class="container" style="page-break-before: always;">
    <h2>General Informations and Trip Schedule</h2>
    <div class="details">
        <span class="green-title"><strong>Product:</strong></span>
        <p class="bold">{78.`3`}</p>
        <p>{78.`5`}</p>
    </div>
</div>

<div class="container" style="page-break-before: always;">
    <h2>General Informations and Trip Schedule</h2>
    <div class="details">
        <span class="green-title"><strong>Product:</strong></span>
        <p class="bold">{79.`3`}</p>
        <p>{79.`5`}</p>
    </div>
</div>

</body>
</html>
"""
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    with open("html-result.pdf", "wb") as f:
        f.write(response.content)
else:
    print(f"Erro: {response.json()}")