# Neelambari — a royal lapis & gold Indian wedding invitation

*Neelambari* — "woven of blue" — is an elegant Indian wedding card
reimagined as **royal lapis stationery**: moonlit-marble grounds and
deep lapis night bands trimmed in antique gold hairlines, a wax-sealed
silk envelope that opens into the invitation, and the same gracious
centred grid throughout — the shloka, "With the divine blessings of
our families", the names in Pinyon Script, an ornamental date row with
foil numerals, the muhurat, the venue and "Your presence will make
our day complete". Below: their story as a centred letter, the
save-the-date plate, the six celebrations as a printed itinerary, the
palette, the garland of festivities, the kalyana mandapam, the
countdown beneath the mandala, the reply card, and a closing note
sealed with the couple's monogram. No site chrome — it reads as the
card itself. Elegant serif headings with script accents and
letter-spaced labels. Fully customisable in the browser with a
guided, auto-saving visual editor — then published live with one
click on Cloudflare.

**Live template pieces**

| Piece | Where |
| --- | --- |
| Guest invitation (envelope opening + ten scenes + RSVP) | `index.html` |
| Visual editor ("Invitation Atelier") | `customize.html` |
| Guest submissions page | `replies.html` |
| Static assets + D1 API | `worker.js`, `functions/` |
| Sample content & copy | `js/config.js` |

## Stack

- **Cloudflare Workers** — static assets (`dist/`) + a small JSON API
- **Cloudflare D1** — stores published invitations and guest replies
  (this repo shares the `kalyanam-invitations` database of the
  [kalyanam-invitation](https://github.com/iftikhar565765/kalyanam-invitation)
  template; invitations and RSVPs are keyed per invitation id, so the
  two sites never collide)
- **No build framework** — vanilla HTML/CSS/JS; `scripts/build.mjs`
  copies source into `dist/` and cache-busts asset URLs with content
  hashes, and stamps every page with the build version
- GSAP (CDN) for the envelope choreography — everything degrades
  gracefully without it
- Every ornament is a pure inline SVG with explicit fills — no
  `<use>`, no shadow-DOM surprises

## Quick start (local)

```bash
npm install
npx wrangler d1 migrations apply kalyanam-invitations --local
npm run build
npx wrangler dev            # http://localhost:8788
```

The invitation runs in honest demonstration mode until published:
RSVPs validate and preview but are not stored. Deploy with a D1
database (see `DEPLOY.md`) and everything — the atelier, publishing,
guest replies, the submissions page — goes live.

## Deploying to Cloudflare

`DEPLOY.md` walks through it step by step (dashboard path and CLI
path). `wrangler.jsonc` already points at a live D1 database, so the
shortest path is simply:

```bash
npm run build && npx wrangler deploy
```

which publishes the site as its own worker at
`https://neelambari-invitation.<your-subdomain>.workers.dev`.
