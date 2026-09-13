from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        msg = data.get("message", "")
        # aqui vai sua lógica do OpenAI
        return jsonify({"reply": f"Você disse: {msg}"})
    except Exception as e:
        return jsonify({"reply": f"Tive uma instabilidade aqui, manda de novo? Erro: {e}"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
