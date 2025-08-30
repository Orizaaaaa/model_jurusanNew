import pandas as pd

# ================================
# 1. Baca file Excel asli
# Ganti "data.xlsx" dengan nama file excel kamu
# ================================
df = pd.read_excel("dumy/dataset_from.xlsx")

# ================================
# 2. Tentukan kolom mana saja yang berisi jawaban
# Struktur kolom dari excel kamu:
# 0 = Timestamp
# 1 = Nama Lengkap
# 2 = Jurusan Saat Ini
# 3 = Apakah Anda merasa cocok di jurusan ini?
# 4..43 = Jawaban angka (40 pertanyaan)
# ================================
answers = df.iloc[:, 4:44]   # ambil 40 kolom pertanyaan (q1..q40)
label = df.iloc[:, 2]        # ambil kolom "Jurusan Saat Ini"

# ================================
# 3. Rename kolom jawaban jadi q1..q40
# ================================
answers.columns = [f"q{i}" for i in range(1, len(answers.columns)+1)]

# ================================
# 4. Gabungkan jawaban + label
# ================================
dataset_new = pd.concat([answers, label.rename("Label")], axis=1)

# ================================
# 5. Simpan ke CSV
# ================================
dataset_new.to_csv("dataset_new.csv", index=False)

print("✅ dataset_new.csv berhasil dibuat!")
