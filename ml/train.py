import os
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import pandas as pd
import joblib

# Synthetic training data — replace with real ICU dataset (e.g. MIMIC-III) before production
data = {
    "heart_rate":       [80, 95, 110, 70, 120, 85, 105, 72, 115, 90],
    "temperature":      [36.5, 38.2, 39.1, 36.8, 40.0, 37.0, 38.8, 36.6, 39.5, 37.5],
    "respiratory_rate": [18, 22, 30, 16, 35, 19, 28, 15, 32, 21],
    "sepsis":           [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
}

df = pd.DataFrame(data)
X = df[["heart_rate", "temperature", "respiratory_rate"]]
y = df["sepsis"]

# Pipeline: scale features then classify (important for logistic regression)
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(random_state=42)),
])

scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")
print(f"Cross-val accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})")

pipeline.fit(X, y)

output_path = os.path.join(os.path.dirname(__file__), "model.joblib")
joblib.dump(pipeline, output_path)
print(f"Model saved to {output_path}")
