import os
import io
from tensorflow import keras
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify

# Load model .h5 from Cloud Storage or local (ensure you upload model to Cloud Storage or include it in the container)
model = keras.models.load_model("model.h5")

# Daftar label sesuai yang Anda berikan
labels = ['Motif Barong From Bali', 'Motif Merak From Bali', 'Motif Ondel Ondel From Jakarta', 'Motif Tumpal From Jakarta', 'Motif Megamendung From Jawa Barat', 'Motif Asem Arang From Jawa Tengah', 'Motif Asem Sinom From Jawa Tengah', 'Motif Asem Warak From Jawa Tengah', 'Motif Blekok From Jawa Tengah', 'Motif Blekok Warak From Jawa Tengah', 'Motif Cipratan From Jawa Tengah', 'Motif Gambang Semarangan From Jawa Tengah', 'Motif Ikan Kerang From Jawa Tengah', 'Motif Jagung Lombok From Jawa Tengah', 'Motif Jambu Belimbing From Jawa Tengah', 'Motif Jambu Citra From Jawa Tengah', 'Motif Jlamprang From Jawa Tengah', 'Motif Kembang Sepatu From Jawa Tengah', 'Motif Laut From Jawa Tengah', 'Motif Lurik Semangka From Jawa Tengah', 'Motif Masjid Agung Demak From Jawa Tengah', 'Motif Naga From Jawa Tengah', 'Motif Parang Kusumo From Jawa Tengah', 'Motif Parang Slobog From Jawa Tengah', 'Motif Semarangan From Jawa Tengah', 'Motif Sidoluhur From Jawa Tengah', 'Motif Tebu Bambu From Jawa Tengah', 'Motif Tembakau From Jawa Tengah', 'Motif Truntum From Jawa Tengah', 'Motif Tugu Muda From Jawa Tengah', 'Motif Warak Beras Utah From Jawa Tengah', 'Motif Yuyu From Jawa Tengah', 'Motif Gentongan From Jawa Timur', 'Motif Pring From Jawa Timur', 'Motif Insang From Kalimantan Barat', 'Motif Dayak From Kalimantan', 'Motif Bledheg From Lampung', 'Motif Gajah From Lampung', 'Motif Kacang Hijau From Lampung', 'Motif Pala From Maluku', 'Motif Lumbung From NTB', 'Motif Asmat From Papua', 'Motif Cendrawasih From Papua', 'Motif Tifa From Papua', 'Motif Lontara From Sulawesi Selatan', 'Motif Rumah Minang From Sumatera Barat', 'Motif Boraspati From Sumatera Utara', 'Motif Pintu Aceh From Aceh', 'Motif Kawung From Yogyakarta', 'Motif Parang Curigo From Yogyakarta', 'Motif Parang Rusak From Yogyakarta', 'Motif Parang Tuding From Yogyakarta']

app = Flask(__name__)

def predict_label(img):
    i = np.asarray(img) / 255.0
    i = i.reshape(1, 224, 224, 3)
    pred = model.predict(i)
    result = labels[np.argmax(pred)]
    return result

@app.route("/predict", methods=["POST"])
def index():
    # Memastikan file diupload
    file = request.files.get('file')
    if file is None or file.filename == "":
        return jsonify({"error": "No file uploaded"}), 400

    # Membaca dan memproses gambar
    image_bytes = file.read()
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((224, 224), Image.NEAREST)
    pred_label = predict_label(img)

    return jsonify({"predicted_label": pred_label})

if __name__ == "__main__":
    # Menggunakan Gunicorn pada Cloud Run, pastikan port sesuai dengan Cloud Run (default: 8080)
    app.run(debug=True, host="0.0.0.0", port=8080)
