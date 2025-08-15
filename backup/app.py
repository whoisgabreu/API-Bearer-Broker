# Flask
from flask import Flask, request, jsonify

# Login Broker
from modules.login_broker import ProjetoBroker

# Ferramentas de Analise
from modules.ferramentas_analise import GoogleTransparency
from modules.ferramentas_analise import MetaAds
# from modules.ferramentas_analise import GoogleBusiness # Reativar quando corrigir erros
# from modules.ferramentas_analise import DuckDuckGo # Reativar quando corrigir erros
from modules.cnpjaAPICustom import coletar_cnpj
from modules.N8N_WebHook import AIAgentCNPJ
from modules.cnpjaAPICustom import criar_lista_fria
from modules.cnpja_api import search

# DOCX > PDF
from modules.pdf_binario import convert_docx_base64_to_pdf
from flask import send_file

# Bibliotecas de suporte
from dotenv import load_dotenv
import os
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

@app.route("/analise/presenca-online", methods=["GET"])
@require_api_key
def presenca_online():

    try:
        cnpj = request.args.get("cnpj")
        business_info = search(cnpj = cnpj)
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
    
@app.route("/analise/coletar-cnpj", methods=["GET"])
# @require_api_key
def coletar_cnp_APIj():

    try:
        nome_socio = request.args.get("socio")
        nome_fantasia = request.args.get("alias")

        # dados_empresa = asyncio.run(coletar_cnpj(nome_socio, nome_fantasia))

        dados_empresa = AIAgentCNPJ(nome_socio, nome_fantasia)

        return jsonify(dados_empresa)
    
    except Exception as e:

        return jsonify(
            {
                "erro": f"{e}"
            }
        ), 400
    
@app.route("/analise/lista-fria", methods=["GET"])
@require_api_key
def criar_lista_fria_API():

    try:
        nome_socio = request.args.get("socio")
        nome_fantasia = request.args.get("alias")

        dados_empresa = asyncio.run(criar_lista_fria(nome_socio, nome_fantasia))

        return jsonify(dados_empresa)
    
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


# @app.route("/convert/docx", methods=["POST"])
# def docx_to_pdf():
#     data = request.get_json()
#     convert_docx_base64_to_pdf(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug = True)