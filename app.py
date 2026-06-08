import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# 🔐 Çalışan Gerçek Groq API Anahtarın
API_KEY = "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"

# Groq istemcisini ayağa kaldırıyoruz
client = Groq(api_key=API_KEY)

@app.route('/')
def index():
    # Templates/index.html dosyasını ekrana basar
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # HTML arayüzünden gelen metin mesajını alıyoruz
        user_message = request.form.get('message', '')
        
        # HTML arayüzünden gelen bir fotoğraf var mı diye kontrol ediyoruz
        uploaded_file = request.files.get('image')

        if not user_message and not uploaded_file:
            return jsonify({'error': 'Boş mesaj gönderemezsin kanka.'}), 400

        # Eğer sadece düz metin mesajı geldiyse bu blok çalışır
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        bot_response = completion.choices[0].message.content
        return jsonify({'response': bot_response})

    except Exception as e:
        # Kodun çökmesini engeller, hatayı güvenli bir şekilde arayüze basar
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
