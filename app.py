from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load model
model = joblib.load("models/model.pkl")

@app.route("/")
def index():
    return "✅ API Prediksi Jurusan Aktif"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    answers = data.get("answers")

    if not answers or len(answers) != 40:
        return jsonify({"error": "Harus menyertakan 40 jawaban"}), 400

    # Konversi ke numpy
    answers = np.array(answers).reshape(1, -1)

    # Cek apakah semua jawaban netral (misal 3)
    if np.all(answers == 3):
        return jsonify({
            "predicted_major": None,
            "message": "⚠️ Jawaban terlalu netral, mohon isi lebih bervariasi agar hasil akurat."
        })

    # Prediksi + Probabilitas
    probs = model.predict_proba(answers)[0]
    prediction = model.classes_[np.argmax(probs)]
    confidence = np.max(probs)

    # Jika confidence rendah, kasih warning
    if confidence < 0.4:
        return jsonify({
            "predicted_major": prediction,
            "confidence": float(confidence),
            "message": "⚠️ Hasil prediksi tidak meyakinkan, mohon isi lebih detail."
        })

    return jsonify({
        "predicted_major": prediction,
        "confidence": float(confidence),
        "message": "✅ Prediksi berhasil"
    })

if __name__ == "__main__":
    app.run(debug=True)
