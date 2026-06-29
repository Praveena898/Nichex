from src.models.deepfake_cnn import load_deepfake_model, predict_deepfake_probability
from src.features.mfcc_extractor import extract_mfcc

model = load_deepfake_model('models/deepfake_cnn.pth')
mfcc = extract_mfcc('data/asvspoof2019/LA/ASVspoof2019_LA_train/flac/LA_T_9999995.flac')
prob = predict_deepfake_probability(model, mfcc)
print(f'Deepfake probability: {prob:.4f}')
