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

        # 🛠️ HATAYI KÖKTEN ÇÖZEN KISIM:
        # Hiçbir parametre (proxies vb.) içermeyen, en yalın httpx istemcisini fonksiyon içinde yaratıyoruz.
        # Böylece Gunicorn başlarken asla takılmıyor ve httpx sürümün ne olursa olsun uyuşmazlık çıkmıyor.
        custom_client = httpx.Client()
        
        client = Groq(
            api_key=API_KEY,
            http_client=custom_client
        )

        # Llama 3 modelimizi tetikliyoruz
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        bot_response = completion.choices[0].message.content
        return jsonify({'cevap': bot_response})

    except Exception as e:
        # Hata durumunda uygulamanın çökmesini engelliyoruz, hatayı ekrana basıyoruz
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
