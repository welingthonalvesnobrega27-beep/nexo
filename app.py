from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Tenta importar openai, se não tiver, roda em modo eco
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    HAS_OPENAI = True
except:
    HAS_OPENAI = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        msg = data.get("message", "").strip()
        if not msg:
            return jsonify({"reply": "Manda uma mensagem aí!"})

        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key or not HAS_OPENAI:
            return jsonify({"reply": f"[MODO TESTE - sem chave] Você disse: {msg}. Coloca a OPENAI_API_KEY no Render pra ficar inteligente."})

        # Chamada GPT
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é o NEXO Pro, um assistente útil que fala em português do Brasil, direto e esperto."},
                {"role": "user", "content": msg}
            ]
        )
        reply = resp.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"ERRO NO CHAT: {e}")
        return jsonify({"reply": f"Deu erro aqui, mas já voltei: {str(e)[:200]}"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
