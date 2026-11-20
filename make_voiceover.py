#!/usr/bin/env python3
"""
Voiceover from a PowerPoint's speaker notes using Microsoft's en-IN-NeerjaNeural.
After each slide: "Next slide." then 2 seconds of silence (not after the last slide).

SETUP
  python3 -m venv .venv && source .venv/bin/activate
  pip install edge-tts python-pptx
  sudo apt install -y ffmpeg        # needed to decode/encode audio

USAGE
  python make_voiceover_neerja.py deck.pptx --out voiceover.mp3
  python make_voiceover_neerja.py deck.pptx --rate=-5% --voice en-IN-AashiNeural

Needs internet (edge-tts calls Microsoft's online speech service).
"""
import argparse
import asyncio
import os
import subprocess
import tempfile
import wave

import edge_tts
from pptx import Presentation

SR = 48000
PAUSE_BEFORE_NEXT = 0.6   # seconds of silence before "Next slide."
PAUSE_AFTER_NEXT = 2.0    # seconds of silence after "Next slide."


async def synth(text, voice, rate, path):
    await edge_tts.Communicate(text, voice, rate=rate).save(path)


def to_pcm(src):
    """Decode any audio file to raw 24 kHz mono 16-bit PCM bytes."""
    return subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-i", src, "-ar", str(SR), "-ac", "1",
         "-f", "s16le", "-"], check=True, capture_output=True).stdout


def silence(sec):
    return b"\x00\x00" * int(SR * sec)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--out", default="voiceover.mp3")
    ap.add_argument("--voice", default="en-IN-NeerjaNeural")
    ap.add_argument("--rate", default="+0%", help='speaking speed, e.g. "-10%%" (use --rate=-10%%)')
    args = ap.parse_args()

    slides = list(Presentation(args.pptx).slides)
    tmp = tempfile.mkdtemp()

    nxt_path = os.path.join(tmp, "next.mp3")
    await synth("Next slide.", args.voice, args.rate, nxt_path)
    next_pcm = to_pcm(nxt_path)

    audio, pos = b"", 0
    for i, slide in enumerate(slides, 1):
        notes = slide.notes_slide.notes_text_frame.text.strip() if slide.has_notes_slide else ""
        secs = pos / 2 / SR
        print(f"slide {i} starts at {int(secs // 60)}:{int(secs % 60):02d}")
        if notes:
            p = os.path.join(tmp, f"s{i}.mp3")
            await synth(notes, args.voice, args.rate, p)
            audio += to_pcm(p)
        if i < len(slides):
            audio += silence(PAUSE_BEFORE_NEXT) + next_pcm + silence(PAUSE_AFTER_NEXT)
        pos = len(audio)

    wav_path = os.path.join(tmp, "all.wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(audio)

    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
                    "-b:a", "128k", args.out], check=True)
    print(f"done: {args.out} ({len(audio) / 2 / SR:.0f} sec)")


if __name__ == "__main__":
    asyncio.run(main())