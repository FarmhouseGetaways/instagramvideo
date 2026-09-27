# Instagram Video Studio — Operating Manual

This repo is Claude's long-term memory for Carissa's Instagram video work.
Cloud sessions start from scratch, so **anything worth remembering must be written
here and pushed**. Read this file, then the relevant `knowledge/` and
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
- `scripts/export_reel.sh`: quick single-file conversion to spec.
- `scripts/setup.sh` installs ffmpeg, Whisper (auto-captions), librosa (beat detection) and fonts. A SessionStart
hook in `.claude/settings.json` runs it automatically in cloud sessions.
