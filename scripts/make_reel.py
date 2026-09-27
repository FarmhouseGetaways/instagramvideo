#!/usr/bin/env python3
"""Render a finished Instagram Reel or Story set from a JSON edit plan.

Usage: python3 scripts/make_reel.py plan.json

See scripts/PLAN_FORMAT.md for every field. Minimal plan:
{
  "format": "reel",                      # reel | story
  "output": "work/out/barn-tour.mp4",
  "hook": {"text": "POV: you found the cutest barn market", "dur": 2.5},
  "captions": "auto",
  "clips": [{"src": "work/raw/IMG_0001.MOV", "in": 1.0, "out": 3.5}]
}
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".heic", ".webp"}

# Areas covered by Instagram's interface on a 1080x1920 canvas (see knowledge/instagram-specs.md)
SAFE = {
    "reel":  {"top": 220, "bottom": 420, "left": 70, "right": 160},
    "story": {"top": 250, "bottom": 340, "left": 70, "right": 70},
}
STORY_MAX_SEG = 55  # Instagram splits Stories over 60s; segmenter cuts at the next keyframe, so leave headroom

DEFAULT_STYLE = {
    "font": "Montserrat ExtraBold",
    "primary": "#FFFFFF",
    "accent": "#F2C14E",
    "outline": "#000000",
    "hook_size": 92,
    "caption_size": 80,
    "text_size": 68,
    "hook_style": "outline",  # outline | box (dark text on a solid box, the "Instagram text" look)
    "box_color": "#FFFFFF",
    "box_text": "#000000",
}

X264 = ["-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r.stdout


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "stream=codec_type,color_transfer:format=duration", "-of", "json", path])
    info = json.loads(out)
    streams = info.get("streams", [])
    video = next((s for s in streams if s["codec_type"] == "video"), {})
    return {
        "duration": float(info.get("format", {}).get("duration", 0) or 0),
        "has_audio": any(s["codec_type"] == "audio" for s in streams),
        "hdr": video.get("color_transfer") in ("arib-std-b67", "smpte2084"),
    }


def atempo_chain(speed):
    parts = []
    while speed > 2.0:
        parts.append("atempo=2.0")
        speed /= 2.0
    while speed < 0.5:
        parts.append("atempo=0.5")
        speed /= 0.5
    parts.append(f"atempo={speed:.4f}")
    return ",".join(parts)


def fit_filter(fit):
    if fit == "blur":
        return ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,boxblur=30:5[bg];[b]scale=1080:1920:force_original_aspect_ratio="
                "decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
    return "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"


TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,")


def beat_durations(beats, count):
    """Clip lengths that land every cut on the beat."""
    every = beats.get("every", 2)
    if "bpm" in beats:
        return [60.0 / beats["bpm"] * every] * count
    import librosa
    y, sr = librosa.load(beats["audio"], sr=None, mono=True)
    _, frames = librosa.beat.beat_track(y=y, sr=sr)
    times = list(librosa.frames_to_time(frames, sr=sr))
    start = beats.get("start", 0.0)
    times = [t for t in times if t >= start]
    cuts = [start] + times[every - 1::every]
    return [b - a for a, b in zip(cuts, cuts[1:])][:count]


def render_clip(clip, idx, default_fit, tmp):
    src = clip["src"]
    out = os.path.join(tmp, f"clip{idx:03d}.mp4")
    fit = clip.get("fit", default_fit)
    speed = float(clip.get("speed", 1.0))
    is_image = os.path.splitext(src)[1].lower() in IMAGE_EXT

    if is_image:
        dur = float(clip.get("dur", 2.5))
        frames = int(dur * 30)
        # Slow push-in so still photos don't feel static
        vf = (f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
              f"zoompan=z='min(1+0.0015*on,1.15)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'"
              f":d={frames}:s=1080x1920:fps=30,format=yuv420p,setsar=1")
        run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", src,
             "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
             "-filter_complex", f"[0:v]{vf}[v]", "-map", "[v]", "-map", "1:a",
             "-t", f"{dur:.3f}", *X264, "-preset", "veryfast", "-crf", "16",
             "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out])
        return out, dur

    info = probe(src)
    t_in = float(clip.get("in", 0.0))
    t_out = float(clip.get("out", info["duration"]))
    t_out = min(t_out, info["duration"])
    src_len = max(0.1, t_out - t_in)
    dur = src_len / speed

    vf = (TONEMAP if info["hdr"] else "") + fit_filter(fit)
    vf += f",setpts=(PTS-STARTPTS)/{speed},fps=30,format=yuv420p,setsar=1"
    use_audio = info["has_audio"] and not clip.get("mute", False)
    inputs = ["-ss", f"{t_in:.3f}", "-t", f"{src_len:.3f}", "-i", src]
    if use_audio:
        vol = clip.get("volume", 1.0)
        af = f"[0:a]asetpts=PTS-STARTPTS,{atempo_chain(speed)},volume={vol},aresample=48000,aformat=channel_layouts=stereo[a]"
        amap = ["-map", "[a]"]
    else:
        inputs += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        af = None
        amap = ["-map", "1:a"]
    fc = f"[0:v]{vf}[v]" + (f";{af}" if af else "")
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", fc,
         "-map", "[v]", *amap, "-t", f"{dur:.3f}", *X264, "-preset", "veryfast",
         "-crf", "16", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out])
    return out, dur


def ass_color(hex_color, alpha=0):
    h = hex_color.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H{alpha:02X}{b}{g}{r}".upper()


def ass_time(t):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def ass_escape(text):
    return text.replace("{", "(").replace("}", ")").replace("\n", "\\N")


def build_ass(plan, style, fmt, clip_starts, words, total):
    s = SAFE[fmt]
    c = {k: ass_color(style[k]) for k in ("primary", "accent", "outline")}
    font = style["font"]
    ml, mr = s["left"], s["right"]
    hook_v = s["top"] + 60
    cap_v = s["bottom"] + 180
    if style["hook_style"] == "box":
        hook_line = (f"Style: Hook,{font},{style['hook_size']},{ass_color(style['box_text'])},{c['accent']},"
                     f"{ass_color(style['box_color'])},&H00000000,0,0,0,0,100,100,0,0,3,14,0,8,{ml},{mr},{hook_v},1")
    else:
        hook_line = (f"Style: Hook,{font},{style['hook_size']},{c['primary']},{c['accent']},{c['outline']},"
                     f"&H80000000,0,0,0,0,100,100,0,0,1,7,3,8,{ml},{mr},{hook_v},1")
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{hook_line}
Style: Caption,{font},{style['caption_size']},{c['primary']},{c['accent']},{c['outline']},&H80000000,0,0,0,0,100,100,0,0,1,6,2,2,{ml},{mr},{cap_v},1
Style: ClipText,{font},{style['text_size']},{c['primary']},{c['accent']},{c['outline']},&H80000000,0,0,0,0,100,100,0,0,1,5,2,8,{ml},{mr},{hook_v + 260},1
Style: End,{font},{style['hook_size']},{c['accent']},{c['primary']},{c['outline']},&H80000000,0,0,0,0,100,100,0,0,1,6,3,5,{ml},{mr},0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    pop = "{\\fscx85\\fscy85\\t(0,120,\\fscx100\\fscy100)}"
    lines = []
    hook = plan.get("hook")
    if hook and hook.get("text"):
        lines.append(f"Dialogue: 2,{ass_time(0)},{ass_time(hook.get('dur', 2.5))},Hook,,0,0,0,,"
                     f"{pop}{ass_escape(hook['text'])}")
    for start, clip in zip(clip_starts, plan["clips"]):
        if clip.get("text"):
            end = start[1]
            lines.append(f"Dialogue: 1,{ass_time(start[0])},{ass_time(end)},ClipText,,0,0,0,,"
                         f"{pop}{ass_escape(clip['text'])}")
    end_text = plan.get("end_text")
    if end_text and end_text.get("text"):
        d = end_text.get("dur", 2.0)
        lines.append(f"Dialogue: 2,{ass_time(total - d)},{ass_time(total)},End,,0,0,0,,"
                     f"{pop}{ass_escape(end_text['text'])}")
    # Word-by-word captions, current word highlighted in the accent color
    if plan.get("caption_case", "upper") == "upper":
        words = [{**w, "word": w["word"].upper()} for w in words]
    for chunk in chunk_words(words, plan.get("caption_words", 3)):
        for i, w in enumerate(chunk):
            end = chunk[i + 1]["start"] if i + 1 < len(chunk) else w["end"]
            text = " ".join(
                ("{\\c" + c["accent"] + "}" + ass_escape(x["word"].strip()) + "{\\c" + c["primary"] + "}")
                if j == i else ass_escape(x["word"].strip())
                for j, x in enumerate(chunk))
            lines.append(f"Dialogue: 0,{ass_time(w['start'])},{ass_time(end)},Caption,,0,0,0,,{text}")
    return header + "\n".join(lines) + "\n"


def chunk_words(words, max_words):
    chunk = []
    for w in words:
        if chunk and (len(chunk) >= max_words or w["start"] - chunk[-1]["end"] > 0.6
                      or chunk[-1]["word"].rstrip().endswith((".", "?", "!", ","))):
            yield chunk
            chunk = []
        chunk.append(w)
    if chunk:
        yield chunk


def transcribe(path, model_name):
    import whisper
    model = whisper.load_model(model_name)
    result = model.transcribe(path, word_timestamps=True, fp16=False, language="en")
    return [w for seg in result["segments"] for w in seg.get("words", [])]


def main():
    plan_path = sys.argv[1]
    with open(plan_path) as f:
        plan = json.load(f)
    fmt = plan.get("format", "reel")
    style = {**DEFAULT_STYLE, **plan.get("style", {})}
    output = plan["output"]
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="reel_")

    clips = plan["clips"]
    if plan.get("beats"):
        for clip, d in zip(clips, beat_durations(plan["beats"], len(clips))):
            speed = float(clip.get("speed", 1.0))
            if os.path.splitext(clip["src"])[1].lower() in IMAGE_EXT:
                clip["dur"] = d
            else:
                clip["out"] = float(clip.get("in", 0.0)) + d * speed

    parts, spans, t = [], [], 0.0
    for i, clip in enumerate(clips):
        path, dur = render_clip(clip, i, plan.get("fit", "crop"), tmp)
        parts.append(path)
        spans.append((t, t + dur))
        t += dur
    total = t

    listfile = os.path.join(tmp, "list.txt")
    with open(listfile, "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    joined = os.path.join(tmp, "joined.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", listfile, "-c", "copy", joined])

    words = []
    if plan.get("captions") == "auto":
        words = transcribe(joined, plan.get("whisper_model", "small"))
        with open(os.path.splitext(output)[0] + "_transcript.txt", "w") as f:
            f.write(" ".join(w["word"].strip() for w in words) + "\n")

    hooks = plan.get("hook_variants") or [plan.get("hook", {}).get("text")]
    outputs = []
    for n, hook_text in enumerate(hooks):
        variant = dict(plan)
        if hook_text:
            variant["hook"] = {**plan.get("hook", {}), "text": hook_text}
        ass_path = os.path.join(tmp, f"subs{n}.ass")
        with open(ass_path, "w") as f:
            f.write(build_ass(variant, style, fmt, spans, words, total))
        out = output if len(hooks) == 1 else output.replace(".mp4", f"_v{n + 1}.mp4")
        outputs += render_final(plan, joined, ass_path, out, total, fmt, tmp)

    cover_t = plan.get("cover", min(1.0, total / 2))
    cover = os.path.splitext(outputs[0])[0] + "_cover.jpg"
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{cover_t:.3f}", "-i", outputs[0],
         "-frames:v", "1", "-q:v", "2", cover])
    shutil.rmtree(tmp)
    for o in outputs:
        print(o)
    print(cover)


def render_final(plan, joined, ass_path, out, total, fmt, tmp):
    inputs = ["-i", joined]
    vf = f"[0:v]ass={ass_path}[v]"
    music = plan.get("music")
    if music:
        inputs += ["-ss", str(music.get("start", 0)), "-i", music["src"]]
        vol = music.get("volume", 0.35)
        af = (f"[1:a]volume={vol},atrim=0:{total:.3f},afade=t=out:st={max(0, total - 1.5):.3f}:d=1.5[m];"
              f"[0:a][m]amix=inputs=2:duration=first:normalize=0,")
    else:
        af = "[0:a]"
    af += "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]"
    audio = ["-map", "[a]", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
    if plan.get("mute_output"):
        audio = ["-an"]
    common = ["-filter_complex", f"{vf};{af}", "-map", "[v]", *audio, *X264,
              "-preset", "slow", "-crf", "18", "-maxrate", "25M", "-bufsize", "50M", "-r", "30"]

    if fmt == "story" and total > STORY_MAX_SEG:
        base = out.replace(".mp4", "")
        run(["ffmpeg", "-y", "-loglevel", "error", *inputs, *common,
             "-force_key_frames", "expr:gte(t,n_forced*1)",
             "-f", "segment", "-segment_time", str(STORY_MAX_SEG), "-reset_timestamps", "1",
             "-segment_format_options", "movflags=+faststart", f"{base}_part%02d.mp4"])
        count = int(total // STORY_MAX_SEG) + (1 if total % STORY_MAX_SEG else 0)
        return [f"{base}_part{i:02d}.mp4" for i in range(count) if os.path.exists(f"{base}_part{i:02d}.mp4")]
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, *common, "-movflags", "+faststart", out])
    return [out]


if __name__ == "__main__":
    main()
