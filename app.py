import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Render Environment kısmından GEMINI_API_KEY değişkenini alır
API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini API istemcisini başlatır
client = genai.Client(api_key=API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # JSON veya Form verisini çek
        data = request.get_json(force=True, silent=True) or request.form or {}
        
        # Frontend'den gelebilecek tüm olası kelimeleri dene
        user_message = data.get("message") or data.get("prompt") or data.get("text") or data.get("user_message") or ""

        # Eğer veri string değilse string'e çevir
        if isinstance(user_message, dict):
            user_message = str(user_message)

        if not str(user_message).strip():
            return jsonify({"error": "Mesaj boş olamaz."}), 400

        # Gemini model çağrısı
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=str(user_message),
        )

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
