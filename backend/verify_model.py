from src.models.deepfake_cnn import load_deepfake_model, predict_deepfake_probability
from src.features.mfcc_extractor import extract_mfcc

MODEL_PATH = "models/deepfake_cnn.pth"

files = [
    "LA_E_5849185.flac",
    "LA_E_4581379.flac",
    "LA_E_6314733.flac",
    "LA_E_3379393.flac",
]

base = "data/asvspoof2019/LA/ASVspoof2019_LA_eval/flac/"

model = load_deepfake_model(MODEL_PATH)

print("=" * 50)
print("ASVSPOOF REAL VOICE TEST — AFTER FINE-TUNING")
print("=" * 50)

for filename in files:
    filepath = base + filename

    mfcc = extract_mfcc(filepath)
    prob = predict_deepfake_probability(model, mfcc)

    prediction = "FAKE" if prob >= 0.5 else "REAL"

    print(f"\nFile: {filename}")
    print("Expected: REAL")
    print(f"Deepfake probability: {prob:.4f}")
    print(f"Prediction: {prediction}")

print("\n" + "=" * 50)