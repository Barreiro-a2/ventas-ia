import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import google.generativeai as genai

# Cargar configuración secreta
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# --- LÓGICA DE IA ---

def analizar_con_gemini(texto):
    """Gemini analiza los detalles técnicos"""
    model = genai.GenerativeModel('gemini-pro')
    res = model.generate_content(f"Resume este pedido: {texto}")
    return res.text

def vender_con_openai(resumen):
    """OpenAI redacta el mensaje de venta persuasivo"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Eres un vendedor experto."},
                  {"role": "user", "content": f"Cierra esta venta: {resumen}"}]
    )
    return response.choices[0].message.content

# --- RUTAS ---

@app.route('/webhook', methods=['POST'])
def handle_message():
    data = request.get_json()
    # Aquí iría la lógica para recibir mensajes de WhatsApp/Meta
    return jsonify({"status": "recibido"}), 200

if __name__ == "__main__":
    app.run(port=5000)

