"""
File-based demo — runs the full pipeline on a pre-recorded audio file
instead of a live microphone. Perfect for classroom presentations where
you want a controlled, reproducible demo.

Demo flow for presentation:
1. Generate a fake scam call audio using ElevenLabs (voice saying
   "Please share the OTP immediately, don't tell anyone, urgent!")
2. Save it as demo/sample_scam_call.wav
3. Run this script — it processes the file and shows the RED alert
4. Then run it on a normal voice file to show the GREEN result

Run from backend/:
    python demo/file_demo.py --audio demo/sample_scam_call.wav
    python demo/file_demo.py --audio demo/sample_normal_call.wav
"""

import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.pipeline import analyze_audio_file


def run_file_demo(audio_path):
    if not os.path.exists(audio_path):
        print(f"File not found: {audio_path}")
        print("Please provide a valid audio file path.")
        return

    print("\n" + "=" * 50)
    print("   DIGITAL BODYGUARD — Analysis Report")
    print("=" * 50)
    print(f"Analyzing: {audio_path}")
    print("Running models...\n")

    result = analyze_audio_file(audio_path)

    color_icons = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}
    icon = color_icons.get(result["color"], "⚪")

    print(f"TRANSCRIPT:      '{result['transcript']}'")
    print(f"DEEPFAKE PROB:   {result['deepfake_prob']:.2f}  (0=real voice, 1=AI voice)")
    print(f"SCAM LANG PROB:  {result['scam_language_prob']:.2f}  (0=safe, 1=scam language)")
    print(f"RISK SCORE:      {result['score']}/100")
    print(f"STATUS:          {icon} {result['color']}")
    print("-" * 50)

    if result["color"] == "GREEN":
        print("✅ Call appears safe. No action needed.")
    elif result["color"] == "YELLOW":
        print("⚠️  Suspicious patterns detected.")
        print("   Recommendation: Do NOT share OTP or personal details.")
    elif result["color"] == "RED":
        print("🚨 HIGH RISK — Likely scam or deepfake call detected!")
        print("   Recommendation: Hang up immediately.")
        print("   Action taken: Family member will be alerted.")

    print("=" * 50)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Digital Bodyguard File Demo")
    parser.add_argument(
        "--audio",
        type=str,
        default="data/asvspoof2019/LA/ASVspoof2019_LA_train/flac/LA_T_9999995.flac",
        help="Path to audio file to analyze"
    )
    args = parser.parse_args()
    run_file_demo(args.audio)
