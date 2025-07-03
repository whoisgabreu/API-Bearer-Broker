# bot.py
import asyncio
import aiohttp
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes,
)
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, message_id = query.data.split(":")
    print(_)
    print(f"Botão clicado: ID {message_id}")

    if _ == "buy":
        async with aiohttp.ClientSession() as session:
            async with session.get("https://n8n.v4lisboatech.com.br/webhook/82c3cc86-a2ef-48e5-995e-78c20409d665") as resp:
                # opcional: verificar resp.status, ler resp.text() etc
                pass
        await query.edit_message_text(
            text=f"Salesforce ID: {message_id} - Realizada Ordem de Compra ✅",
        )

    else:
        await query.edit_message_text(
            text=f"Salesforce ID: {message_id} - Ignorado ❎"
        )

app.add_handler(CallbackQueryHandler(button_handler))

if __name__ == "__main__":
    app.run_polling()   # 🚫 sem asyncio.run()
