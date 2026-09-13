from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    msg = data.get('message','')
    if not msg:
        return jsonify({"reply":"Oi! Como posso ajudar?"}), 200
    # MODO TESTE GARANTIDO - funciona sem chave
    return jsonify({"reply": f"[MODO TESTE - sem chave] Você disse: {msg}"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
