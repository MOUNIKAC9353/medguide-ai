"""
Step 2 - Smart Intent Classification

Trains a TF-IDF + Logistic Regression classifier on intent_dataset.csv.
"""

from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "intent_dataset.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE)

X = df["text"]
y = df["intent"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        sublinear_tf=True
    )),
    ("classifier", LogisticRegression(
        max_iter=3000,
        class_weight="balanced"
    ))
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n======================================")
print("SMART INTENT MODEL TRAINED")
print("======================================")
print(f"Total examples : {len(df)}")
print(f"Training rows  : {len(X_train)}")
print(f"Testing rows   : {len(X_test)}")
print(f"Intents        : {df['intent'].nunique()}")
print(f"Accuracy       : {accuracy:.2%}")

print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))

model_file = MODEL_DIR / "intent_classifier.joblib"
joblib.dump(model, model_file)

print(f"Model saved to: {model_file}")
print("\nThis classifier identifies chatbot intent.")
print("It does not diagnose disease or prescribe medication.")
