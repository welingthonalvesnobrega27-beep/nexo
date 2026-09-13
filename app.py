from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get('message', '')

        if not user_msg:
            return jsonify({"reply": "Manda uma mensagem ai"})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é o NEXO, uma IA útil, direta e brasileira."},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=1024
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"ERRO GROQ: {e}")
        return jsonify({"reply": f"ERRO GROQ: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
