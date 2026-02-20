import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar configuración desde el archivo .env
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

# Configurar Gemini
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

def asistente_ventas_gemini(mensaje_cliente):
    """Gemini analiza y responde como un vendedor experto"""
    prompt = f"""
    Eres un asistente de ventas experto para una empresa. 
    Tu objetivo es ser amable, persuasivo y ayudar al cliente con su pedido.
    
    Mensaje del cliente: {mensaje_cliente}
    
    Respuesta profesional y vendedora:
    """
    response = model.generate_content(prompt)
    return response.text

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    mensaje = data.get("mensaje", "")
    
    if not mensaje:
        return jsonify({"error": "No enviaste un mensaje"}), 400
    
    # Usamos solo Gemini por ahora
    respuesta = asistente_ventas_gemini(mensaje)
    
    return jsonify({"respuesta": respuesta})

@app.route('/', methods=['GET'])
def index():
    return "Servidor de Ventas-IA activo y usando Gemini."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
