import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# 🔹 CONFIGURACIÓN (Reemplaza con tus datos)
TELEGRAM_TOKEN = "8094024293:AAEaEYiqQdjIm52ZRnMq8V8OhHbj6291mhk"  # Token del bot de @BotFather
AMADEUS_API_KEY = "A8XQ2p7Ll8EKGpGBGZAkTX3S4uLAJAMW" # API Key de Amadeus
AMADEUS_API_SECRET = "O5MpGC6fsor28AdW"  # API Secret de Amadeus

# URLs de la API de Amadeus
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_SEARCH_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

# 🔹 FUNCIÓN PARA OBTENER TOKEN DE AMADEUS
def obtener_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY,
        "client_secret": AMADEUS_API_SECRET
    }
    response = requests.post(TOKEN_URL, data=payload)
    return response.json().get("access_token")

# 🔹 FUNCIÓN PARA OBTENER PRECIO DEL VUELO
def obtener_precio(origen, destino, fecha):
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": origen,
        "destinationLocationCode": destino,
        "departureDate": fecha,
        "adults": 1,
        "currencyCode": "EUR",
        "max": 1
    }

    response = requests.get(FLIGHT_SEARCH_URL, headers=headers, params=params)
    data = response.json()

    if "data" in data and data["data"]:
        vuelo = data["data"][0]
        precio = vuelo["price"]["total"]
        aerolinea = vuelo["validatingAirlineCodes"][0]
        return f"✈️ Vuelo más barato de {origen} a {destino} el {fecha}:\n💰 Precio: {precio}€\n🛫 Aerolínea: {aerolinea}"
    
    return "❌ No se encontraron vuelos para esa fecha."

# 🔹 FUNCIÓN PARA RESPONDER EN TELEGRAM
async def precio(update: Update, context: CallbackContext):
    if len(context.args) != 3:
        await update.message.reply_text("✈️ Uso: /precio ORIGEN DESTINO YYYY-MM-DD\nEjemplo: /precio MAD BCN 2024-03-10")
        return
    
    origen, destino, fecha = context.args
    mensaje = obtener_precio(origen, destino, fecha)
    await update.message.reply_text(mensaje)

# 🔹 CONFIGURAR EL BOT
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("precio", precio))

    print("✅ Bot en funcionamiento...")
    app.run_polling()

# 🔹 INICIAR EL BOT
if __name__ == "__main__":
    main()
