"""
The CNN architecture that classifies a voice as real (0) or AI-generated/
deepfake (1), based on MFCC features.

Imported by:
- training script (to train and save the model)
- the live demo (to load the trained model and run predictions)
"""

import torch
import torch.nn as nn


class DeepfakeCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # Input shape: (batch, 1, 40, 130) — treating MFCC as a 1-channel image
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),          # -> (16, 20, 65)

            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),          # -> (32, 10, 32)

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),          # -> (64, 5, 16)
        )
        self.flatten = nn.Flatten()
        self.fc = nn.Sequential(
            nn.Linear(64 * 5 * 16, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.flatten(x)
        x = self.fc(x)
        return x  # probability that the voice is fake (0-1)


def load_deepfake_model(weights_path="models/deepfake_cnn.pth", device="cpu"):
    """Loads a trained model, ready for inference."""
    model = DeepfakeCNN()
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.eval()
    return model


def predict_deepfake_probability(model, mfcc_array, device="cpu"):
    """
    mfcc_array: numpy array of shape (40, 130) from mfcc_extractor.py
    Returns: float probability (0=real, 1=fake)
    """
    import numpy as np
    x = torch.tensor(mfcc_array, dtype=torch.float32).unsqueeze(0).unsqueeze(0)  # (1,1,40,130)
    x = x.to(device)
    with torch.no_grad():
        prob = model(x).item()
    return prob
