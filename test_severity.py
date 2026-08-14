from severity_checker import check_severity

tests = [
    "I have fever and cold",
    "I have severe chest pain",
    "I have difficulty breathing",
    "I have a headache",
]

for text in tests:
    severity, matched = check_severity(text)
    print(f"\nInput: {text}")
    print(f"Severity: {severity}")
    if matched:
        print(f"Matched: {matched}")
