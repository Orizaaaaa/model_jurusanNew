import pandas as pd

# ================================
# 1. Baca file Excel asli
# ================================
df = pd.read_excel("dataset_action/respon_Siswa.xlsx")

# ================================
# 2. Ambil kolom jawaban + label
# ================================
answers = df.iloc[:, 4:44]   # ambil 40 kolom pertanyaan (q1..q40)
label = df.iloc[:, 2]        # ambil kolom "Jurusan Saat Ini"

# ================================
# 3. Rename kolom jawaban jadi q1..q40
# ================================
answers.columns = [f"q{i}" for i in range(1, len(answers.columns)+1)]

# ================================
# 4. Bersihkan label jurusan
#    Ubah "PPLG (Pengembangan Perangkat Lunak dan Game)" -> "PPLG"
# ================================
label = label.str.replace(r"PPLG \(Pengembangan Perangkat Lunak dan Game\)", "PPLG", regex=True)

# ================================
# 5. Gabungkan jawaban + label
# ================================
dataset_new = pd.concat([answers, label.rename("Label")], axis=1)

# ================================
# 6. Simpan ke CSV
# ================================
dataset_new.to_csv("dataset_new.csv", index=False)

print("✅ dataset_new.csv berhasil dibuat!")
