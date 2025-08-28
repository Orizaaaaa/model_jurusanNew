import requests
import random

# URL untuk submit (bukan viewform tapi formResponse)
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfN6hfS399wV1gRMiBBI1X8_yaVyLI3i_TJegV2w3oMxVI1tQ/formResponse"

# Data dummy
import random

form_data = {
    # ✅ Data spesifik
    "entry.1447702576": "Oriza Sativa",   # Nama Lengkap
    "entry.943347128": "Akuntansi",       # Jurusan Saat Ini
    "entry.1471914611": "Iya",            # Apakah cocok?

    # ✅ 38 field skala 1–5 (random)
    "entry.160626020": str(random.randint(1, 5)),
    "entry.1040328376": str(random.randint(1, 5)),
    "entry.1013395402": str(random.randint(1, 5)),
    "entry.782866199": str(random.randint(1, 5)),
    "entry.466204251": str(random.randint(1, 5)),
    "entry.1746078662": str(random.randint(1, 5)),
    "entry.1421791930": str(random.randint(1, 5)),
    "entry.643653765": str(random.randint(1, 5)),
    "entry.2119675585": str(random.randint(1, 5)),
    "entry.433121153": str(random.randint(1, 5)),
    "entry.1360417263": str(random.randint(1, 5)),
    "entry.832968170": str(random.randint(1, 5)),
    "entry.1544775307": str(random.randint(1, 5)),
    "entry.1748347969": str(random.randint(1, 5)),
    "entry.524124343": str(random.randint(1, 5)),
    "entry.1894671203": str(random.randint(1, 5)),
    "entry.518930260": str(random.randint(1, 5)),
    "entry.2133102417": str(random.randint(1, 5)),
    "entry.558757907": str(random.randint(1, 5)),
    "entry.110630600": str(random.randint(1, 5)),
    "entry.616300661": str(random.randint(1, 5)),
    "entry.1449086461": str(random.randint(1, 5)),
    "entry.1831884421": str(random.randint(1, 5)),
    # --- Field tambahan yang belum ada di kode sebelumnya ---
    "entry.555135726": str(random.randint(1, 5)),
    "entry.34026277": str(random.randint(1, 5)),
    "entry.1894845699": str(random.randint(1, 5)),
    "entry.1940046232": str(random.randint(1, 5)),
    "entry.1362552560": str(random.randint(1, 5)),
    "entry.1484769489": str(random.randint(1, 5)),
    "entry.1310155753": str(random.randint(1, 5)),
    "entry.436338964": str(random.randint(1, 5)),
    "entry.1555069666": str(random.randint(1, 5)),
    "entry.1975628030": str(random.randint(1, 5)),
    "entry.1551513475": str(random.randint(1, 5)),
    "entry.210622884": str(random.randint(1, 5)),
    "entry.1238101656": str(random.randint(1, 5)),
    "entry.497288204": str(random.randint(1, 5)),
    "entry.928531190": str(random.randint(1, 5)),
    "entry.547538387": str(random.randint(1, 5)),
    "entry.585896102": str(random.randint(1, 5)),
}
# Kirim POST request ke form
response = requests.post(form_url, data=form_data)

print("Status code:", response.status_code)
if response.status_code == 200:
    print("✅ Berhasil submit form!")
else:
    print("❌ Gagal submit, status:", response.status_code)
