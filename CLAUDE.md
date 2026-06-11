# GovCon Giants - Bootcamp Project

**Last Updated:** April 10, 2026
**Owner:** Eric Coffie
**Purpose:** Federal contracting bootcamp materials, marketing assets, and business tools

---

## Project Overview

This repository contains all GovCon Giants resources for helping small businesses win federal government contracts: bootcamp materials, hit lists, SBLO/contractor databases, email sequences, YouTube content, presentations, and AI/automation tools.

---

## Key Dates

- **Next Event:** April 25, 2026 (First Partner Challenge Bootcamp - FREE)
- **Past Bootcamp:** March 28, 2026 (Contract Vehicles Bootcamp - FREE)
- **Past Bootcamp:** February 28, 2026 (Specifics & Proposals)
- **Past Bootcamp:** January 31, 2026 (replay at `/jan-31-bootcamp-paid`)
- **FY2026 NDAA Signed:** December 18, 2025
- **Fiscal Year End:** September 30

---

## Directory Structure (High Level)

| Directory | Contents |
|-----------|----------|
| `email-templates/` | 10-email nurture + 4 recompete emails |
| `email-sequence-for-surge-downloads/` | 16-email bootcamp promo sequence |
| `general-member-sequence/` | 7-email general list sequence |
| `december-downloads-sequence/` | 7-email December leads sequence |
| `march-surge-email-sequence/` | 7-email March surge sequence |
| `funnels/` | Marketing funnels (opportunity-hunter, march-surge, etc.) |
| `funnels/march-surge/` | March 28 Contracting Launchpad Bootcamp funnel (landing, upsell, downsell, thank-you) |
| `march-surge-page/` | Static HTML deploy folder for March 28 (agenda, slides, hit-list, downloads) |
| `funnels/march-surge/downloads/` | 6 free resources (expiring contracts, IDIQ guides, templates) |
| `presentations/` | Bootcamp slides, TempNet, Veteran War Room |
| `webinar/` | Webinar materials and scripts |
| `files/` | Proposal bootcamp handouts (IDIQ guide, templates) |
| `govcon-resources/` | Deployed web resources |
| `govcon-tools/` | Web-based tools |
| `docs/` | Detailed documentation (see below) |
| `tasks/` | Todo tracking and lessons learned |

### Root File Patterns

- `january-hit-list-*.html` — Contract opportunity hit lists
- `january-*.html` — January bootcamp materials
- `february-28-surge-agenda.html` — February Surge agenda (Pro)
- `march-28-surge-agenda.html` — March agenda (original, links to funnels/march-surge/downloads/)
- `march-surge-page.html` — March landing page (original)
- `product-*.html` — Product/tool landing pages
- `youtube-live-*-slides.html` — 12 YouTube Live slide decks
- `tier1-batch-*.csv` / `tier2-batch-*.csv` — Contractor research batches
- `highlevel-kb-*.md` — AI chatbot knowledge base (30 topics)
- `*.py` — Data processing, scraping, and hit list scripts

---

## Detailed Documentation

For specifics, see these docs:

| Doc | Contents |
|-----|----------|
| [docs/bootcamps.md](docs/bootcamps.md) | All bootcamp events, presentations, handouts, webinars |
| [docs/youtube-lives.md](docs/youtube-lives.md) | 12 slide decks, scripts, thumbnails, content strategy |
| [docs/email-sequences.md](docs/email-sequences.md) | All 4 email sequences (40 emails total) |
| [docs/databases.md](docs/databases.md) | SBLO, Tier 1, Tier 2, contractor databases, KB, Python scripts |
| [docs/vault.md](docs/vault.md) | The Vault premium doc library — architecture, deployment, gotchas |
| [docs/govcon-funnels.md](docs/govcon-funnels.md) | Lead capture system, GHL/Slack integrations, funnel pages |
| [docs/govcon-shop.md](docs/govcon-shop.md) | E-commerce, Stripe webhooks, product emails |
| [docs/deployments.md](docs/deployments.md) | Domains, DNS, Vercel projects, Framer (legacy) |

---

## Related Projects

| Project | Path | URL | Framework |
|---------|------|-----|-----------|
| GovCon Funnels | `/Users/ericcoffie/Projects/govcon-funnels` | `govcongiants.com` | Next.js 16 |
| GovCon Shop | `/Users/ericcoffie/govcon-shop` | `shop.govcongiants.com` | Next.js 16 |
| The Vault | `/Users/ericcoffie/Projects/vault` | `govcongiants.com/vault` | Next.js 15 |

---

## The 8 Agency Pain Points

1. **End-of-Year Spending Urgency** — Q4 budget pressure
2. **Small Business Goals & Set-Asides** — 23% goal compliance
3. **Specialized Technical Expertise Gaps** — Niche skills shortage
4. **Legacy System Modernization** — IT/cloud migration
5. **Construction & Facilities Management** — Infrastructure backlogs
6. **Rapid Response & Emergency Needs** — Quick turnaround
7. **Supply Chain & Logistics** — Reliable suppliers
8. **R&D Innovation** — SBIR/STTR programs

