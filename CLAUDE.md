# GovCon Giants - Bootcamp Project

**Last Updated:** February 24, 2026
**Owner:** Eric Coffie
**Purpose:** Federal contracting bootcamp materials, marketing assets, and business tools

---

## Project Overview

This repository contains all GovCon Giants resources for helping small businesses win federal government contracts: bootcamp materials, hit lists, SBLO/contractor databases, email sequences, YouTube content, presentations, and AI/automation tools.

---

## Key Dates

- **Next Bootcamp:** February 28, 2026 (Specifics & Proposals)
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
| `funnels/` | Marketing funnels (opportunity-hunter, etc.) |
| `presentations/` | Bootcamp slides, TempNet, Veteran War Room |
| `webinar/` | Webinar materials and scripts |
| `files/` | Proposal bootcamp handouts (IDIQ guide, templates) |
| `govcon-resources/` | Deployed web resources |
| `govcon-tools/` | Web-based tools |
| `docs/` | Detailed documentation (see below) |

### Root File Patterns

- `january-hit-list-*.html` — Contract opportunity hit lists
- `january-*.html` — January bootcamp materials
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

## Pending Tasks

- [ ] Generate March 2026 hit lists
- [ ] Update SBLO contacts (Q2 2026)
- [ ] Update expiring contracts data monthly
