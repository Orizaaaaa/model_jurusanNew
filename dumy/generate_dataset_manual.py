import pandas as pd
import random

def generate_dummy_dataset(jumlah_data=300):
    data = []
    for _ in range(jumlah_data):
        jawaban = [random.randint(1, 5) for _ in range(40)]

        # Aturan sederhana untuk label:
        pplg_score = sum([jawaban[i] for i in [1, 4, 8, 9, 10, 13, 14, 18, 27, 30, 33, 37]])
        akuntansi_score = sum([jawaban[i] for i in [2, 3, 6, 9, 12, 16, 21, 22, 25, 29, 35, 38]])
        perhotelan_score = sum([jawaban[i] for i in [0, 5, 7, 11, 15, 17, 19, 23, 24, 26, 32, 39]])

        if pplg_score >= akuntansi_score and pplg_score >= perhotelan_score:
            label = 'PPLG'
        elif akuntansi_score >= perhotelan_score:
            label = 'Akuntansi'
        else:
            label = 'Perhotelan'

        data.append(jawaban + [label])

    columns = [f'q{i+1}' for i in range(40)] + ['Label']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('dataset.csv', index=False)
    print("✅ Dataset berhasil dibuat!")

generate_dummy_dataset()
