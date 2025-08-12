import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score, confusion_matrix
from imblearn.over_sampling import RandomOverSampler
import pickle

# Load dataset (menggunakan header)
df = pd.read_csv('dataset.csv')

# Pisahkan fitur dan label
X = df.drop(columns=['Label'])
y = df['Label']

# Pastikan semua fitur numerik
X = X.apply(pd.to_numeric, errors='coerce')

# Tangani nilai NaN jika ada
if X.isnull().values.any():
    print("⚠️ Ditemukan nilai kosong (NaN), akan diisi dengan 0.")
    X = X.fillna(0)

# Cek distribusi label awal
print("📊 Distribusi label awal:")
print(y.value_counts())

# Oversampling agar data seimbang
ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(X, y)

# Cek distribusi label setelah oversampling
print("\n📊 Distribusi label setelah oversampling:")
print(y_resampled.value_counts())

# Stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, stratify=y_resampled, random_state=42
)

# Latih model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Simpan model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Evaluasi model
y_pred = model.predict(X_test)

print("\n✅ Model Evaluation:\n")
print(classification_report(y_test, y_pred))
print("🎯 Accuracy:", f"{accuracy_score(y_test, y_pred):.2%}")
print("🎯 F1 Score:", f"{f1_score(y_test, y_pred, average='weighted'):.2%}")
print("🧮 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
