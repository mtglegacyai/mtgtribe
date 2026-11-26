#!/usr/bin/env python3
"""Watch and listen to a video MTG sends: timed transcript + contact sheets.

Usage: python3 intake_video.py <video> <out dir> [model]

Writes into <out dir>:
  transcript.txt   one line per segment, "[start-end] text" (faster-whisper, local and free)
  frames/          one frame per second (360 px wide)
  sheet_01.jpg ... 20 frames per sheet (10 x 2), to look at with the Read tool
  info.txt         duration, size, frame rate

Model defaults to medium.en (good on names); small.en is faster. Installs faster-whisper on first run.
Names are often misheard (Claude -> "cloud"): always correct them from the frames.
"""
import glob
import json
import os
import subprocess
import sys
import wave


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    video, out = sys.argv[1], sys.argv[2]
    model_name = sys.argv[3] if len(sys.argv) > 3 else "medium.en"
    os.makedirs(os.path.join(out, "frames"), exist_ok=True)

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
         "-of", "json", video], check=True, capture_output=True, text=True).stdout
    with open(os.path.join(out, "info.txt"), "w") as f:
        f.write(json.dumps(json.loads(probe), indent=1))

    # Frames, one per second, and contact sheets of 20.
    for old in glob.glob(os.path.join(out, "frames", "f_*.jpg")):
        os.remove(old)
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", "fps=1,scale=360:-2",
         os.path.join(out, "frames", "f_%03d.jpg")])
    n = len(glob.glob(os.path.join(out, "frames", "f_*.jpg")))
    for i, start in enumerate(range(1, n + 1, 20), 1):
        run(["ffmpeg", "-v", "error", "-y", "-start_number", str(start), "-i",
             os.path.join(out, "frames", "f_%03d.jpg"), "-frames:v", "1",
             "-vf", "scale=240:-2,tile=10x2", os.path.join(out, f"sheet_{i:02d}.jpg")])

    # Audio for speech-to-text: mono 16 kHz WAV, read directly (avoids PyAV version clashes).
    wav = os.path.join(out, "audio16k.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-ac", "1", "-ar", "16000", wav])
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        run([sys.executable, "-m", "pip", "install", "-q", "faster-whisper"])
        from faster_whisper import WhisperModel
    import numpy as np

    w = wave.open(wav)
    audio = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio, language="en", beam_size=5)
    lines = [f"[{s.start:6.1f}-{s.end:6.1f}] {s.text.strip()}" for s in segments]
    with open(os.path.join(out, "transcript.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\n{n} frames, {len(glob.glob(os.path.join(out, 'sheet_*.jpg')))} contact sheets in {out}")


if __name__ == "__main__":
    main()
