"""
Step 5 - Symptom Severity Checker

This module does NOT diagnose disease.
It only checks whether the user's message contains selected
high-risk symptom phrases that should trigger urgent-care guidance.

This is a prototype rule-based safety layer.
"""

# Examples of phrases that should be treated as urgent warning signs.
# Keep this list conservative and expand it only with medically reviewed content.
URGENT_PATTERNS = [
    "severe chest pain",
    "chest pain with difficulty breathing",
    "difficulty breathing",
    "difficulty in breathing",
    "trouble breathing",
    "cannot breathe",
    "severe shortness of breath",
    "fainting",
    "unconscious",
    "seizure",
    "heavy bleeding",
    "severe bleeding",
    "sudden weakness",
    "sudden confusion",
    "blue lips",
]


def check_severity(text):
    """
    Returns:
        ("urgent", matched_phrase) if an urgent phrase is found
        ("routine", None) otherwise
    """
    normalized = text.lower().strip()

    for phrase in URGENT_PATTERNS:
        if phrase in normalized:
            return "urgent", phrase

    return "routine", None


if __name__ == "__main__":
    print("Symptom Severity Checker")
    print("Type 'exit' to stop.")

    while True:
        text = input("\nUser: ").strip()

        if text.lower() == "exit":
            break

        severity, matched = check_severity(text)

        if severity == "urgent":
            print("\nSeverity: URGENT")
            print(f"Matched warning sign: {matched}")
            print("Please seek immediate medical attention.")
        else:
            print("\nSeverity: ROUTINE / NO SELECTED RED FLAG FOUND")
            print("This does NOT mean the condition is harmless.")
