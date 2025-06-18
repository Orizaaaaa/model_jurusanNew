from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # 🔥 Ini penting untuk mengaktifkan CORS

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return "✅ API Jurusan Siap Digunakan"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    answers = data.get('answers')

    if not answers or len(answers) != 40:
        return jsonify({'error': 'Harus menyertakan 40 jawaban'}), 400

    prediction = model.predict([answers])[0]
    return jsonify({'predicted_major': prediction})

if __name__ == '__main__':
    app.run(debug=True)
