# model/train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train():
    dataset_path = os.path.join(os.path.dirname(__file__), '../dataset.csv')

    print("📥 Membaca dataset...")
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print("❌ Gagal: dataset.csv tidak ditemukan.")
        return

    print(f"✅ Dataset ditemukan. Jumlah data: {df.shape[0]} baris.")

    if not all(f'q{i+1}' in df.columns for i in range(40)) or 'Label' not in df.columns:
        raise ValueError("❌ Kolom tidak lengkap. Harus ada q1 sampai q40 dan kolom 'Label'.")

    X = df[[f'q{i+1}' for i in range(40)]]
    y = df['Label']

    print("🔧 Melatih model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    model_path = os.path.join(os.path.dirname(__file__), 'jurusan_model.pkl')
    joblib.dump(model, model_path)

    print("✅ Model disimpan di:", model_path)

if __name__ == "__main__":
    train()
