#!/usr/bin/env python3
"""Narration for make_reel.py: synthesizes each line with Kokoro TTS and places it on the timeline.

Plan field:
  "voiceover": {
    "voice": "af_heart", "speed": 0.95, "ambient_volume": 0.3,
    "lines": [{"text": "There's a little red barn…", "at": 0.3}, ...]
  }
Or use a recorded voiceover instead of TTS: {"src": "work/raw/my_vo.m4a", "at": 0.0}
"""
import subprocess

import numpy as np

SR = 24000
GAP = 0.15  # minimum breath between lines


def build(vo, out_wav):
    """Write the full narration track to out_wav. Returns [(start, end, text), …]."""
    if "src" in vo:
        at = float(vo.get("at", 0.0))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vo["src"],
                        "-af", f"adelay={int(at * 1000)}:all=1", "-ar", str(SR), "-ac", "1", out_wav],
                       check=True)
        return [(at, None, "")]

    import soundfile as sf
    from kokoro import KPipeline

    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    voice, speed = vo.get("voice", "af_heart"), vo.get("speed", 0.95)
    placed, track, cursor = [], np.zeros(0, dtype=np.float32), 0.0
    for line in vo["lines"]:
        audio = np.concatenate([a.numpy() if hasattr(a, "numpy") else a
                                for _, _, a in pipe(line["text"], voice=line.get("voice", voice),
                                                    speed=line.get("speed", speed))])
        start = max(float(line.get("at", cursor)), cursor)
        s = int(start * SR)
        if len(track) < s + len(audio):
            track = np.pad(track, (0, s + len(audio) - len(track)))
        track[s:s + len(audio)] += audio
        end = start + len(audio) / SR
        placed.append((round(start, 2), round(end, 2), line["text"]))
        cursor = end + GAP
    sf.write(out_wav, track, SR)
    return placed
