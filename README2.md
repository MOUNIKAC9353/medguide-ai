# Step 5 - Symptom Severity Layer

## Purpose

Adds a simple safety layer before the chatbot gives routine guidance.

It checks the user's message for selected high-risk phrases such as:
- severe chest pain
- difficulty breathing
- fainting
- seizure
- heavy bleeding
- sudden confusion

This is NOT a medical diagnosis and the absence of a matched phrase does
NOT mean the user is safe.

## Files

- severity_checker.py
- test_severity.py

## Install

No new package is required.

## Run

python test_severity.py

Then test the interactive checker:

python severity_checker.py

## Next step

The severity checker will be integrated into `chatbot.py`, followed by
verified Ballari healthcare information.
