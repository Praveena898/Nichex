"""
Merges the Kaggle SMS Spam Collection dataset with your manually
written scam phrases into one clean, combined CSV ready for splitting.

Kaggle's spam.csv has messy column names (v1, v2, plus 3 junk columns).
This script cleans that up into a standard 'text', 'label' format
matching what split_dataset.py and the DistilBERT trainer expect.

label: 0 = safe/ham, 1 = scam/spam
"""

import pandas as pd
from add_manual_scam_phrases import build_manual_dataset


def clean_kaggle_spam(csv_path="data/kaggle/spam.csv"):
    df = pd.read_csv(csv_path, encoding="latin-1")

    # Keep only the real columns, rename to standard names
    df = df[["v1", "v2"]].rename(columns={"v1": "label_text", "v2": "text"})

    # Convert ham/spam text labels into 0/1 numbers
    df["label"] = df["label_text"].map({"ham": 0, "spam": 1})

    # Drop the now-unneeded text label column, drop any blank rows
    df = df[["text", "label"]].dropna()

    return df


def build_combined_dataset(
    kaggle_path="data/kaggle/spam.csv",
    output_path="data/combined_scam_dataset.csv"
):
    kaggle_df = clean_kaggle_spam(kaggle_path)
    manual_df = build_manual_dataset()

    combined = pd.concat([kaggle_df, manual_df], ignore_index=True)

    # Remove exact duplicate messages, just in case
    combined = combined.drop_duplicates(subset="text")

    combined.to_csv(output_path, index=False)

    print(f"Kaggle dataset: {len(kaggle_df)} rows")
    print(f"Manual phrases: {len(manual_df)} rows")
    print(f"Combined total: {len(combined)} rows (after removing duplicates)")
    print(f"Class balance:\n{combined['label'].value_counts()}")
    print(f"\nSaved to {output_path}")

    return combined


if __name__ == "__main__":
    build_combined_dataset()
