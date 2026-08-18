import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.form.get('mesaj', '')
        if not user_message:
            return jsonify({'cevap': 'Mesaj boş kanka!'}), 400

        # Render üzerindeki GEMINI_API_KEY değişkenini okur
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return jsonify({'cevap': 'GEMINI_API_KEY Render üzerinde bulunamadı!'}), 500

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )

        return jsonify({'cevap': response.text})

    except Exception as e:
        return jsonify({'cevap': f'Gemini API Hatası: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)