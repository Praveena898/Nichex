"""
Splits any labeled dataset (audio file list OR text dataset) into
80% train / 10% validation / 10% test.

Why split FIRST, before touching the model:
- If you tune feature extraction or balance classes AFTER splitting,
  you leak information between sets and your test accuracy becomes
  meaningless (you'll think the model is better than it really is).
- The test set should stay completely untouched until the very end,
  used only once to report final accuracy.

Works for both:
  A) Text/NLP dataset (a CSV with 'text','label' columns)
  B) Audio dataset (a CSV with 'filepath','label' columns, e.g. ASVspoof)
"""

import pandas as pd
from sklearn.model_selection import train_test_split

def split_dataset(csv_path, label_col="label", save_prefix="dataset"):
    df = pd.read_csv(csv_path)
    print(f"Total rows: {len(df)}")
    print(f"Class balance:\n{df[label_col].value_counts()}")

    # Step 1: split off 80% train, 20% temp (which becomes val+test)
    # stratify=df[label_col] keeps the same class ratio in every split —
    # crucial here since scam/fake examples are usually the minority class
    train_df, temp_df = train_test_split(
        df,
        test_size=0.20,
        stratify=df[label_col],
        random_state=42  # fixed seed = reproducible splits every run
    )

    # Step 2: split the remaining 20% into 10% val, 10% test (50/50 of the 20%)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        stratify=temp_df[label_col],
        random_state=42
    )

    print(f"\nTrain: {len(train_df)} ({len(train_df)/len(df)*100:.1f}%)")
    print(f"Val:   {len(val_df)} ({len(val_df)/len(df)*100:.1f}%)")
    print(f"Test:  {len(test_df)} ({len(test_df)/len(df)*100:.1f}%)")

    train_df.to_csv(f"data/{save_prefix}_train.csv", index=False)
    val_df.to_csv(f"data/{save_prefix}_val.csv", index=False)
    test_df.to_csv(f"data/{save_prefix}_test.csv", index=False)
    print(f"\nSaved 3 files: {save_prefix}_train.csv, _val.csv, _test.csv")

    return train_df, val_df, test_df


if __name__ == "__main__":
    split_dataset(
        "data/combined_scam_dataset.csv",
        label_col="label",
        save_prefix="nlp"
    )

    print("\nDataset split completed successfully!")