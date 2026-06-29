"""
Evaluates the trained DistilBERT scam classifier on the held-out test
set (nlp_test.csv) — text the model has never seen.

Run from backend/:
    python scripts/evaluate_scam_nlp.py
"""

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

MODEL_DIR = "models/scam_distilbert"
TEST_CSV = "data/nlp_test.csv"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def evaluate():
    print(f"Using device: {DEVICE}")
    print("Loading test data...")
    test_df = pd.read_csv(TEST_CSV)
    print(f"Test set size: {len(test_df)} rows")

    print("Loading trained model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.to(DEVICE)
    model.eval()

    all_preds = []
    texts = test_df["text"].tolist()
    labels = test_df["label"].tolist()

    with torch.no_grad():
        for text in texts:
            inputs = tokenizer(str(text), return_tensors="pt", truncation=True, padding=True, max_length=64)
            inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
            logits = model(**inputs).logits
            pred = torch.argmax(logits, dim=1).item()
            all_preds.append(pred)

    acc = accuracy_score(labels, all_preds)
    precision = precision_score(labels, all_preds)
    recall = recall_score(labels, all_preds)
    f1 = f1_score(labels, all_preds)
    cm = confusion_matrix(labels, all_preds)

    print("\n" + "=" * 40)
    print("EVALUATION RESULTS (on unseen test set)")
    print("=" * 40)
    print(f"Accuracy:  {acc:.4f}  ({acc*100:.2f}%)")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"\nConfusion Matrix:")
    print(f"                Predicted Safe   Predicted Scam")
    print(f"Actual Safe     {cm[0][0]:<16} {cm[0][1]}")
    print(f"Actual Scam     {cm[1][0]:<16} {cm[1][1]}")
    print("=" * 40)


if __name__ == "__main__":
    evaluate()
