Kode ini adalah sebuah **API (Application Programming Interface)** yang dibangun menggunakan framework **Flask** (Python) untuk melakukan **prediksi jurusan kuliah berdasarkan jawaban kuesioner psikologis**.

---

### 📌 Fungsi Utama Kode Ini:

1.  **Menyediakan Endpoint Prediksi:** Membuat sebuah layanan web (`/predict`) yang dapat menerima data jawaban dari user (misalnya, dari aplikasi web atau mobile) dan mengembalikan prediksi jurusan yang paling sesuai.
2.  **Load Model Machine Learning:** Menggunakan model *Machine Learning* (yang sudah dilatih sebelumnya dan disimpan dalam file `model.pkl`) untuk melakukan prediksi. Model ini kemungkinan besar adalah klasifikasi (seperti Random Forest, SVM, dll.) yang dilatih untuk memetakan 40 jawaban pertanyaan ke dalam sejumlah jurusan.
3.  **Memberikan Response yang Informative:** Tidak hanya memberikan hasil prediksi, tetapi juga memberikan pesan terkait kualitas jawaban user (misalnya, jika jawaban terlalu netral atau tingkat kepercayaan prediksi rendah).

---

### 🔧 Penjelasan Bagian per Bagian:

#### 1. **Import Library**
   ```python
   from flask import Flask, request, jsonify
   from flask_cors import CORS
   import joblib
   import numpy as np
   ```
   - `Flask`: Framework untuk membuat web server.
   - `request`: Untuk mengakses data JSON yang dikirim oleh client.
   - `jsonify`: Untuk mengubah respons Python menjadi JSON.
   - `CORS`: Untuk mengizinkan request dari domain yang berbeda (penting jika frontend dan backend dihost terpisah).
   - `joblib`: Untuk load model machine learning yang sudah disimpan (`model.pkl`).
   - `numpy`: Untuk operasi matematika dan pengolahan array.

#### 2. **Inisialisasi Aplikasi Flask**
   ```python
   app = Flask(__name__)
   CORS(app)  # Mengizinkan request dari semua domain
   ```

#### 3. **Load Model**
   ```python
   model = joblib.load("models/model.pkl")
   ```
   - Model yang sudah dilatih sebelumnya (misalnya, menggunakan `scikit-learn`) dimuat dari direktori `models/`. File `model.pkl` adalah file yang berisi model serialisasi.

#### 4. **Endpoint Dasar (`/`)**
   ```python
   @app.route("/")
   def index():
       return "✅ API Prediksi Jurusan Aktif"
   ```
   - Endpoint sederhana untuk mengecek apakah API berjalan.

#### 5. **Endpoint Prediksi (`/predict`)**
   ```python
   @app.route("/predict", methods=["POST"])
   def predict():
       data = request.json
       answers = data.get("answers")
   ```
   - Hanya menerima request metode **POST**.
   - Mengambil data JSON dari body request dan mengambil array `answers`.

   **Validasi Input:**
   ```python
   if not answers or len(answers) != 40:
       return jsonify({"error": "Harus menyertakan 40 jawaban"}), 400
   ```
   - Memastikan bahwa input dari user tepat 40 jawaban.

   **Konversi dan Pengecekan Jawaban Netral:**
   ```python
   answers = np.array(answers).reshape(1, -1) # Ubah ke format model (1 sampel, 40 fitur)

   if np.all(answers == 3):
       return jsonify({
           "predicted_major": None,
           "message": "⚠️ Jawaban terlalu netral..."
       })
   ```
   - Mengecek jika user menjawab semua pertanyaan dengan nilai netral (misalnya, selalu memilih 3 dalam skala Likert). Ini akan menghasilkan prediksi yang tidak akurat.

   **Melakukan Prediksi:**
   ```python
   probs = model.predict_proba(answers)[0] # Dapatkan probabilitas untuk setiap kelas
   prediction = model.classes_[np.argmax(probs)] # Ambil kelas dengan probabilitas tertinggi
   confidence = np.max(probs) # Ambil nilai probabilitas tertinggi tersebut
   ```
   - Model tidak hanya memprediksi jurusan, tetapi juga memberikan tingkat kepercayaan (*confidence score*) dari prediksi tersebut.

   **Validasi Tingkat Kepercayaan:**
   ```python
   if confidence < 0.4:
       return jsonify({
           "predicted_major": prediction,
           "confidence": float(confidence),
           "message": "⚠️ Hasil prediksi tidak meyakinkan..."
       })
   ```
   - Jika tingkat kepercayaan model di bawah 40%, API mengirimkan peringatan bahwa hasilnya tidak meyakinkan.

   **Mengembalikan Hasil Akhir:**
   ```python
   return jsonify({
       "predicted_major": prediction,
       "confidence": float(confidence),
       "message": "✅ Prediksi berhasil"
   })
   ```

#### 6. **Menjalankan Server**
   ```python
   if __name__ == "__main__":
       app.run(debug=True)
   ```
   - Menjalankan server Flask dalam mode debug (hanya untuk pengembangan).

---

### 📊 Alur Kerja Secara Keseluruhan:

1.  **Client** (e.g., website) mengirimkan **POST request** ke `https://alamat-api-mu.com/predict` dengan data JSON berformat `{"answers": [1, 4, 2, 3, ..., 5]}` (40 angka).
2.  **Server** (kode Flask ini) menerima request, memvalidasi, dan memprosesnya.
3.  **Model ML** melakukan prediksi berdasarkan 40 jawaban tersebut.
4.  **Server** menganalisis hasil prediksi (probabilitas) dan menentukan respon yang sesuai ke client.
5.  **Client** menerima respons JSON (berisi jurusan, tingkat kepercayaan, dan pesan) dan menampilkannya kepada user.

---

### 🛠️ Contoh Penggunaan:

Sebuah aplikasi **web peminatan jurusan kuliah** akan menggunakan kode ini sebagai backend-nya. User mengisi kuesioner di frontend, frontend mengirimkan jawaban ke API ini, dan kemudian menampilkan jurusan yang diprediksi berdasarkan respons yang diterima.