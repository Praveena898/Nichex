"""
Evaluates the trained deepfake CNN on the eval set (71,237 files this
model has NEVER seen during training) to get a real accuracy number.

This is the moment of truth: training accuracy can be misleadingly
high if the model memorized the training data. Eval accuracy tells
you how well it actually generalizes to new voices.

Run from backend/:
    python scripts/evaluate_deepfake_cnn.py
"""

import numpy as np
import torch
import os
import sys
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Allow importing from src/ when running this script directly
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.models.deepfake_cnn import DeepfakeCNN

MFCC_PATH = "data/mfcc_output_eval/mfcc_features.npy"
LABELS_PATH = "data/mfcc_output_eval/labels.npy"
MODEL_PATH = "models/deepfake_cnn.pth"
BATCH_SIZE = 64
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def evaluate():
    print(f"Using device: {DEVICE}")
    print("Loading eval features and labels...")
    features = np.load(MFCC_PATH)
    labels = np.load(LABELS_PATH)
    print(f"Eval set size: {features.shape[0]} samples")

    # Load trained model
    model = DeepfakeCNN().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()

    all_preds = []
    all_probs = []

    # Run in batches (71k samples at once would use too much memory)
    with torch.no_grad():
        for i in range(0, len(features), BATCH_SIZE):
            batch_feats = features[i:i + BATCH_SIZE]
            x = torch.tensor(batch_feats, dtype=torch.float32).unsqueeze(1).to(DEVICE)
            outputs = model(x).cpu().numpy().flatten()

            all_probs.extend(outputs)
            all_preds.extend((outputs > 0.5).astype(int))

            if i % 5000 == 0:
                print(f"Evaluated {i}/{len(features)}")

    all_preds = np.array(all_preds)
    labels = np.array(labels)

    # --- Metrics ---
    acc = accuracy_score(labels, all_preds)
    precision = precision_score(labels, all_preds)
    recall = recall_score(labels, all_preds)
    f1 = f1_score(labels, all_preds)
    cm = confusion_matrix(labels, all_preds)

    print("\n" + "=" * 40)
    print("EVALUATION RESULTS (on unseen eval set)")
    print("=" * 40)
    print(f"Accuracy:  {acc:.4f}  ({acc*100:.2f}%)")
    print(f"Precision: {precision:.4f}  (of files flagged fake, how many really were)")
    print(f"Recall:    {recall:.4f}  (of all real fakes, how many we caught)")
    print(f"F1 Score:  {f1:.4f}")
    print(f"\nConfusion Matrix:")
    print(f"                Predicted Real   Predicted Fake")
    print(f"Actual Real     {cm[0][0]:<16} {cm[0][1]}")
    print(f"Actual Fake     {cm[1][0]:<16} {cm[1][1]}")
    print("=" * 40)


if __name__ == "__main__":
    evaluate()