from flask import Flask, render_template, request, jsonify
import os
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message","")
    return jsonify({"reply": f"Eco: {msg}"})
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
