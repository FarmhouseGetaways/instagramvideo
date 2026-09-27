# The House Look: Crisp, Vivid "HDR Style"

_Chosen by Carissa on 2026-09-27: the crisp, vivid HDR **look**, graded for standard (SDR) output
so it looks the same on every phone. Not true-HDR playback._

## What the engine does (`"grade": "crisp"`, the default in `make_reel.py`)
1. **iPhone HDR → SDR tone-map** so nothing looks washed out on Instagram.
2. **Light denoise** so sharpening doesn't amplify phone grain.
3. **HDR-style tone curve:** lifts shadows, rolls off highlights (keeps skies and windows from blowing out).
4. **Color:** +12% saturation plus vibrance (boosts muted colors more than already-bright ones,
   so skin tones stay natural).
5. **Clarity:** local-contrast boost that gives the "HDR pop".
6. **Fine sharpening** after Lanczos scaling for crisp detail.

Use `"grade": "none"` on a clip or plan to skip it (e.g., footage that's already been edited).

## How to film for the crispest result (iPhone)
- **Settings → Camera → Record Video: 4K at 30 fps** (or 60 fps for slow-motion moments).
- **HDR Video can stay ON.** I convert it properly.
- **Wipe the lens** before every shoot. A smudged lens is the #1 cause of soft, hazy footage.
- **Light:** face the light source. Golden hour and bright shade look best, and harsh noon sun is hardest.
- **Lock exposure and focus:** tap and hold on the subject until "AE/AF LOCK" appears.
- **No digital zoom.** Walk closer, or use the 0.5×/1×/2×/3× lens buttons only.
- **Hold each shot 3–6 seconds** and move slowly. Smooth, slow movement looks expensive.
- **Shoot vertical** unless it's drone footage.
- **Send the original files.** Screen recordings or re-saved copies lose quality.
