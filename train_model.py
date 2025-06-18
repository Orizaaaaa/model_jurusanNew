import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# Load dataset
df = pd.read_csv('dataset.csv')
X = df.drop(columns=['Label'])
y = df['Label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Evaluation
y_pred = model.predict(X_test)
print("✅ Model Evaluation:\n")
print(classification_report(y_test, y_pred))
