# Connecting the Instagram API (publishing + view counts)

This gives Claude **token-based** access: no password, revocable anytime, and
it survives between sessions. It's how we measure progress toward the 1M-views goal.

**Requirements:** each account must be a **Professional** account (Business or Creator).
Verify each step against Meta's current docs as we set it up together. Meta
renames things often.

## Steps (about 20 minutes, done once)
1. Go to developers.facebook.com, log in as yourself, and click **Create App**. Choose the
   use case for managing Instagram content / "Instagram API with Instagram Login".
2. Add each Instagram account as a tester or connected account, and accept the
   invite inside Instagram (Settings → Website permissions / Apps).
3. Generate an access token per account with these permissions:
   `instagram_business_basic`, `instagram_business_content_publish`,
   `instagram_business_manage_insights`, `instagram_business_manage_comments`.
4. Exchange it for a **long-lived token** (about 60 days, refreshable). Claude can do
   this step once the short token is stored.
5. Store the tokens in **this cloud environment's settings**, not in chat and not in the repo:
   session title bar → environment → **Edit** → environment variables:
   - `IG_TOKEN_MBM`: @minibarnmarket
   - `IG_TOKEN_FG`: @farmhousegetaways
   - `IG_TOKEN_FFF`: @financialfreedomfarmgirl
6. Start a new session. Claude will confirm each token works (read-only call first).

## What this unlocks
- Pulling views, reach, shares, saves and follows per Reel and Story into `tracking/results.csv`
- Publishing or scheduling Reels and Stories, if you want that. Default: Claude
  prepares everything and you post, so you can add trending audio in-app.

## What it can't do
- Add songs from Instagram's music library (no API for that; add in the app).
- Stickers (polls, questions, links) on Stories: add these in the app.
- The API fetches videos from a public URL, so publishing also needs a place to
  host the final file (e.g., a Dropbox shared link).
