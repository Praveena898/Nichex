"""
The risk engine — the "brain" that combines the deepfake voice score
and the scam language score into one final 0-100 risk number, and
maps it to a color (green/yellow/red).

This is what your demo calls every few seconds during a live call.
"""


def calculate_risk_score(
    deepfake_prob,
    scam_language_prob,
    deepfake_weight=0.4,
    scam_weight=0.6
):
    score = (
        deepfake_weight * deepfake_prob
        + scam_weight * scam_language_prob
    ) * 100

    return round(score)


def get_risk_color(score):
    if score < 40:
        return "GREEN"
    elif score < 70:
        return "YELLOW"
    else:
        return "RED"
    
CRITICAL_KEYWORDS = [
    "otp",
    "pin",
    "cvv",
    "password",
    "upi pin",
    "net banking password",
    "transfer money",
    "wire transfer",
    "gift card",
    "remote access",
    "anydesk",
    "teamviewer"
]

SUSPICIOUS_KEYWORDS = [
    "credentials",
    "verify",
    "identity",
    "bank details",
    "refund",
    "income tax",
    "blocked account",
    "debit card",
    "credit card",
    "kyc",
    "account details",
    "unusual activity",
    "suspicious activity"
]

def assess_call_chunk(deepfake_prob, scam_language_prob, transcript):
    score = calculate_risk_score(
        deepfake_prob,
        scam_language_prob,
        deepfake_weight=0.4,
        scam_weight=0.6
    )

    text = transcript.lower()

    # ---------------------------------------------------------
    # 1. Strong AI/deepfake evidence
    # ---------------------------------------------------------
    if deepfake_prob >= 0.8:
        score = max(score, 90)

    # ---------------------------------------------------------
    # 2. Critical scam keywords
    # ---------------------------------------------------------
    elif any(word in text for word in CRITICAL_KEYWORDS):
        score = max(score, 85)

    # ---------------------------------------------------------
    # 3. Suspicious keywords
    # ---------------------------------------------------------
    elif any(word in text for word in SUSPICIOUS_KEYWORDS):
        score = max(score, 60)

    # ---------------------------------------------------------
    # 4. NLP probability
    # ---------------------------------------------------------
    elif scam_language_prob >= 0.9:
        score = max(score, 75)

    elif scam_language_prob >= 0.5:
        score = max(score, 60)

    elif scam_language_prob >= 0.35:
        score = max(score, 40)

    color = get_risk_color(score)

    return {
        "score": score,
        "color": color,
        "deepfake_prob": round(deepfake_prob, 2),
        "scam_language_prob": round(scam_language_prob, 2),
        "alert_family": color == "RED"
    }

if __name__ == "__main__":
    # Quick sanity tests
    print(assess_call_chunk(0.1, 0.0))   # expect GREEN
    print(assess_call_chunk(0.5, 0.6))   # expect YELLOW
    print(assess_call_chunk(0.9, 0.95))  # expect RED, alert_family True
