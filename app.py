# app.py

from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model/jurusan_model.pkl')
model = joblib.load(model_path)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    answers = data.get("answers")

    if not answers or len(answers) != 40:
        return jsonify({"error": "Jawaban tidak valid. Harus 40 item."}), 400

    prediction = model.predict([answers])[0]
    return jsonify({"jurusan": prediction})

if __name__ == "__main__":
    app.run(debug=True)
