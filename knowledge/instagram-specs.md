# Instagram Video Specs

_Last checked: 2026-09-27. Instagram changes these often, so re-verify every few months._

## Reels (the main format)
| Spec | Value |
|---|---|
| Aspect ratio | **9:16** (only ratio that fills the screen) |
| Resolution | **1080×1920** (min 720p; Instagram serves up to 1080p) |
| Container / codec | MP4, H.264 video, AAC audio |
| Frame rate | 30 fps standard (23.976–60 accepted; keep the source rate if 24/25/60) |
| Pixel format | yuv420p, 8-bit SDR (HDR/10-bit iPhone footage gets washed out, so convert it) |
| Audio | AAC, 48 kHz, stereo, 192 kbps+; loudness around −14 LUFS |
| Max length | Up to 20 min can be uploaded, but **Reels over 3 min aren't recommended to non-followers** |
| Max file size | 4 GB |
| Cover | 1080×1920; profile grid shows a **3:4 center crop (1080×1440)** |

**Length for reach:** 7–15s for loops and trends, 15–45s for tips and tours, 60–90s
only for story-driven content that holds attention.

## Safe zones (1080×1920 canvas)
Instagram's interface covers parts of the frame. Keep text and faces out of:
- **Top ~220 px**: header and "Reels" label
- **Bottom ~420 px**: caption, audio label, username
- **Right ~140 px**: like/comment/share buttons
- **Stories** have different overlays: keep clear of the **top ~250 px**
  (progress bar, profile name) and **bottom ~340 px** (reply bar / link sticker).
  Leave room in the middle-lower third for poll/question/link stickers added in-app.
- For the 3:4 grid crop, keep the key cover content in the **middle 1440 px**.

## Other placements
| Placement | Ratio | Resolution | Notes |
|---|---|---|---|
| Stories | 9:16 | 1080×1920 | Clips over 60s get split into segments |
| Feed video / carousel | 4:5 (best), 1:1 | 1080×1350 / 1080×1080 | Carousel: up to 20 slides |
| Landscape | 1.91:1 / 16:9 | 1080×566 / 1920×1080 | Avoid: tiny on phones |

## Sources
- https://riverside.com/blog/instagram-reels-dimensions
- https://influencermarketinghub.com/instagram-video-size/
- https://postfa.st/sizes/instagram/reels
