# Mindy Day — Demo Deck Build Spec

**Built:** `mindy-demo-deck.html` (17 slides, 1280×720) · `Mindy-Demo-Deck.pdf` · `png/slide-01..17.png`
**Audience:** Federal contractors. NON-technical. "Bad at computers and worse at government contracts."
**Presenter:** Eric, live.

---

## Structure — three acts

| Act | Slides | What happens |
|---|---|---|
| **1 — The Map** | 3–7 | All the map features. Live demo of the Opportunity Map. |
| **2 — How It Works** | 8–11 | Mindy inside the AI tools you already use. Live demo in Claude, then ChatGPT. |
| **3 — Install It** | 12–16 | **Everyone installs it on their own machine, together.** |
| Close | 17 | The habit: *"The first place you look, every morning."* |

Slide 2 sets the expectation up front: *"You're leaving with it working — not with notes."*

---

## Hard rule for this audience

**Never put "MCP," "API," "endpoint," "server," or "token" on a slide as a concept.**
The only permitted occurrence is inside the address people must paste
(`https://mcp.getmindy.ai/mcp`) — never as a label or an explanation. Verified: 4 occurrences,
all inside that URL.

Framing is always the benefit: **"Mindy works inside the AI tools you already use."**

---

## Act 3 — the installation (the part that must not go wrong)

**Address everyone pastes:** `https://mcp.getmindy.ai/mcp` (verified live, returns 401 unauthenticated — correct)

**Prerequisite slide first:** a free Mindy account at `getmindy.ai`. That is what they sign into
at the end, and not having one is the most likely stall.

**Claude — 4 steps** (verified against the live /mcp page):
1. Settings → Connectors
2. Add custom connector
3. Paste the address
4. Connect → sign in with Mindy → Allow

**ChatGPT — 4 steps, more hidden:**
1. Settings → turn on **Developer mode** ← *nothing appears until this is on*
2. Plugins
3. Add manually → paste the same address
4. Sign in with your Mindy account → approve access

**Both end with authentication.** That is the step everyone misses; the slide says so explicitly.

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

## Numbers — verified live 2026-08-21

| Figure | Value | Note |
|---|---|---|
| Open opportunities | **15,085** | future response deadline — the strictest, checkable reading |
| Posted per weekday | **~2,000** | 1,229 today; ~2,000–2,165 prior weekdays |
| Things Mindy can look up | **54** | from `docs/mcp-tool-catalog.json` |

**"88,000+" was removed** — it matched no current query and overstated the open count ~6×.
Never hardcode a corpus number; see `market-assassin/src/lib/marketing-stats.ts`.

---

## Morning-of checklist

- [ ] Pre-test **both** demo prompts. Keep the notice number and category ready to **paste**, not type.
- [ ] Have a free Mindy account made on the demo machine.
- [ ] Have both Claude and ChatGPT already signed in and ready to screen-share.
- [ ] Copy `https://mcp.getmindy.ai/mcp` once and leave it somewhere you can re-copy fast.
