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
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Mesaj boş olamaz."}), 400

        # Doğru model adı ve virgüllerle eksiksiz yapı
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_message,
        )

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
