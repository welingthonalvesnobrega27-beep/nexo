from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    try:
        with open('index.html','r',encoding='utf-8') as f:
            return f.read()
    except:
        return "<h1>NEXO Pro</h1><p>index.html não encontrado</p>"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    msg = data.get('message','')
    return jsonify({"reply": f"[MODO TESTE OK] Você disse: {msg}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
