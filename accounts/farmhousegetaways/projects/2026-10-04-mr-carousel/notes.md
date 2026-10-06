# Mountain Retreat Carousel: Post Kit (Oct 4, 2026)

**Account:** @farmhousegetaways · **Format:** feed carousel, 10 slides, 4:5 (1080×1350)
**Images:** your 10 picks, in your upload order, cropped to 4:5 with the house crisp grade.
Hook on slide 1 only.

| # | Slide |
|---|---|
| 1 | Aerial at dusk. Hook: "Sleeps 14. Eight acres. Disc golf and a pub-style arcade." |
| 2 | Disc golf basket under the string lights |
| 3 | Golden-hour basket under the oak |
| 4 | Wooden bridge and stone path |
| 5 | Basket below the granite hilltop |
| 6 | Basket with the bridge behind it |
| 7 | Blacklight arcade wall |
| 8 | Lit bridge at night |
| 9 | Game room lounge |
| 10 | Game room arcade: air hockey, foosball, cabinets |

## Caption
> Sleeps 14 on eight acres at the foot of Iron Mountain 🏔️
>
> Mountain Retreat in Ramona, CA: 4 bedrooms, 3 baths, hiking trails, a horseshoe pit,
> a pub-style arcade… and Boulder Oak, a private 3-hole disc golf course just for guests 🥏
>
> Tag the crew you'd bring 👇
> Details & dates: farmhousegetaways.com/mountain-retreat
>
> #ramonaca #discgolf #vacationrental #sandiegogetaway #groupgetaway

## Other hooks for slide 1 (I can swap any of these in)
- "Your group's next getaway comes with its own disc golf course."
- "8 acres. 14 guests. 1 private disc golf course."
- "Disc golf by day. Arcade by night."

## When posting
- **Audio:** carousels can have music. Add a calm, warm instrumental in-app.
- **AI label:** these images are AI-enhanced, so turn on Instagram's **AI info** label when posting.
- **First comment:** pin "Which slide sold you? 1–10 👇" to get comments going.
- **Story:** share the post to Stories with a link sticker to the Mountain Retreat page.

## Facts used (all confirmed on boulderoakdiscgolf.com)
Ramona CA · sleeps 14 · 4 bd / 3 ba · 8 acres · foot of Iron Mountain · hiking trails · horseshoe pit ·
pub-style arcade · Boulder Oak private 3-hole course for guests.
The hot tub and fire pit show in slide 1. Want them in the caption too?

---

## Video version (Reel + Story), 17s, silent for in-app music
Hook: "This getaway comes with its own disc golf course" · day-to-night flow: aerial → disc golf
in golden hour → string lights at dusk → lit bridge → arcade → game room · end card
"Mountain Retreat · Ramona, CA · Sleeps 14". Wide photos glide across the vertical frame.
**Reel caption:** reuse the carousel caption. **Sound:** a warm, upbeat acoustic or lo-fi track, added in-app.
Use the AI info label (AI-enhanced images).

## V2: 14 slides, built in Instagram (Oct 4, Desktop session)
- The chat copies of the 10 slides were never saved, so the slides were rebuilt locally from the originals
  in `Downloads/MR carousel` with `plan_carousel_v2.json`. Output: `Downloads/MR carousel/slides_V2/`.
- Slides 7–11 are new: Boulder Oak site hero, the three hole signs, the course map (course guide page 1),
  and two scorecard phone screenshots (hole 1 in play, final "Tied at 9"). These use `"grade": "none"`.
  Phone screenshots sit on an edge-matched dark background instead of being cropped.
- The original slide 7 (blacklight arcade) wasn't on the Desktop PC, so it's left out. `MR_FirePit_V1.png` is in
  the folder but was never in the plan, so it isn't used either.
- Built on @farmhousegetaways in Chrome: 4:5 crop, caption pasted exactly, AI label on. Stopped at Share.
  Desktop web has no music option for photo carousels, so music has to be added in the phone app.
- Local rebuild on Windows needs ffmpeg (`pip install imageio-ffmpeg`) and Montserrat ExtraBold. Override
  `make_carousel.FONT` instead of editing the Linux path in the script.

## V3: 12 slides (Oct 4, Cory)
- Cory removed V2 slides 8 (three hole signs) and 11 (final "Tied at 9" scorecard). Plan: `plan_carousel_v3.json`.
  Slides: `Downloads/MR carousel/slides_V3/`. Review PDF: `MR_Carousel_Review_V2.pdf`.
- Removed in the open Instagram composer too. Caption and AI label carried over. Still stopped at Share, on hold for Carissa.

## V4: 9 slides (Oct 4, Cory)
- Cory removed V3 slides 6 (basket with bridge), 9 (hole 1 scorecard) and 10 (lit bridge at night). Plan: `plan_carousel_v4.json`.
- The course map slide was re-rendered from boulderoakdiscgolf `print/course-guide.html?page=1` at commit 905c18c, so it says
  GAME ROOM, not GARAGE. Never call MR's second building a garage.
- Slides: `Downloads/MR carousel/slides_V4/`. Review PDF: `MR_Carousel_Review_V3.pdf`. Rebuilt in a fresh Instagram tab, stopped at Share.

