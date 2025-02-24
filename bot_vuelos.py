import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# API Key de Skyscanner (cámbiala por la tuya)
SKYSCANNER_API_KEY = "bfea23ac4bmsh13d29d7b00e3c08p185fb9jsn4635ca417000"
BOT_TOKEN = "8094024293:AAEaEYiqQdjIm52ZRnMq8V8OhHbj6291mhk"

# Función para buscar vuelos en una fecha específica
def buscar_vuelo(update: Update, context: CallbackContext):
    try:
        if len(context.args) < 3:
            update.message.reply_text("Uso: /vuelo ORIGEN DESTINO FECHA(YYYY-MM-DD)")
            return

        origen, destino, fecha = context.args
        url = "https://skyscanner44.p.rapidapi.com/search"

        params = {
            "adults": "1",
            "origin": origen,
            "destination": destino,
            "departureDate": fecha,
            "currency": "USD"
        }

        headers = {
            "X-RapidAPI-Key": SKYSCANNER_API_KEY,
            "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            itineraries = data.get("itineraries", [])

            if itineraries:
                vuelo = itineraries[0]
                precio = vuelo.get("price", {}).get("formatted", "No disponible")
                aerolinea = vuelo.get("legs", [{}])[0].get("carriers", {}).get("marketing", [{}])[0].get("name", "Desconocida")

                update.message.reply_text(f"✈️ Vuelo encontrado:\n📌 Aerolínea: {aerolinea}\n💰 Precio: {precio}")
            else:
                update.message.reply_text("❌ No se encontraron vuelos para esa fecha.")

        else:
            update.message.reply_text("❌ Error al buscar vuelos. Intenta más tarde.")

    except Exception as e:
        update.message.reply_text(f"⚠️ Error interno: {str(e)}")

# Función para buscar vuelos en un mes completo
def buscar_vuelo_mes(update: Update, context: CallbackContext):
    try:
        if len(context.args) < 3:
            update.message.reply_text("Uso: /mes ORIGEN DESTINO AAAA-MM")
            return

        origen, destino, mes = context.args
        url = "https://skyscanner44.p.rapidapi.com/search-month"

        params = {
            "adults": "1",
            "origin": origen,
            "destination": destino,
            "year": mes.split("-")[0],
            "month": mes.split("-")[1],
            "currency": "USD"
        }

        headers = {
            "X-RapidAPI-Key": SKYSCANNER_API_KEY,
            "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            vuelos = data.get("bestPrices", [])

            if vuelos:
                mensaje = "✈️ Mejores precios para el mes:\n"
                for vuelo in vuelos[:5]:  # Solo los primeros 5 vuelos
                    fecha = vuelo.get("departureDate", "Desconocida")
                    precio = vuelo.get("price", {}).get("formatted", "No disponible")
                    mensaje += f"📅 {fecha} - 💰 {precio}\n"
                update.message.reply_text(mensaje)
            else:
                update.message.reply_text("❌ No se encontraron vuelos en ese mes.")

        else:
            update.message.reply_text("❌ Error al buscar vuelos. Intenta más tarde.")

    except Exception as e:
        update.message.reply_text(f"⚠️ Error interno: {str(e)}")

# Función de inicio
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hola! Usa /vuelo ORIGEN DESTINO FECHA o /mes ORIGEN DESTINO AAAA-MM para buscar vuelos.")

# Configurar el bot
updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("vuelo", buscar_vuelo))
dp.add_handler(CommandHandler("mes", buscar_vuelo_mes))  # Nuevo comando para búsqueda mensual

# Iniciar el bot
updater.start_polling()
updater.idle()
