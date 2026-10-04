# Instagram Video Studio — Operating Manual

This repo is Claude's long-term memory for Carissa's Instagram video work.
Cloud sessions start from scratch, so **anything worth remembering must be written
here and pushed**. Read this file (and the latest `docs/handoff-*.md`), then the relevant `knowledge/` and
`accounts/<account>/brand.md` files, before starting any edit.

## Who I work for
Carissa, owner of Mini Barn Market. Short names she uses:
MBM = Mini Barn Market · RBR = Red Barn Ranch · MR = Mountain Retreat ·
IMM = Industrial Mini Mansion · FG = Farmhouse Getaways · FCF = Full Circle Farms.

## Accounts (one folder each under `accounts/`)
| Folder | Handle | Notes |
|---|---|---|
| `minibarnmarket` | [@minibarnmarket](https://www.instagram.com/minibarnmarket/) | MBM |
| `financialfreedomfarmgirl` | [@financialfreedomfarmgirl](https://www.instagram.com/financialfreedomfarmgirl) | |
| `farmhousegetaways` | [@farmhousegetaways](https://www.instagram.com/farmhousegetaways) | FG (RBR, MR, IMM properties?) |

Instagram blocks logged-out viewing, so Claude can't browse these profiles.
Style knowledge comes from what Carissa shares and from `brand.md`.

## Posting mix (Carissa's priority order)
1. **Stories**: the dominant format
2. **Reels**
3. **Trial Reels**
4. Feed posts

Stories mostly reach existing followers. Growth to non-followers comes from Reels
and Trial Reels, so every shoot should produce **both** a Story set and a Reel
cut from the same footage (see `knowledge/stories-strategy.md`).

## Goal (set 2026-09-27)
Daily videos for all three accounts; target **1M+ views within 2 weeks**.
Track results in `tracking/results.csv`. The plan is `plan/2026-10-14-day-plan.md`.

## Standing orders from Carissa (2026-09-27, indefinite)
1. **Listen to exactly what's asked.** Don't create content she hasn't requested.
2. **Ask questions** whenever there's a real chance of misinterpreting anything.
3. **Create videos on demand** when she uploads phone footage through the Claude app,
   using every tool and all the knowledge here to make "our masterpiece".
4. **Visual standard: a really crisp, HDR-quality look.** See `knowledge/look-and-grade.md`.

## "Finished" means built in Instagram (2026-10-04)
When Carissa asks for a carousel, Reel, Story or post, the job isn't done until it's **built inside
Instagram on the right account**: media uploaded and ordered, cropped, caption, hashtags, audio, AI label,
right up to the **Share** button. Then **stop and ask her** before tapping Share. Never post without her yes.
This needs a session that can control her logged-in browser: Claude Desktop with Claude in Chrome, the
built-in browser, or computer use. A cloud session can't, so say so and prepare everything else.

## How we work
1. Carissa uploads footage and describes what she wants.
2. Claude reviews the footage and flags anything that looks off (framing,
   lighting, shaky shots, weak hook, too long). Claude explains *why* and asks
   when style or wording is unclear. Otherwise Claude works on its own.
3. Claude edits end-to-end: hook, pacing, cuts on the beat, captions/text,
   safe zones, cover frame, export to spec.
4. Claude suggests audio (often 2–3 options, and delivers versions when that
   makes sense). **If Carissa names a specific song, that choice is final.**
5. Claude delivers the final video plus a post kit: caption, hashtags,
   cover-frame timestamp, audio to add in-app, best time to post.
6. After each project, record new style lessons in the account's `brand.md`
   (things she liked, changed, or rejected).

## Rules
- **Never state a fact about a business, property or Carissa's life that isn't confirmed** in that
  account's `brand.md` "Confirmed facts". This covers amenities, Wi-Fi, animals, availability,
  prices and numbers. If a line depends on one, ask first. Tone guesses are fine to suggest; facts aren't.
- **No Google Drive for handing over files** (Carissa, 2026-10-04). She uploads straight into the chat,
  5 at a time. (The Drive connector can't see stars and caps files at 10 MB.)
- **Don't make posts from old footage found in Drive unless Carissa asks.** Wait for
  fresh footage and her brief.
- **Every document for Carissa** (plans, strategy, research, hook/idea lists,
  documentation, business info) is also delivered as a **downloadable PDF**.
  Build it with `scripts/md_to_pdf.py` and send it with SendUserFile.
- Media files (video/audio/images) are **not** committed; they're too large
  for git. Commit project notes (`projects/<date>-<slug>/notes.md`) only.
- Export with `scripts/export_reel.sh` so every file meets the specs in
  `knowledge/instagram-specs.md`.
- Keep text inside the safe zone (see specs file).
- Refresh `knowledge/` whenever research finds newer info, and update its
  "last checked" date.

## Access & credentials
- Never commit passwords or tokens to this repo.
- Browser work on Instagram goes through Carissa's own logged-in browser
  (Claude in Chrome / the desktop app's built-in browser), not a scripted login.
- API tokens (publishing + Insights) live in the cloud environment's settings as
  `IG_TOKEN_MBM`, `IG_TOKEN_FG`, `IG_TOKEN_FFF`. See `docs/instagram-api-setup.md`.

## Tooling
- `scripts/make_reel.py plan.json`: the editing engine (Reels + Stories, captions,
  hook variants, beat-timed cuts, cover frame). Plan format: `scripts/PLAN_FORMAT.md`.
- `scripts/voiceover.py`: narration. Kokoro TTS voice lines timed per shot (default voice `af_heart`),
  or a recorded voice memo (`{"src": …}`). Captions follow the narration, using the exact script wording.
- **Voice clone (in progress):** Carissa wants her own voice cloned for narration. Plan: Chatterbox
  (open source, MIT license, runs here) from a 60–90s voice memo (`docs/voice-clone-recording-guide.md`).
  Upgrade to ElevenLabs if quality falls short. That needs `ELEVENLABS_API_KEY` in the environment settings.
  Only generate lines she has approved. Tell her to use Instagram's AI label on cloned-voice posts.
  **Voice sample storage (approved 2026-09-27):** Google Drive → `Claude Instagram Studio/Voice Sample (private)`
  (folder id `1UG2Y046QnQnS_bLrEUTDlPyS9ZqzBVWb`). Never commit it to git. Keep the file under 10 MB
  (the Drive connector's limit), so convert the memo to mono 24 kHz WAV/FLAC first.
  Pronunciation list: `accounts/pronunciations.md` (waiting on Carissa).
- `scripts/make_carousel.py plan.json`: carousel slides from photos. 4:5 (1080×1350) crops with per-slide focus,
  the same crisp grade as the videos, and an optional slide-1 hook.
- `scripts/export_reel.sh`: quick single-file conversion to spec.
- `scripts/fit_for_chat.sh`: the Claude app caps files at **30 MB**. Run this on any finished video
  over that and send the `_share.mp4` copy (still well above what Instagram keeps).
- `scripts/setup.sh` installs ffmpeg, Whisper (auto-captions), librosa (beat detection) and fonts. A SessionStart
hook in `.claude/settings.json` runs it automatically in cloud sessions.
