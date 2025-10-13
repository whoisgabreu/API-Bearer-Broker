# Flask
from flask import Flask, request, jsonify, Response

# Login Broker
from modules.login_broker import ProjetoBroker

# Ferramentas de Analise
from modules.ferramentas_analise import GoogleTransparency
from modules.ferramentas_analise import MetaAds
from modules.N8N_WebHook import AIAgentCNPJ
# from modules.ferramentas_analise import GoogleBusiness # Reativar quando corrigir erros
# from modules.ferramentas_analise import DuckDuckGo # Reativar quando corrigir erros

# DOCX > PDF
from modules.pdf_binario import convert_docx_base64_to_pdf

# HTML > PDF
# import xhtml2pdf.pisa as pisa
# import io
import re
from weasyprint import HTML


# Carregar encoder e modelo
import joblib
import pandas as pd

# Bibliotecas de suporte
from dotenv import load_dotenv
import os
import subprocess
from threading import Lock
import asyncio

modelo = joblib.load("modules/modelo/modelo_classificador_com_termos_do_forms - V2.joblib")
encoder = joblib.load("modules/modelo/encoder_classificador_com_termos_do_forms.joblib")

app = Flask(__name__)
load_dotenv()

API_KEY = os.getenv("API_KEY")
selenium_lock = Lock()  # lock global

def require_api_key(func):
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-KEY")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@app.route("/analise/lead", methods=["GET"])
# /analise/lead?socio=NOME&alias=NOME
@require_api_key
def presenca_online():

    try:
        alias = request.args.get("empresa")
        socio = request.args.get("socio")
        business_info = AIAgentCNPJ(alias, socio)
        business_info = GoogleTransparency().analyse(business_info)
        business_info = MetaAds().analyse(business_info)
        # business_info = GoogleBusiness().analyse(business_info) # Reativar quanto corrigir o problema
        # business_info["paginas_online"] = []
        # business_info["paginas_online"].append(DuckDuckGo().buscar(business_info["empresa"]["nome_fantasia"], ".br"))
        # business_info["paginas_online"].append(DuckDuckGo().buscar(business_info["empresa"]["nome_fantasia"], "instagram.com"))
        # business_info["paginas_online"].append(DuckDuckGo().buscar(business_info["empresa"]["nome_fantasia"], "facebook.com"))

        return jsonify(business_info)
    
    except Exception as e:

        return jsonify(
            {
                "erro": f"{e}"
            }
        ), 400

# ------------------------ TEMPORÁRIO ------------------
@app.route("/analise/lead2", methods=["GET"])
# /analise/lead?socio=NOME&alias=NOME
@require_api_key
def presenca_online2():

    try:
        business_info = GoogleTransparency().analyse(business_info)
        business_info = MetaAds().analyse(business_info)

        return jsonify(business_info)
    
    except Exception as e:

        return jsonify(
            {
                "erro": f"{e}"
            }
        ), 400
# ---------------------------------------------------------


@app.route("/broker/extrair_bearer", methods=["GET"])
@require_api_key
def extrair_bearer():
    with selenium_lock:
        try:
            bearer = ProjetoBroker().extrair_bearer()
            return jsonify({"broker_bearer": bearer})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400



### Conversor de Documentos

# DOCX > PDF
@app.route("/convert/docx", methods=["POST"])
@require_api_key
def convert_docx_endpoint():
    data = request.get_json()

    if not data or 'file_base64' not in data:
        return jsonify({"error": "Campo 'file_base64' não encontrado"}), 400

    try:
        pdf_bytes = convert_docx_base64_to_pdf(data['file_base64'])

        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={
                "Content-Disposition": "inline; filename=arquivo.pdf"
            }
        )
    except:
        pass

# HTML > PDF
# @app.route("/convert/html", methods=["POST"])
# @require_api_key
# def convert_html_endpoint():
#     data = request.get_json()

#     if not data or 'html_content' not in data:
#         return jsonify({"error": "Campo 'html_content' não encontrado"}), 400

#     try:
#         html_content = data['html_content']

#         # Converte HTML para PDF em memória
#         pdf_io = io.BytesIO()
#         pisa_status = pisa.CreatePDF(html_content, dest=pdf_io)

#         if pisa_status.err:
#             return jsonify({"error": "Erro ao converter HTML para PDF"}), 500

#         pdf_bytes = pdf_io.getvalue()

#         return Response(
#             pdf_bytes,
#             mimetype='application/pdf',
#             headers={
#                 "Content-Disposition": "inline; filename=arquivo.pdf"
#             }
#         )
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@app.route("/convert/html", methods=["POST"])
@require_api_key
def convert_html_endpoint():
    data = request.get_json()
    if not data or 'html_content' not in data:
        return jsonify({"error": "Campo 'html_content' não encontrado"}), 400

    css = """
        @page {
            size: Letter;
            margin: 5mm;
        }

        body {
            margin: 0;
            padding: 0;
        }

        .container {
            page-break-inside: avoid;
            transform: scale(0.96);
            transform-origin: top left;
        }
    """

    html_content = data['html_content']

    # html_content = re.sub(r"(<style>)", r"\1\n{}".format(css), html_content)

    pdf_bytes = HTML(string=html_content).write_pdf()

    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={"Content-Disposition": "inline; filename=arquivo.pdf"}
    )


# Classificação por ML
@app.route("/ml/lead", methods = ["POST"])
# @require_api_key
def classificacao_ml():
    # Verifica se o corpo da requisição é JSON
    if not request.is_json:
        return jsonify({'erro': 'Requisição precisa ser JSON'}), 400

    # Pega o JSON da requisição
    dados = request.get_json()


    # Campos esperados
    campos_esperados = [
        "faturamento",
        "cargo",
        "nivel_urgencia",
        "tem_site",
        "tem_anuncio",
        "segmento"
    ]

    # Verifica se todos os campos estão presentes
    for campo in campos_esperados:
        if campo not in dados:
            return jsonify({'erro': f'Campo "{campo}" ausente'}), 400


    dado = encoder.transform(pd.DataFrame([dados]))
    predicao = modelo.predict(dado)
    certeza = max(modelo.predict_proba(dado)[0])


    # Aqui você pode fazer o que quiser com os dados, por exemplo:
    return jsonify({
        'mensagem': 'Dados recebidos com sucesso',
        'decisao': predicao.tolist()[0],
        'certeza': f"{float(certeza)*100}%"
        }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug = True)