---

## Key Agencies

DHS, DoD, DOE, DOT, GSA, DLA, VA, Space Force, FEMA, DARPA/MDA

---

## Common Commands

```bash
# Hit lists
python create-hit-list-from-csv.py
python auto-generate-hit-lists.py

# Database management
python compile-sblo-list.py
python update-database-vendor-portals.py
python create-tier2-priority-batches.py
```

---

## Data Sources

SAM.gov, USAspending.gov, FPDS, SBA Prime Directory, Agency strategic plans, GAO Reports

---

## Notes

- All HTML files are designed for PDF export
- CSV files use UTF-8 encoding
- Vendor portal URLs need quarterly verification
- Hit lists should be regenerated monthly with fresh SAM.gov data

---

## March 2026 Contract Vehicles Bootcamp

**Date:** March 28, 2026
**Time:** 9:00 AM ET | Live on Zoom
**Topic:** Contract Vehicles — IDIQs, GWACs, Qualifications & Team Building
**Format:** FREE, open to public
**Registration:** `govcongiants.com/contract-vehicles-bootcamp`
**April Bootcamp:** Winning with Certifications (Pro Members)

### Curriculum (6 Sessions) — Updated March 28, 2026

| Session | Time | Topic | Duration |
|---------|------|-------|----------|
| 1 | 9:00 AM | **Contract Vehicles 101** — The Big Picture (IDIQ, GWAC, BPA, GSA MAS) | 90 min |
| 2 | 10:45 AM | **Vehicles By YOUR Industry** — 8 industries, 40+ real IDIQs with names & values | 75 min |
| 3 | 12:45 PM | **Sources Sought & RFI Responses** — Get on radar before RFP | 60 min |
| 4 | 1:45 PM | **How to Qualify + Team Assembly** — Real requirement tear-downs, solopreneur gaps | 60 min |
| 5 | 3:00 PM | **Task Order Response Strategy** — Win work under IDIQs | 60 min |
| 6 | 4:00 PM | **ON vs. THROUGH Vehicles** — Strategic decision + subcontracting deep dive | 45 min |

Breaks: 10:30-10:45 AM, 12:00-12:45 PM (lunch), 2:45-3:00 PM, 4:45-4:50 PM
Closing Q&A: 4:50-5:00 PM

### Key Content Additions (March 28, 2026)
- **Industry-specific vehicles:** 6 IDIQs per industry (Construction, IT, Cyber, Professional Services, Healthcare, Logistics, Facilities, Training)
- **Breaking News slides:** FAR Overhaul, CIO-SP4 cancelled, OASIS+ rolling awards, SEWP VI protests (5 open), Alliant 3 (43 awards), Polaris WOSB (55 awards), EVOLVE ($10B)
- **Real requirement tear-downs:** OASIS+ and CIO-SP3 SB qualification requirements
- **Team assembly guide:** 4 ways solopreneurs fill capability gaps
- **Subcontracting deep dive:** Money reality (prime cuts), how to approach primes, red flags
- **AI use cases:** Specific prompts for vehicle research, teaming, qualification analysis
- **Email CTA banners:** 5 keywords (VEHICLES, PROMPTS, TEAM, SUBK, SOURCES)
- **Market Intelligence examples:** Daily Intel, Weekly Deep Dive, Pursuit Brief mockups

### Slides File
`presentations/march-28-bootcamp-slides.html` — 99 slides

### Deployments
- **Next.js funnel:** `govcongiants.com/contract-vehicles-bootcamp` (govcon-funnels)
  - Routes: `/march-surge/` (landing, upsell, downsell, thank-you)
- **Static HTML:** `march-surge-page.vercel.app` (Vercel project: march-surge-page)
  - Files: index.html, agenda.html, slides.html, hit-list.html, proposal-landing-page.html
  - 6 download files co-located in same folder

### Files Created
- `presentations/march-28-bootcamp-slides.html` — Main slide deck (99 slides)
- `presentations/March-28-Contract-Vehicles-Bootcamp.pdf` — PDF export (99 pages)
- `presentations/march-28-pngs/` — Individual slide images (99 PNGs)
- `march-surge-page/` — Static deploy folder (agenda, slides, hit-list, downloads)
- `funnels/march-surge/` — 4-page funnel (landing → upsell → downsell → thank-you)
- `funnels/march-surge/downloads/` — 6 free resources
- `march-surge-email-sequence/` — 7 emails
- `march-28-surge-agenda.html` — Original agenda (root, points to funnels/downloads)
- `march-surge-page.html` — Original landing page (root)

### Free Downloads
1. `march-2026-expiring-contracts.xlsx` — 944 real contracts
2. `recompete-positioning-checklist.pdf` — 12-18 month timeline
3. `10-idiq-vehicles-guide.pdf`
4. `active-idiq-vehicles-list.xlsx`
5. `sources-sought-response-template.docx`
6. `task-order-response-template.docx`

