from flask import Flask, render_template, request, jsonify
import re, requests, urllib.parse, random, time
app = Flask(__name__)

def get_key():
    try:
        raw = open('groq.key','r').read().strip()
        m = re.search(r'gsk_[A-Za-z0-9_]+', raw)
        return m.group(0) if m else raw
    except: return None

@app.route('/')
def home(): return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    msg = request.get_json().get('message','').strip()
    low = msg.lower()
    if not msg: return jsonify({"reply":""})

    # IMAGEM = infinita
    if any(w in low for w in ["imag","foto","desen","pato","cachorro","gato","vaca","crie","gere","cria","gera"]):
        prompt = re.sub(r'gere|gera|crie|cria|imagem de|foto de|desenhe', '', msg, flags=re.I).strip()
        if len(prompt) < 3: prompt = msg
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=768&height=768&nologo=true&seed={random.randint(1,9999999)}"
        return jsonify({"reply": f"__IMAGE__{url}__ {prompt}"})

    key = get_key()
    modelos = ["openai/gpt-oss-20b","openai/gpt-oss-120b","groq/compound-mini","llama3-8b-8192","gemma2-9b-it"]

    for modelo in modelos:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={
                    "model": modelo,
                    "messages": [
                        {"role":"system","content":"Você é NEXO PRO MAX, assistente brasileiro inteligente. Responda sempre como IA, nunca com frase pronta. Seja natural."},
                        {"role":"user","content": msg}
                    ],
                    "max_tokens": 250,
                    "temperature": 0.8
                }, timeout=15)
            j = r.json()
            if 'choices' in j and j['choices']:
                return jsonify({"reply": j['choices'][0]['message']['content']})
        except:
            continue

    # Se tudo falhar, não mostra ERRO, só pede pra tentar de novo (sem mensagem programada)
    return jsonify({"reply": "Tive uma instabilidade aqui, manda de novo?"})

if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)
