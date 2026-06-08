import os
import httpx
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# 🔐 Aktif Groq API Anahtarın
API_KEY = "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"

@app.route('/')
def index():
    return render_template('index.html')

# 📱 HEM WEB HEM MOBİL DESTEKLİ CHAT ENDPOINT'I
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = ""

        # 1. Yol: Eğer istek Mobil Uygulamadan JSON olarak geldiyse
        if request.is_json:
            data = request.get_json()
            user_message = data.get('mesaj', '')
        
        # 2. Yol: Eğer istek mevcut Web Arayüzünden Form verisi olarak geldiyse
        else:
            user_message = request.form.get('mesaj', '')

        # Mesaj kontrolü
        if not user_message:
            return jsonify({'error': 'Mesaj boş olamaz kanka.'}), 400

        # 🛠️ HTTPX İstemci Yapılandırması
        custom_client = httpx.Client()
        client = Groq(
            api_key=API_KEY,
            http_client=custom_client
        )

        # 🚀 Llama 3.1 Modeli Tetikleme
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        bot_response = completion.choices[0].message.content
        
        # 🎯 Standart JSON Çıktısı (Hem Mobil Hem Web Anlar)
        return jsonify({'cevap': bot_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
