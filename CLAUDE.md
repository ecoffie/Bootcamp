# GovCon Giants - Bootcamp Project

**Last Updated:** March 9, 2026
**Owner:** Eric Coffie
**Purpose:** Federal contracting bootcamp materials, marketing assets, and business tools

---

## Project Overview

This repository contains all GovCon Giants resources for helping small businesses win federal government contracts: bootcamp materials, hit lists, SBLO/contractor databases, email sequences, YouTube content, presentations, and AI/automation tools.

---

## Key Dates

- **Next Event:** March 28, 2026 (Recompete Contracts Surge - FREE)
- **April Bootcamp:** Winning with Certifications (Pro Members)
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
| `funnels/march-surge/` | March 28 Recompete Surge funnel (landing, upsell, downsell, thank-you) |
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
- `march-28-surge-agenda.html` — March Surge agenda (FREE, with download links)
- `march-surge-page.html` — March Surge landing page
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
| GovCon Funnels | `/Users/ericcoffie/Projects/govcon-funnels` | `govcongiants.org` | Next.js 16 |
| GovCon Shop | `/Users/ericcoffie/govcon-shop` | `shop.govcongiants.org` | Next.js 16 |
| The Vault | `/Users/ericcoffie/Projects/vault` | `govcongiants.org/vault` | Next.js 15 |

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

## March 2026 Surge Event

**Date:** March 28, 2026 (Saturday)
**Time:** 9:00 AM - 5:00 PM Eastern (8 hours)
**Topic:** Recompete Contracts, IDV, IDIQ
**Format:** FREE, open to public
**April Bootcamp:** Winning with Certifications (Pro Members)

### Files Created
- `march-28-surge-agenda.html` — Full 8-hour agenda with clickable downloads
- `march-surge-page.html` — Landing page
- `funnels/march-surge/` — 4-page funnel (landing → upsell → downsell → thank-you)
- `funnels/march-surge/downloads/` — 6 free resources
- `march-surge-email-sequence/` — 7 emails

### Free Downloads (from recompete tracker)
1. `march-2026-expiring-contracts.xlsx` — 944 real contracts
2. `recompete-positioning-checklist.pdf` — 12-18 month timeline
3. `10-idiq-vehicles-guide.pdf`
4. `active-idiq-vehicles-list.xlsx`
5. `sources-sought-response-template.docx`
6. `task-order-response-template.docx`

---

## Pending Tasks

- [x] Generate March 2026 expiring contracts data
- [x] Create March surge funnel and email sequence
- [ ] Update SBLO contacts (Q2 2026)
- [ ] Update expiring contracts data monthly
- [ ] April Bootcamp: Winning with Certifications materials
