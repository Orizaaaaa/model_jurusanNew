# utils/generate_dataset.py

import csv
import random
import os

# Pertanyaan sebanyak 40
questions = [f"q{i+1}" for i in range(40)]

# Fungsi untuk menggenerate 1 jawaban (nilai 1-5)
def generate_answers():
    return [random.randint(1, 5) for _ in range(40)]

# Fungsi untuk menentukan label (jurusan) berdasarkan skor heuristik
def determine_label(answers):
    score_pplg = sum(answers[i] for i in [1, 4, 5, 9, 11, 15, 19, 25, 29, 32, 35, 38])
    score_perhotelan = sum(answers[i] for i in [0, 7, 14, 16, 18, 21, 24, 28, 31, 34, 37, 39])
    score_akuntansi = sum(answers[i] for i in [2, 3, 6, 10, 13, 17, 20, 23, 27, 30, 36, 38])

    if score_pplg >= score_perhotelan and score_pplg >= score_akuntansi:
        return "PPLG"
    elif score_perhotelan >= score_pplg and score_perhotelan >= score_akuntansi:
        return "Perhotelan"
    else:
        return "Akuntansi"

# Simpan file ke root sebagai dataset.csv
output_path = os.path.join(os.path.dirname(__file__), '../dataset.csv')

with open(output_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(questions + ["Label"])  # header

    for _ in range(1000):
        answers = generate_answers()
        label = determine_label(answers)
        writer.writerow(answers + [label])

print("✅ Dataset berhasil dibuat di:", output_path)
