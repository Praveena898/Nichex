"""
Fine-tunes DistilBERT on your combined scam text dataset (Kaggle SMS
Spam Collection + your 50 manual scam phrases) to detect scam language.

What this script does:
1. Loads nlp_train.csv and nlp_val.csv (already split in Phase 2)
2. Tokenizes the text using DistilBERT's tokenizer
3. Fine-tunes distilbert-base-uncased for binary classification
   (0 = safe, 1 = scam)
4. Saves the trained model + tokenizer to models/scam_distilbert/
   so src/models/scam_nlp.py can load it later

Run from backend/:
    python scripts/train_scam_nlp.py

Note: this trains on CPU fine since DistilBERT is small and your
dataset (~5,200 rows) is tiny by NLP standards. Expect ~10-20 minutes
on a laptop CPU for 3 epochs.
"""

import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.optim import AdamW
import os

MODEL_NAME = "distilbert-base-uncased"
TRAIN_CSV = "data/nlp_train.csv"
VAL_CSV = "data/nlp_val.csv"
SAVE_DIR = "models/scam_distilbert"

BATCH_SIZE = 16
EPOCHS = 3
LEARNING_RATE = 2e-5
MAX_LEN = 64   # SMS/call messages are short, 64 tokens is plenty
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class ScamTextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=MAX_LEN):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = int(self.labels[idx])

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt"
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "label": torch.tensor(label, dtype=torch.long)
        }


def train():
    print(f"Using device: {DEVICE}")

    print("Loading datasets...")
    train_df = pd.read_csv(TRAIN_CSV)
    val_df = pd.read_csv(VAL_CSV)
    print(f"Train: {len(train_df)} rows | Val: {len(val_df)} rows")

    print(f"Loading tokenizer and model: {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    model.to(DEVICE)

    train_dataset = ScamTextDataset(train_df["text"].tolist(), train_df["label"].tolist(), tokenizer)
    val_dataset = ScamTextDataset(val_df["text"].tolist(), val_df["label"].tolist(), tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)

    best_val_acc = 0.0
    os.makedirs(SAVE_DIR, exist_ok=True)

    for epoch in range(1, EPOCHS + 1):
        # --- Training ---
        model.train()
        train_loss = 0.0
        correct = 0
        total = 0

        for batch in train_loader:
            input_ids = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)
            labels = batch["label"].to(DEVICE)

            optimizer.zero_grad()
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * labels.size(0)
            predicted = torch.argmax(outputs.logits, dim=1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

        train_loss /= total
        train_acc = correct / total

        # --- Validation ---
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch["input_ids"].to(DEVICE)
                attention_mask = batch["attention_mask"].to(DEVICE)
                labels = batch["label"].to(DEVICE)

                outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss

                val_loss += loss.item() * labels.size(0)
                predicted = torch.argmax(outputs.logits, dim=1)
                val_correct += (predicted == labels).sum().item()
                val_total += labels.size(0)

        val_loss /= val_total
        val_acc = val_correct / val_total

        print(f"Epoch {epoch}/{EPOCHS} | "
              f"Train loss: {train_loss:.4f}, acc: {train_acc:.4f} | "
              f"Val loss: {val_loss:.4f}, acc: {val_acc:.4f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            model.save_pretrained(SAVE_DIR)
            tokenizer.save_pretrained(SAVE_DIR)
            print(f"  -> New best model saved (val_acc: {val_acc:.4f})")

    print(f"\nTraining complete. Best validation accuracy: {best_val_acc:.4f}")
    print(f"Model saved to {SAVE_DIR}")


if __name__ == "__main__":
    train()
