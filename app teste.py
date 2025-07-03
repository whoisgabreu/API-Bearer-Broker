from flask import Flask, request, jsonify
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import uuid
import asyncio
from modules.login_broker import ProjetoBroker
from modules.ferramentas_analise import GoogleTransparency
from modules.ferramentas_analise import GoogleBusiness
from modules.ferramentas_analise import DuckDuckGo
from modules.cnpjaAPICustom import coletar_cnpj
from modules.cnpja_api import search
from dotenv import load_dotenv
import os
from threading import Lock

app = Flask(__name__)
load_dotenv()

API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

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
        # business_info = GoogleBusiness().analyse(business_info) # Reativar quanto corrigir o problema
        business_info["paginas_online"] = []
        business_info["paginas_online"].append(DuckDuckGo().buscar(business_info["empresa"]["nome_fantasia"], ".br"))
        business_info["paginas_online"].append(DuckDuckGo().buscar(business_info["empresa"]["nome_fantasia"], "instagram.com"))
        business_info["paginas_online"].append(DuckDuckGo().buscar(business_info["empresa"]["nome_fantasia"], "facebook.com"))

        return jsonify(business_info)
    
    except Exception as e:

        return jsonify(
            {
                "erro": f"{e}"
            }
        ), 400
    
@app.route("/analise/coletar-cnpj", methods=["GET"])
@require_api_key
def coletar_cnp_APIj():

    try:
        nome_socio = request.args.get("socio")
        nome_fantasia = request.args.get("alias")

        dados_empresa = coletar_cnpj(nome_socio, nome_fantasia)

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


bot = Bot(token=TOKEN)
@app.route("/telegram/send", methods=["POST"])
def send_message():
    data = request.get_json()
    salesforce_id = data.get("id") or str(uuid.uuid4())[:8]
    value = data.get("value")
    alias = data.get("alias")
    name = data.get("name")
    cnae = data.get("cnae")
    founded = data.get("founded")
    cnpj = data.get("cnpj")
    equity = data.get("equity")
    person = data.get("person")
    role = data.get("role")



    keyboard = [
        [InlineKeyboardButton("Comprar", callback_data=f"buy:{salesforce_id}")],
        [InlineKeyboardButton("Não Comprar", callback_data=f"pass:{salesforce_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    lead_text = f"""
ID SalesForce: {salesforce_id}

Valor do Lead: {value}

CNPJ: {cnpj}
Nome Fantasia: {alias}
Razão Social: {name}
Fundado em: {founded}

Capital Social: {equity}
Atividade Principal: {cnae}

Nome Sócio: {person}
Cargo: {role}
    """

    # Como telegram.Bot usa métodos assíncronos, precisamos rodar com asyncio
    asyncio.run(bot.send_message(
        chat_id=CHAT_ID,
        # text=f"Nova solicitação ID: {salesforce_id}",
        text = lead_text,
        reply_markup=reply_markup
    ))

    return jsonify({"status": "ok", "id": salesforce_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
