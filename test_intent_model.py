"""
Step 2 - Test the Smart Intent Classifier
"""

from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "model" / "intent_classifier.joblib"

model = joblib.load(MODEL_FILE)

print("Smart Intent Classifier")
print("Type 'exit' to stop.\n")

while True:
    text = input("User: ").strip()

    if text.lower() == "exit":
        break

    if not text:
        continue

    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]

    ranked = sorted(
        zip(model.classes_, probabilities),
        key=lambda x: x[1],
        reverse=True
    )

    print(f"\nPredicted intent: {prediction}")
    print("Top predictions:")

    for intent, probability in ranked[:3]:
        print(f"  {intent}: {probability:.2%}")

    print()
