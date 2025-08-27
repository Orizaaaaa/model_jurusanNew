import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, f1_score, confusion_matrix
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline
import os

# === Load dataset ===
df = pd.read_csv("dataset.csv")

# Pisahkan fitur dan label
X = df.drop(columns=["Label"])
y = df["Label"]

# Pastikan semua fitur numerik
X = X.apply(pd.to_numeric, errors="coerce")

# Tangani nilai NaN
if X.isnull().values.any():
    print("⚠️ Terdapat nilai kosong (NaN), diisi dengan 0.")
    X = X.fillna(0)

# Distribusi awal
print("📊 Distribusi Label Awal:")
print(y.value_counts())

# === Pipeline (Oversampling + RandomForest) ===
pipeline = Pipeline([
    ("oversample", RandomOverSampler(random_state=42)),
    ("clf", RandomForestClassifier(
        n_estimators=200,       # lebih besar untuk stabilitas
        max_depth=None,         # biarkan RF cari kedalaman optimal
        min_samples_split=2,
        random_state=42,
        n_jobs=-1               # gunakan semua core CPU
    ))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train model
pipeline.fit(X_train, y_train)

# === Save model ===
os.makedirs("models", exist_ok=True)
joblib.dump(pipeline, "models/model.pkl")
print("\n💾 Model berhasil disimpan di models/model.pkl")

# === Evaluasi ===
y_pred = pipeline.predict(X_test)

print("\n✅ Model Evaluation:\n")
print(classification_report(y_test, y_pred))
print("🎯 Accuracy:", f"{accuracy_score(y_test, y_pred):.2%}")
print("🎯 F1 Score:", f"{f1_score(y_test, y_pred, average='weighted'):.2%}")
print("🧮 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# === Cross Validation ===
cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")
print("\n📊 Cross Validation Accuracy:", cv_scores)
print("📊 Mean CV Accuracy:", f"{cv_scores.mean():.2%}")

# === Feature Importance (dari RandomForest) ===
clf = pipeline.named_steps["clf"]
importances = clf.feature_importances_
features = X.columns

sorted_idx = np.argsort(importances)[::-1][:10]  # top 10 fitur
print("\n🌟 Top 10 Pertanyaan Paling Berpengaruh:")
for i in sorted_idx:
    print(f"{features[i]}: {importances[i]:.4f}")
