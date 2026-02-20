from flask import Flask, request, jsonify

app = Flask(__name__)

# ==========================
# CONFIGURACIÓN BÁSICA
# ==========================

ACCESS_TOKEN = "TU_ACCESS_TOKEN_AQUI"
VERIFY_TOKEN = "ventas_ia_token"

# ==========================
# WEBHOOK VERIFICACIÓN META
# ==========================

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge
    return "Token incorrecto", 403


# ==========================
# RECEPCIÓN DE MENSAJES
# ==========================

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message["text"]["body"]

        print(f"Mensaje recibido de {sender}: {text}")

        # RESPUESTA INTELIGENTE BÁSICA
        reply = generar_respuesta(text)

        return jsonify({"status": "ok"})
    except:
        return jsonify({"status": "no message"})


# ==========================
# IA BÁSICA DE VENTAS
# ==========================

def generar_respuesta(texto):
    texto = texto.lower()

    if "precio" in texto:
        return "Claro, tenemos planes desde $389 pesos mensuales. ¿Deseas instalar en casa o negocio?"

    elif "internet" in texto:
        return "Manejamos fibra óptica con instalación rápida. ¿En qué colonia te encuentras?"

    elif "promoción" in texto:
        return "Tenemos promoción de instalación sin costo este mes."

    else:
        return "Hola 👋 Gracias por tu mensaje. ¿Buscas internet para casa o negocio?"


# ==========================
# INICIO SERVIDOR
# ==========================

if __name__ == "__main__":
    app
