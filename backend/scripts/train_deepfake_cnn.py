"""
Trains the DeepfakeCNN model (defined in src/models/deepfake_cnn.py) on
the MFCC features extracted from ASVspoof in Phase 2.

What this script does, step by step:
1. Loads mfcc_features.npy + labels.npy (your training data)
2. Splits a portion off as an internal validation set (so we can watch
   for overfitting during training, separate from the final test set)
3. Trains the CNN for a set number of epochs using BCELoss + Adam
4. Saves the best-performing version of the model to models/deepfake_cnn.pth
5. Prints accuracy/loss after every epoch so you can see it improving

Run from backend/:
    python scripts/train_deepfake_cnn.py
"""

import os
import sys
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split

# Allow importing from src/ when running this script directly
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.models.deepfake_cnn import DeepfakeCNN

# ---------------- Config ----------------
MFCC_PATH = os.environ.get("MFCC_PATH", "data/mfcc_output/mfcc_features.npy")
LABELS_PATH = os.environ.get("LABELS_PATH", "data/mfcc_output/labels.npy")
MODEL_SAVE_PATH = "models/deepfake_cnn.pth"

BATCH_SIZE = 32
EPOCHS = 25
LEARNING_RATE = 0.001
VAL_SPLIT = 0.1   # 10% of training data held out for validation during training
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class MFCCDataset(Dataset):
    """Wraps the numpy arrays so PyTorch can batch and shuffle them."""
    def __init__(self, features, labels):
        # Add a channel dimension: (N, 40, 130) -> (N, 1, 40, 130)
        self.features = torch.tensor(features, dtype=torch.float32).unsqueeze(1)
        self.labels = torch.tensor(labels, dtype=torch.float32).unsqueeze(1)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


def train_model():
    print(f"Using device: {DEVICE}")

    # --- Load data ---
    print("Loading MFCC features and labels...")
    features = np.load(MFCC_PATH)
    labels = np.load(LABELS_PATH)
    print(f"Loaded {features.shape[0]} samples, feature shape {features.shape[1:]}")

    dataset = MFCCDataset(features, labels)

    # --- Split into train/val ---
    val_size = int(len(dataset) * VAL_SPLIT)
    train_size = len(dataset) - val_size
    train_dataset, val_dataset = random_split(
        dataset, [train_size, val_size],
        generator=torch.Generator().manual_seed(42)  # reproducible split
    )
    print(f"Train: {train_size} samples | Internal val: {val_size} samples")

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

    # --- Model, loss, optimizer ---
    model = DeepfakeCNN().to(DEVICE)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_val_acc = 0.0
    os.makedirs("models", exist_ok=True)

    # --- Training loop ---
    for epoch in range(1, EPOCHS + 1):
        model.train()
        train_loss = 0.0
        correct = 0
        total = 0

        for x_batch, y_batch in train_loader:
            x_batch, y_batch = x_batch.to(DEVICE), y_batch.to(DEVICE)

            optimizer.zero_grad()
            outputs = model(x_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * x_batch.size(0)
            predicted = (outputs > 0.5).float()
            correct += (predicted == y_batch).sum().item()
            total += y_batch.size(0)

        train_loss /= total
        train_acc = correct / total

        # --- Validation ---
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for x_batch, y_batch in val_loader:
                x_batch, y_batch = x_batch.to(DEVICE), y_batch.to(DEVICE)
                outputs = model(x_batch)
                loss = criterion(outputs, y_batch)

                val_loss += loss.item() * x_batch.size(0)
                predicted = (outputs > 0.5).float()
                val_correct += (predicted == y_batch).sum().item()
                val_total += y_batch.size(0)

        val_loss /= val_total
        val_acc = val_correct / val_total

        print(f"Epoch {epoch}/{EPOCHS} | "
              f"Train loss: {train_loss:.4f}, acc: {train_acc:.4f} | "
              f"Val loss: {val_loss:.4f}, acc: {val_acc:.4f}")

        # Save the model only when validation accuracy improves
        # (this avoids saving an overfit later-epoch version)
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"  -> New best model saved (val_acc: {val_acc:.4f})")

    print(f"\nTraining complete. Best validation accuracy: {best_val_acc:.4f}")
    print(f"Model saved to {MODEL_SAVE_PATH}")


if __name__ == "__main__":
    train_model()
