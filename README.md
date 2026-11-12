# Neelambari — a royal lapis & gold Indian wedding invitation

*Neelambari* — "woven of blue" — is an Indian wedding invitation
reimagined as **a Mughal palace at midnight**. The guest enters
through a lapis-silk farman envelope sealed in gold — its flap lined
with woven jaali — and walks the durbar: the names blazing in gold
script inside a grand cusped jharokha arch, the story set like a
gallery plaque with a giant chapter numeral, the date proclaimed on a
candlelit farman band, the celebrations strung along a sacred gold
thread, the palette presented as silk swatches, the festivities
hanging from a marigold garland, the mandapam in its courtyard, a
rotunda countdown beneath a turning moon-mandala, a fountain-pen reply
desk and a petal-shower farewell. Alternating lapis nights and moonlit
marble, joined by cusped jaali arcade bands; set in Italiana, Crimson
Pro, Parisienne and Jost. No site chrome — it is the palace itself.
Fully customisable in the browser with a guided, auto-saving visual
editor — then published live with one click on Cloudflare.

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
