"""
The risk engine — the "brain" that combines the deepfake voice score
and the scam language score into one final 0-100 risk number, and
maps it to a color (green/yellow/red).

This is what your demo calls every few seconds during a live call.
"""


def calculate_risk_score(deepfake_prob, scam_language_prob,
                          deepfake_weight=0.6, scam_weight=0.4):
    """
    deepfake_prob: 0-1, from src/models/deepfake_cnn.py
    scam_language_prob: 0-1, from src/models/scam_nlp.py

    Returns: integer risk score 0-100
    """
    score = (deepfake_weight * deepfake_prob + scam_weight * scam_language_prob) * 100
    return round(score)


def get_risk_color(score):
    """Maps a 0-100 score to a color category."""
    if score < 40:
        return "GREEN"
    elif score < 70:
        return "YELLOW"
    else:
        return "RED"


def assess_call_chunk(deepfake_prob, scam_language_prob):
    """
    One call to rule them all — returns everything the demo UI needs
    to display for a single 3-second chunk of the call.
    """
    score = calculate_risk_score(deepfake_prob, scam_language_prob)
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
