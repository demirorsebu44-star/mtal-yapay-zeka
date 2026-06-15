import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Kendi API anahtarını kullanmaya devam et
API_KEY = "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" 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Mesajı al
        user_message = request.form.get('mesaj', '')
        if not user_message:
            return jsonify({'error': 'Mesaj boş kanka!'}), 400

        client = Groq(api_key=API_KEY)

        # Llama 3.1 ile cevap al
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7,
            max_tokens=1024
        )
        
        bot_response = completion.choices[0].message.content
        return jsonify({'cevap': bot_response})

    except Exception as e:
        # Hata durumunda bunu döndür, böylece undefined görmezsin
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
