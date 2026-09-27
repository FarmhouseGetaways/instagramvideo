# Edit plan format for `make_reel.py`

```json
{
  "format": "reel",                    // "reel" or "story" (safe zones differ; stories split into <60s parts)
  "output": "work/out/mbm-2026-10-01.mp4",
  "fit": "crop",                       // default for all clips: "crop" fills 9:16, "blur" shows the whole frame
  "hook": {"text": "This was $4 at an estate sale", "dur": 2.5},
  "hook_variants": ["This was $4 at an estate sale", "Guess what I priced this at"],  // Trial Reel A/B: renders _v1, _v2…
  "captions": "auto",                  // Whisper word-by-word captions; false to skip
  "whisper_model": "small",            // base = faster, small = more accurate
  "caption_words": 3,                  // words per caption chunk
  "caption_case": "upper",             // "upper" or "as-is"
  "beats": {"bpm": 120, "every": 2},   // cut every 2 beats; or {"audio": "song.mp3", "every": 2, "start": 0}
  "clips": [
    {"src": "work/raw/IMG_0412.MOV", "in": 3.2, "out": 5.8},
    {"src": "work/raw/IMG_0415.MOV", "in": 0, "out": 2, "speed": 2.0, "fit": "blur", "mute": true},
    {"src": "work/raw/photo.jpg", "dur": 2.5, "text": "Open Saturday 9–3"}
  ],
  "end_text": {"text": "Send this to your thrifting buddy", "dur": 2},
  "music": {"src": "licensed_track.mp3", "start": 12.0, "volume": 0.35},  // only audio we have rights to
  "mute_output": false,                // true = silent export, trending audio added in-app
  "cover": 1.2,                        // seconds; writes *_cover.jpg
  "style": {
    "font": "Montserrat ExtraBold", "primary": "#FFFFFF", "accent": "#F2C14E",
    "outline": "#000000", "hook_style": "box", "box_color": "#FFFFFF", "box_text": "#000000"
  }
}
```

Notes
- Clip `in`/`out` are source seconds. With `beats`, `out` is recalculated so cuts land on the beat.
- Photos get a slow push-in. HDR iPhone footage is tone-mapped to SDR automatically.
- Emoji don't render in burned-in text. Put them in the Instagram caption instead.
- Timing a Reel to a trending in-app sound: set `beats.bpm` to the sound's tempo and
  `mute_output: true`, then add the sound in the app at the matching start point.
