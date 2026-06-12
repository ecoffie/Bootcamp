# Lessons Learned

## Bootcamp Duration Standard (March 2026)

**Mistake**: Created March Surge as a 4-hour event instead of the standard 8-hour bootcamp format.

**Pattern**: ALL bootcamps are 8 hours with lunch and breaks:
- **Time**: 9:00 AM - 5:00 PM Eastern
- **Duration**: 8 hours
- **Break 1**: 10:45 AM - 11:00 AM (15 min)
- **Lunch**: 12:30 PM - 1:15 PM (45 min)
- **Break 2**: 2:15 PM - 2:30 PM (15 min)
- **Break 3**: 4:30 PM - 4:45 PM (15 min)

**Rule**: When creating new bootcamp/surge events, default to 8-hour format. Reference `january-31-bootcamp-agenda.html` for the standard structure.

---

## Color/Styling Consistency (March 2026)

**Mistake**: Created March Surge agenda with custom green colors instead of matching existing bootcamp style.

**Pattern**: When creating new event pages (bootcamps, surges, agendas), ALWAYS use the January bootcamp color scheme as the default:
- Body background: `#1e3a8a` → `#7c3aed` (blue to purple)
- Header: `#059669` → `#10b981` (emerald green)
- Time color: `#7c3aed` (purple)
- Session titles: `#1e3a8a` (dark blue)
- Bullets: `#10b981` (emerald)
- Deliverables box: `#1e3a8a` → `#7c3aed` (blue to purple)
- CTA button: `#7c3aed` → `#a855f7` (purple gradient)

**Rule**: Before creating new styled HTML pages, check `january-31-bootcamp-agenda.html` for the canonical color scheme. Don't invent new color schemes unless explicitly requested.

**Reference Files**:
- `/Users/ericcoffie/Bootcamp/january-31-bootcamp-agenda.html` (canonical style)
- `/Users/ericcoffie/Bootcamp/february-28-surge-agenda.html` (purple variant for paid events)

---

## Mindy Launch + Supabase scaling (June 2026)

**Domain: .com only.** govcongiants.org / tools.govcongiants.org are retired. Never use .org in any new asset. Always cite **317K** for the contractor database (BigQuery recipients universe) — never the 2.7K SEO-page count or the old "500K" copy.

**Clean event URL on a Next.js site for a static funnel:** use a `rewrite` (not a `redirect`) in govcon-funnels `next.config.ts` so the address bar stays on `govcongiants.com/...`. A redirect bounces the visitor to the ugly `funnels-one.vercel.app` URL. Rewrite = proxy, URL stays put. (Form posts to relative `/api/lead` → the *main site's* handler, which must exist + accept the same fields.)

**Static funnel `/folder/` must serve the real page, not a stub.** The 241-byte `index.html` meta-refresh stub caused a clunky double-hop / "looks stale" perception. Make `index.html` a copy of the full landing page.

**Vimeo embeds:** (1) videos need the embedding domain on Vimeo's Privacy allowlist or they show "We couldn't verify the security of your connection." (2) Headless/Puppeteer checks show blocked even when real browsers play — can't verify playback via automation, only layout. (3) Match the card aspect ratio to the video: vertical reels = portrait 9:16 (`padding-bottom:177.78%`), not 16:9.

**Lead capture should never be single-point-of-failure.** GHL-only meant a failed GHL call = lost lead. Added a non-blocking Supabase `funnel_leads` backup (parallel with GHL via `Promise.all`); if env missing or write fails, log + continue. Verified end-to-end by POSTing a test lead then checking the DB row, then deleting it.

**Supabase "exhausting resources" alert = undersized compute, not code.** Micro tier (1GB RAM) sits at ~60% baseline memory before any work. Real fix = bump the tier (Micro→Small/2GB). Then reduce load with *additive* changes that don't remove features (the goal was scaling to 100K free users): pg_trgm GIN indexes for `ilike '%...%'` searches (leading wildcard can't use btree), btree on ordered columns, and `select('*')`→explicit columns to avoid pulling wide JSONB (raw_data ~50KB/row) into memory. Left the risky/feature-affecting items (count:exact→estimated, cron refactors) for a separate tested pass.

**CREATE INDEX CONCURRENTLY can't run in the Supabase SQL editor** (it wraps in a transaction). Either run statements one at a time, or drop CONCURRENTLY and accept a brief write-lock during build (fine in low traffic).
