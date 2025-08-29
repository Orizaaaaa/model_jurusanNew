import requests 
import time
from datetime import datetime
import random
import pandas as pd

# ======================================
# KONFIGURASI
# ======================================

form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfN6hfS399wV1gRMiBBI1X8_yaVyLI3i_TJegV2w3oMxVI1tQ/formResponse"

dataset_file = "dataset.csv"
users_file   = "dumy/new_data_siswa.xlsx"

start_user = 1
end_user   = 4   # contoh 4 siswa saja

allowed_dates = [
    datetime(2024, 8, 28),
    datetime(2024, 8, 29),
    datetime(2024, 9, 1)
]

# ======================================
# MAPPING ENTRY GOOGLE FORM
# ======================================

mapping = {
    "q1": "entry.160626020","q2": "entry.1040328376","q3": "entry.1013395402",
    "q4": "entry.782866199","q5": "entry.466204251","q6": "entry.1746078662",
    "q7": "entry.1421791930","q8": "entry.643653765","q9": "entry.2119675585",
    "q10": "entry.433121153","q11": "entry.1360417263","q12": "entry.832968170",
    "q13": "entry.1544775307","q14": "entry.1748347969","q15": "entry.524124343",
    "q16": "entry.1894671203","q17": "entry.518930260","q18": "entry.2133102417",
    "q19": "entry.558757907","q20": "entry.110630600","q21": "entry.616300661",
    "q22": "entry.1449086461","q23": "entry.1831884421","q24": "entry.555135726",
    "q25": "entry.34026277","q26": "entry.1894845699","q27": "entry.1940046232",
    "q28": "entry.1362552560","q29": "entry.1484769489","q30": "entry.1310155753",
    "q31": "entry.436338964","q32": "entry.1555069666","q33": "entry.1975628030",
    "q34": "entry.1551513475","q35": "entry.210622884","q36": "entry.1238101656",
    "q37": "entry.497288204","q38": "entry.928531190","q39": "entry.547538387",
    "q40": "entry.585896102",
}

nama_entry    = "entry.1447702576"
jurusan_entry = "entry.943347128"
cocok_entry   = "entry.1471914611"

# ======================================
# BACA DATASET & USERS
# ======================================

dataset_df = pd.read_csv(dataset_file)
users_df   = pd.read_excel(users_file)

dataset = dataset_df.to_dict(orient="records")
users   = users_df.to_dict(orient="records")

users = users[start_user-1:end_user]

# ======================================
# KELOMPOKKAN DATASET BERDASARKAN JURUSAN
# ======================================

dataset_by_jurusan = {}
for row in dataset:
    jur = row["Label"]
    if jur not in dataset_by_jurusan:
        dataset_by_jurusan[jur] = []
    dataset_by_jurusan[jur].append(row)

# ======================================
# FUNGSI WAKTU UNIK
# ======================================

used_times = {date: set() for date in allowed_dates}

def generate_unique_time(date):
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

for i, user in enumerate(users):
    jurusan_user = str(user["Jurusan"]).strip()

    if jurusan_user not in dataset_by_jurusan or len(dataset_by_jurusan[jurusan_user]) == 0:
        print(f"❌ Tidak ada dataset tersisa untuk jurusan {jurusan_user} (user: {user['Nama Lengkap']})")
        continue

    # Ambil dataset sesuai jurusan
    row = dataset_by_jurusan[jurusan_user].pop(0)

    if row["Label"] == "PPLG":
        jurusan_form = "PPLG (Pengembangan Perangkat Lunak dan Game)"
    else:
        jurusan_form = row["Label"]

    submission_time = timestamps[i]
    timestamp_str = submission_time.strftime("%Y-%m-%d %H:%M:%S")

    # Data form
    form_data = {
        nama_entry: user["Nama Lengkap"],
        jurusan_entry: jurusan_form,
        cocok_entry: user["Apakah Anda merasa cocok di jurusan ini ?"]
    }

    for q, entry_id in mapping.items():
        form_data[entry_id] = str(row[q])

    # Gabungkan dataset jadi string untuk ditampilkan
    dataset_values = [str(row[f"q{n}"]) for n in range(1, 41)]
    dataset_values.append(row["Label"])
    dataset_str = ",".join(dataset_values)

    # Kirim ke Google Form
    response = requests.post(form_url, data=form_data)

    delay = 0.5
    time.sleep(delay)

    print(f"\nMengirim data untuk: {user['Nama Lengkap']}")
    print(f"Jurusan: {jurusan_form}")
    print(f"Dataset dipakai: {dataset_str}")
    print(f"Waktu submission: {timestamp_str}")
    print("Status code:", response.status_code)
    if response.status_code == 200:
        print("✅ Berhasil submit form!")
    else:
        print("❌ Gagal submit, status:", response.status_code)
    print("-" * 60)

print("\n✅ Semua data telah dikirim!")
