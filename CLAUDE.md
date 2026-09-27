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
- Media files (video/audio/images) are **not** committed; they're too large
  for git. Commit project notes (`projects/<date>-<slug>/notes.md`) only.
- Export with `scripts/export_reel.sh` so every file meets the specs in
  `knowledge/instagram-specs.md`.
- Keep text inside the safe zone (see specs file).
- Refresh `knowledge/` whenever research finds newer info, and update its
  "last checked" date.

## Tooling
`scripts/setup.sh` installs ffmpeg and Whisper (auto-captions). A SessionStart
hook in `.claude/settings.json` runs it automatically in cloud sessions.
