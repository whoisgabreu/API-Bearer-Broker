import os
import uuid
import asyncio
from threading import Lock

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Header, Depends, Query
from fastapi.responses import JSONResponse
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from modules.login_broker import ProjetoBroker
from modules.ferramentas_analise import GoogleTransparency, GoogleBusiness, DuckDuckGo
from modules.cnpjaAPICustom import coletar_cnpj
from modules.cnpja_api import search

load_dotenv()

API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = FastAPI()
bot = Bot(token=TOKEN)

selenium_lock = Lock()

# Middleware de autenticação por header
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# --- Endpoints ---

@app.get("/analise/presenca-online")
async def presenca_online(
    cnpj: str = Query(...),
    _: str = Depends(verify_api_key)
):
    try:
        business_info = search(cnpj=cnpj)
        business_info = GoogleTransparency().analyse(business_info)
        # business_info = GoogleBusiness().analyse(business_info)  # Reativar se necessário
        business_info["paginas_online"] = [
            DuckDuckGo().buscar(business_info["empresa"]["nome_fantasia"], ".br"),
            DuckDuckGo().buscar(business_info["empresa"]["nome_fantasia"], "instagram.com"),
            DuckDuckGo().buscar(business_info["empresa"]["nome_fantasia"], "facebook.com"),
        ]
        return JSONResponse(content=business_info)
    except Exception as e:
        return JSONResponse(status_code=400, content={"erro": str(e)})

@app.get("/analise/coletar-cnpj")
async def coletar_cnpj_api(
    socio: str = Query(...),
    alias: str = Query(...),
    _: str = Depends(verify_api_key)
):
    try:
        dados_empresa = await coletar_cnpj(socio, alias)
        return JSONResponse(content=dados_empresa)
    except Exception as e:
        return JSONResponse(status_code=400, content={"erro": str(e)})

@app.get("/broker/extrair_bearer")
async def extrair_bearer(_: str = Depends(verify_api_key)):
    with selenium_lock:
        try:
            bearer = ProjetoBroker().extrair_bearer()
            return JSONResponse(content={"broker_bearer": bearer})
        except Exception as e:
            return JSONResponse(status_code=400, content={"erro": str(e)})

@app.post("/telegram/send")
async def send_message(
    request: Request,
    _: str = Depends(verify_api_key)
):
    data = await request.json()
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

    # Agora é assíncrono de forma nativa!
    await bot.send_message(
        chat_id=CHAT_ID,
        text=lead_text,
        reply_markup=reply_markup
    )

    return {"status": "ok", "id": salesforce_id}
