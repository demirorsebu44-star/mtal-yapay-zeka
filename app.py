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

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Arayüzden gelen mesajı alıyoruz
        user_message = request.form.get('mesaj', '')
        
        if not user_message:
            return jsonify({'error': 'Mesaj boş olamaz kanka.'}), 400

        # 🛠️ GUNICORN & HTTPX ÇAKIŞMA ÇÖZÜMÜ:
        # Parametresiz, temiz bir httpx istemcisini fonksiyon içinde yaratarak uyuşmazlıkları engelliyoruz.
        custom_client = httpx.Client()
        
        client = Groq(
            api_key=API_KEY,
            http_client=custom_client
        )

        # 🚀 GÜNCEL MODEL:
        # Kapatılan eski model yerine Groq'un aktif olarak desteklediği güncel modeli tetikliyoruz.
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        bot_response = completion.choices[0].message.content
        return jsonify({'cevap': bot_response})

    except Exception as e:
        # Sunucunun çökmesini önlemek için hatayı yakalayıp arayüze güvenli bir şekilde basıyoruz
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