---

## April 2026 First Partner Challenge Bootcamp

**Date:** April 25, 2026
**Time:** 9:00 AM - 6:00 PM ET | Live on Zoom
**Topic:** Find Your First Teaming Partner or Consultant Client
**Format:** FREE, open to public
**Registration:** `govcongiants.com/first-partner-challenge`

### The 5 Objectives

1. **Pick Industry** — Max 2 NAICS codes, double niche down
2. **Find Sources Sought** — Use Market Assassin to find opportunities
3. **Build Call List** — 10-15 companies who can perform the work
4. **Make Calls** — LIVE calls during the bootcamp (Power Hours)
5. **Book Meetings** — Leave with 1-2 follow-up calls scheduled

### Curriculum (8 Sessions)

| Time | Session | Duration |
|------|---------|----------|
| 9:00 AM | **Welcome + The Strategy** — Solo vs Team, value exchange | 30 min |
| 9:30 AM | **Pick Your Industry** — NAICS selection workshop | 45 min |
| 10:30 AM | **Find Sources Sought** — Market Assassin live demo | 60 min |
| 11:30 AM | **Analyze Requirements** — What capabilities needed? | 30 min |
| 12:45 PM | **Build Call List** — Contractor Database workshop | 45 min |
| 1:30 PM | **The Pitch + Role Play** — Practice phone script | 45 min |
| 2:30 PM | **Power Hour #1** — LIVE CALLS (real companies) | 60 min |
| 3:30 PM | **Hot Seats** — What worked? Refine approach | 30 min |
| 4:00 PM | **Power Hour #2** — More calls, better pitch | 45 min |
| 5:00 PM | **Wins + Commitments** — Share results, next steps | 45 min |

Breaks: 10:15-10:30 AM, 12:00-12:45 PM (lunch), 2:15-2:30 PM, 4:45-5:00 PM

### Key Differentiator

**LIVE CALLS during the bootcamp** — Everyone makes real calls to real companies with accountability. Not homework — action.

### Tools Used

| Tool | Purpose |
|------|---------|
| **Market Assassin** | Find Sources Sought by NAICS |
| **Contractor Database** | Build call list of potential partners |
| **Federal Market Scanner** | Validate spending in industry |

### The Value Exchange

| What You Bring | What They Bring |
|----------------|-----------------|
| Market research (Sources Sought) | Experience performing work |
| Upfront BD work | Money/capital |
| Submission handling | Past performance |
| Possibly certifications | Estimating capability |

### Files Created

**Agenda & Slides**
- `april-25-first-partner-challenge-agenda.html` — Main agenda
- `presentations/april-25-first-partner-slides.html` — 57-slide deck
- `docs/first-partner-challenge-reference.md` — Challenge methodology reference

**Email Sequence** (`april-25-first-partner-challenge-email-sequence/`)
- 16 HTML emails: pre-event (8), day-of (1), post-event (7)
- Follows GovCon Giants email template styling

**Landing Page Funnel** (`funnels/first-partner-challenge/`)
- `index.html` — Redirect
- `1-landing.html` — Registration page (purple/indigo theme)
- `4-thank-you.html` — Confirmation with download links

**Free Handouts** (`funnels/first-partner-challenge/downloads/`)
- `call-list-template.csv` — Partner tracking spreadsheet
- `phone-script.html` — Word-for-word call script with objection handlers
- `teaming-agreement-template.html` — Formal teaming agreement template

**YT Lives Series** (`presentations/yt-lives/first-partner-challenge/`)
- `live-01-why-teaming-matters.html` — 12 slides
- `live-02-finding-partners.html` — 14 slides
- `live-03-the-first-call.html` — 16 slides
- `live-04-challenge-preview.html` — 14 slides
- `export-slides.js` — Puppeteer PNG export script

---

## Pending Tasks

- [x] Generate March 2026 expiring contracts data
- [x] Create March surge funnel and email sequence
- [x] Rename March event to "Contract Vehicles Bootcamp" (was "Recompete Contracts Surge")
- [x] Deploy march-surge-page static site to Vercel
- [x] Export slides to PDF (99 pages)
- [x] Add breaking news: Alliant 3, Polaris WOSB, EVOLVE, SEWP VI protests
- [x] Add Market Intelligence briefing examples (Daily, Weekly, Pursuit)
- [x] Update agenda files to match slide structure
- [x] Update march-surge-page.html with Contract Vehicles theme
- [x] Plan April First Partner Challenge curriculum
- [x] Create April bootcamp agenda HTML
- [x] Create April bootcamp slides (57 slides)
- [x] Create April email sequence (16 emails)
- [x] Create April landing page/funnel
- [x] Create April handouts (call list, phone script, teaming agreement)
- [x] Create April YT Lives series (4 promo videos)
- [ ] Assign custom domain to march-surge-page Vercel project
- [ ] Export April slides to PDF/PNG
- [ ] Update SBLO contacts (Q2 2026)
- [ ] Update expiring contracts data monthly
