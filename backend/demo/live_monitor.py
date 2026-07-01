"""
Live call monitor — captures audio from the microphone in 3-second
chunks and runs the full pipeline on each chunk in real-time.

This is the closest thing to the actual "app running in the background
during a phone call" described in your project concept.

For the demo: play the ElevenLabs-generated fake scam audio through
your laptop speakers while this script listens through the microphone.
You'll see the risk score climb from GREEN to RED in real-time.

Run from backend/:
    python demo/live_monitor.py

Press Ctrl+C to stop.
"""

import os
import sys
import time
import wave
import tempfile
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.pipeline import analyze_audio_file, _load_models
from src.alert_system import send_family_alert

# Config
CHUNK_DURATION = 3        # seconds per analysis window
SAMPLE_RATE = 16000
CHANNELS = 1
FAMILY_PHONE = "+91XXXXXXXXXX"   # replace with real number before demo
ALERT_COOLDOWN = 30       # seconds between repeated family alerts

# Try importing pyaudio — it's optional (skip if not installed)
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False


def print_result(result, chunk_num):
    """Prints a clean, color-coded result to the terminal."""
    color_icons = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}
    icon = color_icons.get(result["color"], "⚪")

    print(f"\n{'='*50}")
    print(f"Chunk #{chunk_num} | {icon} {result['color']} | Score: {result['score']}/100")
    print(f"Transcript:    '{result['transcript']}'")
    print(f"Deepfake prob: {result['deepfake_prob']:.2f} | Scam prob: {result['scam_language_prob']:.2f}")

    if result["color"] == "YELLOW":
        print("⚠️  WARNING: Suspicious call detected. Do NOT share any OTP or personal details.")
    elif result["color"] == "RED":
        print("🚨 SCAM ALERT: High risk call detected! Hang up immediately.")
        if result["alert_family"]:
            print("📱 Alerting family member...")


def record_chunk(duration=CHUNK_DURATION, sample_rate=SAMPLE_RATE):
    """Records one chunk of audio from the microphone, returns a temp .wav filepath."""
    if not PYAUDIO_AVAILABLE:
        raise RuntimeError("pyaudio not installed. Run: pip install pyaudio")

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=sample_rate,
        input=True,
        frames_per_buffer=1024
    )

    frames = []
    num_frames = int(sample_rate / 1024 * duration)
    for _ in range(num_frames):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    pa.terminate()

    # Save to a temp .wav file so pipeline.py can read it
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with wave.open(tmp.name, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))

    return tmp.name


def run_live_monitor():
    print("Digital Bodyguard — Live Call Monitor")
    print("Loading models (first time takes ~10 seconds)...")
    _load_models()
    print("Models ready. Monitoring started. Press Ctrl+C to stop.\n")

    chunk_num = 0
    last_alert_time = 0

    while True:
        chunk_num += 1
        print(f"\nListening... (chunk #{chunk_num})", end="", flush=True)

        try:
            # Record 3 seconds from mic
            wav_path = record_chunk()

            # Run full pipeline
            result = analyze_audio_file(wav_path)

            # Print result
            print_result(result, chunk_num)

            # Fire family alert if RED (with cooldown to avoid SMS spam)
            if result["alert_family"]:
                now = time.time()
                if now - last_alert_time > ALERT_COOLDOWN:
                    try:
                        send_family_alert(FAMILY_PHONE, result["score"])
                        last_alert_time = now
                    except Exception as e:
                        print(f"(Alert failed: {e} — set Twilio env vars to enable)")

            # Clean up temp file
            os.unlink(wav_path)

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")
            break
        except Exception as e:
            print(f"\nError on chunk #{chunk_num}: {e}")
            continue


if __name__ == "__main__":
    run_live_monitor()
