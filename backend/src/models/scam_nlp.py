"""
Wraps the fine-tuned DistilBERT model + a keyword rule layer for
scam language detection.

Two-tier design:
- Tier 1 (keyword rules): instant, works offline, catches obvious cases
- Tier 2 (DistilBERT): catches subtler scam language patterns

Imported by risk_engine.py to get a single scam-language probability.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

SCAM_KEYWORDS = [
    "otp", "urgent", "immediately", "don't tell", "confidential",
    "wire transfer", "gift card", "social security", "bail money",
    "verify your identity", "blocked", "suspended", "click this link",
    "remote access", "bank account", "pin number", "claim your prize"
]


def keyword_score(text):
    """
    Tier 1: instant rule-based check.
    Returns a score 0-1 based on how many scam keywords appear.
    """
    text_lower = text.lower()
    matches = sum(1 for kw in SCAM_KEYWORDS if kw in text_lower)
    # Cap at 1.0 — 3+ keyword matches is already maximum suspicion
    return min(matches / 3, 1.0)


class ScamNLPModel:
    def __init__(self, model_path="models/scam_distilbert", device="cpu"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.to(device)
        self.model.eval()

    def predict(self, text):
        """Returns DistilBERT's scam probability for the given text."""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=1)
            scam_prob = probs[0][1].item()  # index 1 = scam class
        return scam_prob

    def combined_score(self, text, bert_weight=0.7, keyword_weight=0.3):
        """
        Combines both tiers into one final scam-language score (0-1).
        Weighted toward BERT since it catches subtler phrasing,
        but keywords still pull the score up fast for obvious cases.
        """
        bert_prob = self.predict(text)
        kw_prob = keyword_score(text)
        return bert_weight * bert_prob + keyword_weight * kw_prob


if __name__ == "__main__":
    # Quick test without needing a trained model — keyword tier only
    test_texts = [
        "Hi mom, just checking in, how are you?",
        "Please share the OTP immediately, don't tell anyone, your account is blocked",
    ]
    for t in test_texts:
        print(f"'{t}' -> keyword_score: {keyword_score(t):.2f}")
