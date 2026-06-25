"""
Converts ASVspoof's protocol .txt files into a clean filepath,label CSV
that split_dataset.py and extract_mfcc.py can use directly.

ASVspoof protocol file format (space-separated, 5 columns):
    LA_0079  LA_T_1138215  -  -  bonafide
    speaker  filename       -  -  label  (bonafide = real, spoof = fake)

label mapping used everywhere else in this project:
    0 = real/bonafide
    1 = fake/spoof  (this matches deepfake_cnn.py's sigmoid output meaning)
"""

import pandas as pd
import os


def parse_protocol_file(protocol_path, audio_dir, file_ext=".flac"):
    """
    protocol_path: path to e.g. ASVspoof2019.LA.cm.train.trn.txt
    audio_dir: path to the matching flac folder, e.g.
               data/asvspoof2019/LA/ASVspoof2019_LA_train/flac
    """
    rows = []
    with open(protocol_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue  # skip malformed lines

            _, filename, _, _, label_word = parts

            label = 0 if label_word == "bonafide" else 1
            filepath = os.path.join(audio_dir, filename + file_ext)

            rows.append({"filepath": filepath, "label": label})

    return pd.DataFrame(rows)


def build_all_asvspoof_csvs(base_dir="data/asvspoof2019/LA"):
    """
    Builds 3 CSVs matching ASVspoof's own train/dev/eval split
    (these become your filepath,label inputs — you can still re-split
    them with split_dataset.py afterward if you want a different ratio,
    but ASVspoof's own splits are already well-balanced and standard
    to use as-is).
    """
    configs = [
        ("ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt",
         "ASVspoof2019_LA_train/flac", "asvspoof_train.csv"),
        ("ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.dev.trl.txt",
         "ASVspoof2019_LA_dev/flac", "asvspoof_dev.csv"),
        ("ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.eval.trl.txt",
         "ASVspoof2019_LA_eval/flac", "asvspoof_eval.csv"),
    ]

    for protocol_rel, audio_rel, out_name in configs:
        protocol_path = os.path.join(base_dir, protocol_rel)
        audio_dir = os.path.join(base_dir, audio_rel)

        df = parse_protocol_file(protocol_path, audio_dir)
        out_path = os.path.join("data", out_name)
        df.to_csv(out_path, index=False)

        print(f"{out_name}: {len(df)} files "
              f"({sum(df.label==0)} real, {sum(df.label==1)} fake)")
        print(f"  Saved to {out_path}\n")


if __name__ == "__main__":
    build_all_asvspoof_csvs()