## V5: words on the photos, aimed at OC & LA disc golfers (Oct 4, Cory)
- Cory: the carousel should attract disc golfers from Orange and LA counties to come stay and play. They're likely solo.
  Words go on most images, but not the Boulder Oak web page. The course map got none either, since it's already text-heavy.
- Slide words: 1 "OC & LA disc golfers: stay and play in Ramona" · 2 "A private disc golf course, just for guests" ·
  3 "Play it as many times as you like" · 4 "Three holes among the granite and the oaks" · 5 "3 holes · par 9 · 740 ft" ·
  8 "Then unwind in the game room" · 9 "The 19th hole: a pub-style arcade".
- New caption in `caption_v5.txt`. It uses Cory's sleeping line (4 bedrooms, 6 beds, 2 pullout couches) in place of "sleeps 14".
- Review PDF `MR_Carousel_Review_V3.pdf`. Rebuilt in Instagram, stopped at Share. Threads cross-post off (caption > 500 chars).

## File location (Oct 4)
All carousel files moved from `Downloads/MR carousel` to `Z:/Farmhouse Getaways/1. Marketing/0. Social Media 2.0/3. Social Media/` (current slides in `MR Carousel/`, older sets in `Archived/MR Carousel/`). Earlier `Downloads/...` paths in these notes are stale.

## V6–V8: Cory's own slide words (Oct 4)
- Cory wrote the text and order himself. V6 was the first build, V7 changed slide 3 to "The 19th hole: …", and V8 moved
  "Night play unlocked" to slide 5. Plan: `plan_carousel_v8.json`. Slides: Z: `MR Carousel/slides_V8/`.
- Numbered lists in chat were hard for Cory to write. The lettered picture key (`MR_Carousel_Picture_Key_V1.jpg`, A–N) is the way
  to ask for slide orders now: "letter: text", one per line, in order.
- Built in Instagram, stopped at Share, AI label on. Threads cross-post still off (caption 522 chars).

## V9: 8 slides (Oct 4, Cory)
Dropped the lounge and the bridge ("Experience Mountain Retreat…"). The lounge's NES/Xbox line moved onto the arcade slide,
and slide 2 now ends "…at the base of Iron Mountain". Plan `plan_carousel_v9.json`, slides on Z: `MR Carousel/slides_V9/`,
review PDF `MR_Carousel_Review_V5.pdf`. Rebuilt in Instagram, stopped at Share.

## V10 (Oct 4, Cory)
Slide 6 now reads "Adventure and play right out the back door." Plan `plan_carousel_v10.json`, slides Z: `MR Carousel/slides_V10/`, review `MR_Carousel_Review_V6.pdf`. Rebuilt in Instagram, stopped at Share.

## V11 (Oct 4, Cory)
Slide 8's text moved to the center of the image (new `"position": "center"` in make_carousel.py). Plan `plan_carousel_v11.json`, slides Z: `MR Carousel/slides_V11/`, review `MR_Carousel_Review_V7.pdf`. Only slide 8 was swapped in the open Instagram composer.

## V12 (Oct 5, Cory)
Slide 3 now opens "Boulder Oak Arcade:" instead of "The 19th hole:". Plan `plan_carousel_v12.json`, slides Z: `MR Carousel/slides_V12/`, review `MR_Carousel_Review_V8.pdf`. Rebuilt in Instagram, stopped at Share.

## Demo Reel with licensed music (Oct 5)
- Built from the V12 slides: each 4:5 slide centered on a blurred 9:16 copy of itself, slow zoom, 0.5s crossfades,
  2.8s per slide, 18.9s total. Music: Adobe Stock "Acoustic Dream" by Alex Saym (asset 511566980, a FREE Adobe Stock
  track, licensed on Cory's Adobe login), loudness-normalised to -14 LUFS, faded out at the end.
- Files: Z: `MR Carousel/Reel/MR_Reel_demo_V1.mp4` (full) and `_share.mp4` (chat-size). Not posted.
- Motion Array: the logged-in account has NO active subscription (download asks to subscribe). Adobe Stock free audio works.
- Instagram's own song library can't be added from outside the app, so licensed music baked into a Reel is the only
  fully automatic way to post with music.

## V13 + Reel V2 (Oct 6, Cory)
Slide words now: 1 "Check out this Disc Golf Vacation Rental in San Diego" · 2 "A private course on a beautiful 8-acre property
at the base of Iron Mountain" · 3 "It also has a private 700 sq ft arcade." · 4 "Night play unlocked." · 5 "Exclusive to guests of
Mountain Retreat" · 6 "Adventure and play right out the back door." · 7 "Keep score with our app, or enter it on UDisc." ·
8 "Iron Mountain and Mount Woodson trails are 3 miles away." Plan `plan_carousel_v13.json` (non-breaking spaces keep
"Disc Golf", "San Diego" and "700 sq ft" on one line; make_carousel now splits on plain spaces only).
Reel V2 = same slides + Adobe "Acoustic Dream". Both queued as drafts (no time) on farmhouse-admin's Publish tab.
Phone copies in Downloads/MR Carousel for iPhone. The Z: share was offline at the time; copy slides_V13 + Reel V2 there later.
