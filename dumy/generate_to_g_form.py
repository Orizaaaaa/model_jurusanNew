import requests
import time
from datetime import datetime
import random
import pandas as pd

# ======================================
# KONFIGURASI
# ======================================

# URL submit Google Form (formResponse, bukan viewform)
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfN6hfS399wV1gRMiBBI1X8_yaVyLI3i_TJegV2w3oMxVI1tQ/formResponse"

# File dataset & user
dataset_file = "dataset.csv"
users_file   = "dumy/data_siswa.xlsx"

# Atur range user yang mau dikirim (misal user ke 1–5)
start_user = 1
end_user   = 5

# Daftar tanggal yang diizinkan
allowed_dates = [
    datetime(2024, 8, 28),
    datetime(2024, 8, 29),
    datetime(2024, 9, 1)
]

# ======================================
# MAPPING DATASET KE ENTRY GOOGLE FORM
# ======================================

mapping = {
    "q1": "entry.160626020",
    "q2": "entry.1040328376",
    "q3": "entry.1013395402",
    "q4": "entry.782866199",
    "q5": "entry.466204251",
    "q6": "entry.1746078662",
    "q7": "entry.1421791930",
    "q8": "entry.643653765",
    "q9": "entry.2119675585",
    "q10": "entry.433121153",
    "q11": "entry.1360417263",
    "q12": "entry.832968170",
    "q13": "entry.1544775307",
    "q14": "entry.1748347969",
    "q15": "entry.524124343",
    "q16": "entry.1894671203",
    "q17": "entry.518930260",
    "q18": "entry.2133102417",
    "q19": "entry.558757907",
    "q20": "entry.110630600",
    "q21": "entry.616300661",
    "q22": "entry.1449086461",
    "q23": "entry.1831884421",
    "q24": "entry.555135726",
    "q25": "entry.34026277",
    "q26": "entry.1894845699",
    "q27": "entry.1940046232",
    "q28": "entry.1362552560",
    "q29": "entry.1484769489",
    "q30": "entry.1310155753",
    "q31": "entry.436338964",
    "q32": "entry.1555069666",
    "q33": "entry.1975628030",
    "q34": "entry.1551513475",
    "q35": "entry.210622884",
    "q36": "entry.1238101656",
    "q37": "entry.497288204",
    "q38": "entry.928531190",
    "q39": "entry.547538387",
    "q40": "entry.585896102",
}

# Entry untuk data tambahan
nama_entry   = "entry.1447702576"
jurusan_entry = "entry.943347128"
cocok_entry   = "entry.1471914611"

# ======================================
# BACA DATASET & USERS
# ======================================

dataset_df = pd.read_csv(dataset_file)
users_df = pd.read_excel(users_file)

dataset = dataset_df.to_dict(orient="records")
users = users_df.to_dict(orient="records")

# Ambil range user sesuai setting
users = users[start_user-1:end_user]
dataset = dataset[start_user-1:end_user]

# ======================================
# FUNGSI WAKTU UNIK
# ======================================

used_times = {date: set() for date in allowed_dates}

def generate_unique_time(date):
    """Generate waktu unik untuk tanggal tertentu (tidak lebih dari jam 3 pagi)."""
    for _ in range(100):
        hour = random.choice(range(0, 4))
        minute = random.choice(range(0, 60))
        second = random.choice(range(0, 60))
        time_key = (hour, minute, second)
        if time_key not in used_times[date]:
            used_times[date].add(time_key)
            return datetime(date.year, date.month, date.day, hour, minute, second)
    return datetime(date.year, date.month, date.day, 0, 0, 0)

# ======================================
# GENERATE TIMESTAMP
# ======================================

timestamps = []
for _ in range(len(users)):
    date = random.choice(allowed_dates)
    timestamps.append(generate_unique_time(date))

# ======================================
# KIRIM DATA KE GOOGLE FORM
# ======================================

for i, (user, row) in enumerate(zip(users, dataset)):
    jurusan_dataset = row["Label"]
    if jurusan_dataset == "PPLG":
        jurusan_form = "PPLG (Pengembangan Perangkat Lunak dan Game)"
    else:
        jurusan_form = jurusan_dataset

    submission_time = timestamps[i]
    timestamp_str = submission_time.strftime("%Y-%m-%d %H:%M:%S")

    # Data form
    form_data = {
        nama_entry: user["Nama Lengkap"],
        jurusan_entry: jurusan_form,
        cocok_entry: user["Apakah Anda merasa cocok di jurusan ini ?"]
    }

    # Isi q1–q40 sesuai mapping
    for q, entry_id in mapping.items():
        form_data[entry_id] = str(row[q])

    # Kirim ke Google Form
    response = requests.post(form_url, data=form_data)

    delay = 0.5  # delay fixed 0.5 detik
    time.sleep(delay)

    print(f"\nMengirim data untuk: {user['Nama Lengkap']}")
    print(f"Jurusan: {jurusan_form}")
    print(f"Waktu submission: {timestamp_str}")
    print(f"Delay berikutnya: {delay:.1f} detik")
    print("Status code:", response.status_code)
    if response.status_code == 200:
        print("✅ Berhasil submit form!")
    else:
        print("❌ Gagal submit, status:", response.status_code)
    print("-" * 60)

print("\n✅ Semua data telah dikirim!")
