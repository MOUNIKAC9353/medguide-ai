"""
Medical Chatbot - Prediction Test

Use this file after training to test the classifier with your own text.
"""

from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "model" / "condition_classifier.joblib"


def predict_condition(user_text):
    model = joblib.load(MODEL_FILE)

    prediction = model.predict([user_text])[0]

    probabilities = model.predict_proba([user_text])[0]
    classes = model.classes_

    ranked = sorted(
        zip(classes, probabilities),
        key=lambda x: x[1],
        reverse=True,
    )

    return prediction, ranked[:5]


if __name__ == "__main__":
    print("Medical Chatbot ML Prediction Test")
    print("Type 'exit' to stop.\n")

    while True:
        text = input("Describe your symptoms: ").strip()

        if text.lower() == "exit":
            break

        if not text:
            print("Please enter some symptoms.")
            continue

        prediction, top_results = predict_condition(text)

        print(f"\nPredicted category: {prediction}")
        print("\nTop predictions:")

        for condition, probability in top_results:
            print(f"  {condition}: {probability:.2%}")

        print(
            "\nNote: This is an ML prototype and does not confirm a diagnosis."
        )
        print("-" * 50)
