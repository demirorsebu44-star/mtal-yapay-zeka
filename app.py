import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# 🔐 Yeni Groq API Anahtarın (Sorunsuz Çalışan Standart API Key Formatı)
API_KEY = "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"

# Groq İstemcisini doğrudan bu anahtarla tetikliyoruz
client = Groq(api_key=API_KEY)

@app.route('/')
def index():
    # Templates klasörünün altındaki index.html dosyasını ekrana basar
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Arayüzden (index.html) gelen mesajı yakalıyoruz
        user_message = request.form.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Mesaj boş olamaz kanka.'}), 400

        # En kararlı ve hızlı çalışan Llama 3 modelini çağırıyoruz
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        
        # Yapay zekanın ürettiği cevabı ayıklıyoruz
        bot_response = completion.choices[0].message.content
        
        # Cevabı arayüze JSON formatında güvenle geri gönderiyoruz
        return jsonify({'response': bot_response})

    except Exception as e:
        # Herhangi bir hata oluşursa sunucunun çökmesini engeller, hatayı arayüze yansıtır
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Lokal testler için debug modunu aktif ediyoruz
    app.run(debug=True)
