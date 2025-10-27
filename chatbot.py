# chatbot.py
# -----------------
# ChatBot de emergencia que espera JSON: {"texto": "...", "lat": "...", "lon": "..."}
# Responde en JSON: {"respuesta": "..."}

from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Mensajes: aquí puedes cambiar los textos si quieres
mensaje_inicial = (
    "Hola, soy tu asistente de emergencias de QuickSecure.\n"
    "Estoy aquí contigo. Por favor, cuéntame lo que está pasando."
)

mensaje_confirmacion = (
    "Gracias por informarme.\n"
    "🚨 Ya estoy notificando a las entidades de emergencia correspondientes.\n"
    "🛰️ Tenemos tu ubicación en todo momento y los equipos están en camino.\n"
    "Mantén la calma, no estás solo/a. Estoy contigo hasta que lleguen."
)

mensaje_despedida = (
    "✅ La comunicación se ha cerrado.\n"
    "Si necesitas ayuda nuevamente, solo vuelve a escribirme.\n"
)

# Lista de despedidas (más puedes agregar)
despedidas = [
    "adios","adiós","bye","chao","chau","hasta luego","nos vemos","me voy",
    "hasta pronto","hasta mañana","cuidate","cuídate","hasta la próxima",
    "ok","okei","okay","vale","listo","dale","bueno","ya fue","gracias",
    "estoy bien","todo bien","no más","gracias bot","terminar","salir","ya"
]

def limpiar_texto(t):
    if not t:
        return ""
    t = t.lower()
    # quitamos todo menos letras, números y caracteres de acentos
    return re.sub(r"[^\w\sáéíóúñ]", " ", t).strip()

@app.route("/mensaje", methods=["POST"])
def procesar_mensaje():
    data = request.get_json(force=True, silent=True) or {}
    texto = limpiar_texto(data.get("texto", ""))
    lat = data.get("lat", None)
    lon = data.get("lon", None)

    # Respuestas
    if any(p in texto for p in despedidas):
        respuesta = mensaje_despedida
    elif texto == "" or texto.isspace():
        respuesta = mensaje_inicial
    else:
        # Ejemplo: personalizar mensaje si se recibió lat/lon
        if lat is not None and lon is not None:
            respuesta = (mensaje_confirmacion +
                         f"\n📍 Recibimos tu ubicación: lat {lat}, lon {lon}.")
        else:
            respuesta = mensaje_confirmacion

    return jsonify({"respuesta": respuesta})

@app.route("/", methods=["GET"])
def index():
    return "API QuickSecure activa. Usa POST /mensaje con JSON {'texto':'...', 'lat':'...', 'lon':'...'}"

if __name__ == "__main__":
    # Solo para pruebas locales; en PythonAnywhere no se usa este run directamente
    app.run(port=5000, debug=True)
