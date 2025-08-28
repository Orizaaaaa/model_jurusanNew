import requests
import time
from datetime import datetime, timedelta
import random

# URL untuk submit (bukan viewform tapi formResponse)
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfN6hfS399wV1gRMiBBI1X8_yaVyLI3i_TJegV2w3oMxVI1tQ/formResponse"

# Dataset lengkap (6 baris data)
dataset = [
    [1,1,2,4,3,5,4,5,1,3,5,1,5,4,2,3,4,5,5,1,5,1,5,4,5,5,3,2,5,5,2,1,4,2,4,3,4,1,4,5,"Akuntansi"],
    [4,3,2,5,1,5,3,2,3,5,5,3,5,4,2,4,2,3,3,1,2,3,1,5,1,3,5,3,2,1,2,2,4,4,4,1,4,3,4,4,"PPLG"],
    [1,3,1,5,5,3,3,4,4,3,5,4,3,2,2,1,3,3,1,4,4,1,3,4,2,2,4,2,4,3,1,1,5,1,3,1,4,2,2,1,"PPLG"],
    [3,4,1,1,5,3,4,4,5,2,4,1,3,2,2,3,5,2,2,5,4,5,5,4,5,5,2,5,5,5,3,1,2,1,1,2,4,5,2,2,"PPLG"],
    [5,2,2,1,1,2,3,4,2,5,1,3,1,1,2,4,5,1,5,4,2,3,4,5,5,3,3,2,1,5,2,4,2,4,1,2,3,1,1,4,"Perhotelan"],
    [5,2,1,1,2,3,1,1,2,4,4,4,5,1,2,4,3,1,5,5,4,2,2,4,2,1,3,1,3,2,3,5,4,3,4,5,5,4,3,3,"PPLG"]
]

# Data user (hanya nama dan apakah cocok)
users = [
    {"Nama Lengkap": "Rafael abizar", "Apakah cocok?": "Iya"},
]

# Mapping entry ID untuk pertanyaan skala 1-5
entry_ids = [
    "entry.160626020", "entry.1040328376", "entry.1013395402", "entry.782866199",
    "entry.466204251", "entry.1746078662", "entry.1421791930", "entry.643653765",
    "entry.2119675585", "entry.433121153", "entry.1360417263", "entry.832968170",
    "entry.1544775307", "entry.1748347969", "entry.524124343", "entry.1894671203",
    "entry.518930260", "entry.2133102417", "entry.558757907", "entry.110630600",
    "entry.616300661", "entry.1449086461", "entry.1831884421", "entry.555135726",
    "entry.34026277", "entry.1894845699", "entry.1940046232", "entry.1362552560",
    "entry.1484769489", "entry.1310155753", "entry.436338964", "entry.1555069666",
    "entry.1975628030", "entry.1551513475", "entry.210622884", "entry.1238101656",
    "entry.497288204", "entry.928531190", "entry.547538387", "entry.585896102"
]

# Daftar tanggal yang diizinkan: 28 Agustus, 29 Agustus, 1 September 2024
allowed_dates = [
    datetime(2024, 8, 28),
    datetime(2024, 8, 29), 
    datetime(2024, 9, 1)
]

# Generate jam yang unik untuk setiap tanggal
used_times = {date: set() for date in allowed_dates}

def generate_unique_time(date):
    """Generate waktu yang unik untuk tanggal tertentu (tidak lebih dari jam 3)"""
    available_hours = list(range(0, 4))  # Jam 0, 1, 2, 3
    available_minutes = list(range(0, 60))
    available_seconds = list(range(0, 60))
    
    # Coba maksimal 100 kali untuk mendapatkan waktu yang unik
    for _ in range(100):
        hour = random.choice(available_hours)
        minute = random.choice(available_minutes)
        second = random.choice(available_seconds)
        
        time_key = (hour, minute, second)
        
        if time_key not in used_times[date]:
            used_times[date].add(time_key)
            return datetime(date.year, date.month, date.day, hour, minute, second)
    
    # Jika tidak bisa dapat waktu unik, gunakan waktu default
    return datetime(date.year, date.month, date.day, 0, 0, 0)

# Generate timestamp unik untuk setiap user
timestamps = []
for i in range(len(users)):
    # Pilih tanggal secara acak dari allowed_dates
    date = random.choice(allowed_dates)
    timestamp = generate_unique_time(date)
    timestamps.append(timestamp)

# Kirim data untuk setiap user
for i, user in enumerate(users):
    # Ambil data dari dataset secara berurutan
    data_index = i % len(dataset)
    jawaban_skala = dataset[data_index][:40]
    jurusan_dataset = dataset[data_index][40]
    
    # Format khusus untuk jurusan PPLG
    if jurusan_dataset == "PPLG":
        jurusan_form = "PPLG (Pengembangan Perangkat Lunak dan Game)"
    else:
        jurusan_form = jurusan_dataset
    
    # Ambil timestamp yang sudah digenerate
    submission_time = timestamps[i]
    timestamp_str = submission_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Siapkan data untuk form
    form_data = {
        "entry.1447702576": user["Nama Lengkap"],      # Nama Lengkap
        "entry.943347128": jurusan_form,               # Jurusan Saat Ini
        "entry.1471914611": user["Apakah cocok?"],     # Apakah cocok?
    }
    
    # Tambahkan timestamp jika ada field untuknya
    # form_data["entry.timestamp"] = timestamp_str
    
    # Tambahkan jawaban untuk pertanyaan skala 1-5
    for j in range(40):
        if j < len(jawaban_skala) and j < len(entry_ids):
            form_data[entry_ids[j]] = str(jawaban_skala[j])
    
    # Kirim POST request ke form
    response = requests.post(form_url, data=form_data)
    
    # Delay acak antara 3-8 detik antara setiap submission
    delay = random.uniform(3, 8)
    time.sleep(delay)
    
    print(f"\nMengirim data untuk: {user['Nama Lengkap']}")
    print(f"Jurusan: {jurusan_form}")
    print(f"Waktu submission: {timestamp_str}")
    print(f"Tanggal: {submission_time.strftime('%d/%m/%Y')}")
    print(f"Jam: {submission_time.strftime('%H:%M:%S')}")
    print(f"Delay berikutnya: {delay:.1f} detik")
    print(f"Menggunakan dataset baris: {data_index + 1}")
    print("Status code:", response.status_code)
    if response.status_code == 200:
        print("✅ Berhasil submit form!")
    else:
        print("❌ Gagal submit, status:", response.status_code)
    print("-" * 60)

print("\n✅ Semua data telah dikirim!")
print("\n📊 Summary Waktu:")
for i, timestamp in enumerate(timestamps):
    print(f"{i+1}. {timestamp.strftime('%d/%m/%Y %H:%M:%S')} - {users[i]['Nama Lengkap']}")