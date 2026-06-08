from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# ==========================================
# GEMINI API AYARLARI
# ==========================================
# Kanka, buradaki "KENDI_API_ANAHTARIN" yazan yere Google AI Studio'dan aldığın anahtarı yapıştır.
# Sunum günü kota sorunu yaşamamak için buraya yedek/taze bir anahtar koyabilirsin.
API_KEY = "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"
genai.configure(api_key=API_KEY)

# Gemini 2.5 Flash modelimizi tanımlıyoruz
model = genai.GenerativeModel('gemini-2.5-flash')


# ==========================================
# ANA SAYFA ROTASI
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')


# ==========================================
# AKILLI SOHBET VE FOTOĞRAF ANALİZ ROTASI
# ==========================================
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # 1. Frontend'den gelen form verilerini yakalıyoruz
        kullanici_mesaji = request.form.get('mesaj')
        gelen_foto = request.files.get('fotoğraf')

        # Eğer hem mesaj hem fotoğraf boşsa işlemi durdur
        if not kullanici_mesaji and not gelen_foto:
            return jsonify({'cevap': 'Kanka bomboş mesaj gönderdin, bir şeyler yazsana!'})

        # 2. Gemini'ye gönderilecek içerik listesini hazırlıyoruz
        icerik_listesi = []

        # Eğer kullanıcı fotoğraf yüklediyse, bunu Gemini'nin okuyabileceği bayt formatına çeviriyoruz
        if gelen_foto:
            foto_verisi = gelen_foto.read()
            foto_mime = gelen_foto.content_type  # image/png, image/jpeg vb.

            # Çoklu modlu veri yapısını listeye ekle
            icerik_listesi.append({
                "mime_type": foto_mime,
                "data": foto_verisi
            })

        # Eğer metin mesajı varsa listeye ekle
        if kullanici_mesaji:
            icerik_listesi.append(kullanici_mesaji)

        # 3. Gemini API'ye içeriği gönderip yanıtı bekliyoruz
        response = model.generate_content(icerik_listesi)
        yapay_zeka_cevabi = response.text

        # Başarılı cevabı frontend'e JSON olarak fırlat
        return jsonify({'cevap': yapay_zeka_cevabi})

    except Exception as e:
        hata_mesaji = str(e)
        print("Hata Raporu:", hata_mesaji)  # Terminale hatayı basar

        # 4. AKILLI KOTA KORUMASI (429 RESOURCE EXHAUSTED YÖNETİMİ)
        if "429" in hata_mesaji or "RESOURCE_EXHAUSTED" in hata_mesaji:
            kurtarma_cevabi = (
                "Kanka şu an Kulu MTAL Yapay Zekâ Laboratuvarı aşırı yoğunluktan dolayı kota sınırına ulaştı! 🚀 "
                "Sunum için günlük ücretsiz istek limitimiz (20 mesaj) dolmuş. "
                "Lütfen app.py kodundaki API anahtarını taze bir hesapla değiştir kanka."
            )
            return jsonify({'cevap': kurtarma_cevabi})

        # Diğer genel hatalar için kurtarma mesajı
        return jsonify({'cevap': f'Sistemde bir dalgalanma oldu kanka. Hata detayı: {hata_mesaji}'})


# ==========================================
# PROJENİN ÇALIŞTIRILMA ALANI
# ==========================================
if __name__ == '__main__':
    # SİSTEM: Yeni nesil v1 bağlantısı başarılı!
    print("*" * 40)
    print("SİSTEM: Kulu MTAL Yapay Zekâ Asistanı Başlatılıyor...")
    print("Görsel yükleme ve Oval tasarım entegrasyonu aktif!")
    print("*" * 40)
    app.run(debug=True, port=5000)
