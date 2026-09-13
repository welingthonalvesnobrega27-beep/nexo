from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/')
def home():
    try:
        with open('index.html','r',encoding='utf-8') as f:
            return f.read()
    except:
        return "<h1>NEXO no ar</h1>"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    msg = data.get('message','')
    if not msg:
        return jsonify({"reply":"Fala comigo!"})
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"Você é NEXO Pro, assistente criado por Welingthon, direto, útil, brasileiro."},
                {"role":"user","content": msg}
            ]
        )
        return jsonify({"reply": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"ERRO IA: {str(e)[:200]}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",5000)))
