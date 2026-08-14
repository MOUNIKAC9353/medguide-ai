# Medical Chatbot ML - Step 1

This folder contains the first machine-learning component of the project.

## Files

- `medical_chatbot_initial_dataset.csv` - initial 30-condition dataset
- `train_model.py` - trains the TF-IDF + Logistic Regression model
- `predict.py` - tests the trained model
- `requirements.txt` - Python packages

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Train:

```bash
python train_model.py
```

Test:

```bash
python predict.py
```

## Important

This is an educational ML prototype. The classifier estimates a category from text.
It must not be treated as a medical diagnosis or as an automated prescription system.
