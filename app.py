from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"<h1>Erro: {e}</h1><p>Crie templates/index.html</p>", 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if not client:
            return jsonify({"reply": "GROQ_API_KEY nao configurada no Render"})

        data = request.get_json(force=True)
        msg = data.get('message','').strip()
        if not msg:
            return jsonify({"reply": "Manda uma mensagem ai!"})

        comp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role":"system","content":"Voce e o NEXO, IA criada em Goiania. Seja parceiro e direto."},
                {"role":"user","content":msg}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return jsonify({"reply": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"ERRO: {str(e)}"}), 200

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
