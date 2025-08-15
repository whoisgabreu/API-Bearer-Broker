# Flask
from flask import Flask, request, jsonify

# Login Broker
from modules.login_broker import ProjetoBroker

# Ferramentas de Analise
from modules.ferramentas_analise import GoogleTransparency
from modules.ferramentas_analise import MetaAds
from modules.N8N_WebHook import AIAgentCNPJ
from modules.pdf_binario import convert_docx_base64_to_pdf
# from modules.ferramentas_analise import GoogleBusiness # Reativar quando corrigir erros
# from modules.ferramentas_analise import DuckDuckGo # Reativar quando corrigir erros

# DOCX > PDF
from modules.pdf_binario import convert_docx_base64_to_pdf
from flask import send_file

# Bibliotecas de suporte
from dotenv import load_dotenv
import os
import subprocess
from threading import Lock
import asyncio

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
        pdf_b64 = convert_docx_base64_to_pdf(data['file_base64'])
        return jsonify({"pdf_base64": pdf_b64})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Falha na conversão com LibreOffice", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Erro geral", "details": str(e)}), 500


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug = True)