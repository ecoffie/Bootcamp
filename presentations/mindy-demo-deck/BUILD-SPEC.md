# Mindy Day — Demo Deck Build Spec

**Built:** `mindy-demo-deck.html` (28 slides, 1280×720) · `Mindy-Demo-Deck.pdf` · `png/slide-01..28.png`
**Audience:** Federal contractors. NON-technical. "Bad at computers and worse at government contracts."
**Presenter:** Eric, live.

---

## Structure — three acts

| Act | Slides | What happens |
|---|---|---|
| **1 — The Map** | 4–11 | Coverage, map totals, live Opportunity Map demo |
| **2 — How It Works** | 12–21 | Mindy inside Claude and ChatGPT. Live demo in both. |
| **3 — Install It** | 22–27 | **Everyone installs it on their own machine, together.** |
| Close | 28 | The habit: *"The first place you look, every morning."* |

Slide 3 sets the expectation up front: *"You're leaving with it working — not with notes."*

---

## Hard rule for this audience

**Never put "MCP," "API," "endpoint," "server," or "token" on a slide as a concept.**
The only permitted occurrence is inside the address people must paste
(`https://mcp.getmindy.ai/mcp`) — never as a label or an explanation.

Framing is always the benefit: **"Mindy works inside the AI tools you already use."**

---

## Act 3 — the installation (the part that must not go wrong)

**Address:** `https://mcp.getmindy.ai/mcp` (verified live, returns 401 unauthenticated — correct)

**Claude is directory-first.** Paste the URL only if Mindy is missing from the connector directory.

**Claude (matches `getmindy.ai/mcp/setup`):**
1. Settings → Connectors (under Customize)
2. Add → Browse connectors, search **mindy**
3. Click the orange **Connect to Claude** button
4. Make a free Mindy account → Allow
5. Set Read-only tools to **Always allow**

Fallback if it is not in the directory: Add custom connector → paste `https://mcp.getmindy.ai/mcp`.

**ChatGPT (matches `getmindy.ai/mcp/setup`):**
1. Settings → **Security and login** → turn on **Developer mode** (elevated-risk warning is ChatGPT's standard notice)
2. Plugins → click **+**
3. Name it **Mindy**, paste the address, Authentication **OAuth**, Create
4. **Sign in with Mindy** → free account
5. **Allow low-risk actions**

**Both end with a Mindy sign-in.** That is the step everyone misses; the slide says so explicitly.

**Then a proof slide:** they type a real question and confirm they get an answer, plus a
troubleshooting card (developer mode still off · restart Claude · finish the sign-in).

---

## Design system

- Dark throughout. Background `#0A0A0F`, card fill `#15161F`.
- Title/demo/close: dual radial glow. Content: single teal glow.
- Palette: teal `#1BB6A0` · mint `#02C39A` · yellow `#FFC845` · white · muted `#AEB4C2` · dim `#7C8290`
- Fonts: Arial/Helvetica — opens clean on any machine in the room.
- Act label top-right on content slides so the room always knows where they are.
- Map-pin dots on title/demo/close only.

---

## Numbers — measured 2026-08-26

Public copy uses **distinct canonical listings** (`solicitation_number`, else `notice_id`), not raw `sam_opportunities` rows. Do not cite `OPPORTUNITY_COUNT = 178_000` as unique opportunities.

| Figure | Public floor | Definition |
|---|---|---|
| Tracked SAM listings | **124,000+** | Distinct canonical listings in `sam_opportunities` (124,944 measured) |
| Open SAM listings | **10,000+** | Distinct listings with `active=true` and `response_deadline > now` (10,972 measured) |
| Typical weekday new listings | **~2,000** | Distinct listings by `posted_date` on complete weekdays (median 1,956). Not “2,000 more”; listings also close. |
| Mapped records | **164,000+** | Sum of map headlines: open pinned listings + recompetes in PoP + DIBBS + pinned forecasts (164,205) |
| Open and pinned | **3,600+** | Unique open SAM listings with coordinates (map `totalForFilters` 3,601) |
| Recompetes on the map | **113,000+** | Map default: mapped, `quality_flag` null, PoP not expired (113,654) |
| DIBBS RFQs on the map | **28,000+** | `dibbs_rfqs` with coordinates (28,202) |
| Forecasts on the map | **18,000+** | `agency_forecasts` with coordinates (18,748). Table holds 33,334. |
| MCP tools | **54** | Live `GET https://getmindy.ai/api/mcp/catalog` |
| Podcast episodes | **743** | Distinct `mindy_rag_documents` `podcast_interview` `source_path` values |
| Signup credits | **100** | Default `SIGNUP_CREDITS` / live catalog |
| Referral | **100 each, cap 25** | `REFERRAL_CREDITS` / `REFERRAL_CAP`; pays on verified sign-in |

Do not restore the retired row-count opportunity figure, the two conflicting open counts, the old pin-total shorthand, the expired recompete pin count, or DoD-wide bidder percentages. Those failed the August 26 fact-check.

---

## Navy pursuit story (slides 15–18)

Public slides keep the story. Internal only:

**VERIFY before reuse: the dollar amounts, record counts, dates, question count, requirement count, speed discrepancy, and Navy response are Eric’s pursuit anecdote and were not independently remeasured in the August 26 fact-check.**

Do not put that note on a public slide.

---

## Morning-of checklist

- [ ] Pre-test **both** demo prompts. Keep the notice number and category ready to **paste**, not type.
- [ ] Have a free Mindy account made on the demo machine.
- [ ] Have both Claude and ChatGPT already signed in and ready to screen-share.
- [ ] Copy `https://mcp.getmindy.ai/mcp` once and leave it somewhere you can re-copy fast.
- [ ] Pick a named buyer for the live bidder-count / one-bid / set-aside demo (slide 10). Do not quote DoD-wide percentages.
