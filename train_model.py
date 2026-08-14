"""
Medical Chatbot - First ML Prototype

The original training script failed because the initial dataset has
only one row per condition. A stratified train/test split requires
at least two examples in every class.

This version trains on all 30 rows so the prototype model can be created.
After that, we will build a proper multi-example intent dataset and
perform a real train/test evaluation.
"""

from pathlib import Path
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "medical_chatbot_initial_dataset.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_DIR.mkdir(exist_ok=True)


def load_data():
    df = pd.read_csv(DATA_FILE)

    required_columns = ["condition", "symptoms", "warning_signs"]
    missing = [c for c in required_columns if c not in df.columns]

    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")

    df["text"] = (
        df["condition"].fillna("")
        + " "
        + df["symptoms"].fillna("").str.replace(";", " ", regex=False)
        + " "
        + df["warning_signs"].fillna("").str.replace(";", " ", regex=False)
    )

    return df


def train_model(df):
    X = df["text"]
    y = df["condition"]

    model = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    sublinear_tf=True,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=3000,
                    class_weight="balanced",
                ),
            ),
        ]
    )

    model.fit(X, y)

    model_file = MODEL_DIR / "condition_classifier.joblib"
    joblib.dump(model, model_file)

    print("\n======================================")
    print("MODEL TRAINING COMPLETED")
    print("======================================")
    print(f"Training examples : {len(df)}")
    print(f"Conditions        : {df['condition'].nunique()}")
    print(f"Model saved to    : {model_file}")

    print("\nNOTE:")
    print("This is a prototype classifier, not a medical diagnosis.")
    print("A proper accuracy test will be added after we create")
    print("multiple natural-language examples for each class.")


def main():
    print("Loading dataset...")
    df = load_data()

    print(f"Loaded {len(df)} conditions.")
    print("Training model...")

    train_model(df)


if __name__ == "__main__":
    main()
