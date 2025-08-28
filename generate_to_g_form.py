import requests

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
    {"Nama Lengkap": "Rafa Pratama ", "Apakah cocok?": "Iya"},
    {"Nama Lengkap": "Arya Handayani", "Apakah cocok?": "Iya"},
    {"Nama Lengkap": "Daffa Ananta", "Apakah cocok?": "Tidak"},
    {"Nama Lengkap": "Anya Anggraini", "Apakah cocok?": "Iya"},
    {"Nama Lengkap": "Cleo Pertiwi", "Apakah cocok?": "Iya"},
    {"Nama Lengkap": "Farel Saputra", "Apakah cocok?": "Iya"},
    {"Nama Lengkap": "Salma Pertiwi", "Apakah cocok?": "Iya"}
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

# Kirim data untuk setiap user
for i, user in enumerate(users):
    # Ambil data dari dataset secara berurutan
    data_index = i % len(dataset)  # Menggunakan modulo untuk mengulang jika dataset habis
    jawaban_skala = dataset[data_index][:40]  # Ambil 40 nilai pertama (q1 sampai q40)
    jurusan_dataset = dataset[data_index][40]  # Ambil label jurusan dari dataset
    
    # Format khusus untuk jurusan PPLG
    if jurusan_dataset == "PPLG":
        jurusan_form = "PPLG (Pengembangan Perangkat Lunak dan Game)"
    else:
        jurusan_form = jurusan_dataset
    
    # Siapkan data untuk form
    form_data = {
        "entry.1447702576": user["Nama Lengkap"],      # Nama Lengkap
        "entry.943347128": jurusan_form,               # Jurusan Saat Ini (dari dataset)
        "entry.1471914611": user["Apakah cocok?"],     # Apakah cocok?
    }
    
    # Tambahkan jawaban untuk pertanyaan skala 1-5
    for j in range(40):
        if j < len(jawaban_skala) and j < len(entry_ids):
            form_data[entry_ids[j]] = str(jawaban_skala[j])
    
    # Kirim POST request ke form
    response = requests.post(form_url, data=form_data)
    
    print(f"\nMengirim data untuk: {user['Nama Lengkap']}")
    print(f"Jurusan: {jurusan_form}")
    print(f"Menggunakan dataset baris: {data_index + 1}")
    print("Status code:", response.status_code)
    if response.status_code == 200:
        print("✅ Berhasil submit form!")
    else:
        print("❌ Gagal submit, status:", response.status_code)
    print("-" * 50)

print("\n✅ Semua data telah dikirim!")