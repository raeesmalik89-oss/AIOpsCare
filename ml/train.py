
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

FEATURES = ["HR","O2Sat","Temp","SBP","MAP","Resp","Age","ICULOS"]

print("Loading real PhysioNet dataset...")
df = pd.read_csv("data/Dataset.csv")
df = df[FEATURES + ["SepsisLabel"]].dropna()

X = df[FEATURES]
y = df["SepsisLabel"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
])

print("Training on real ICU patient data...")
pipeline.fit(X_train, y_train)

print(classification_report(y_test, pipeline.predict(X_test)))

output_path = os.path.join(os.path.dirname(__file__), "model.joblib")
joblib.dump(pipeline, output_path)
print(f"Model saved to {output_path}")
