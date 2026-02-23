# Databases — Contractors, SBLOs & Contacts

## SBLO Contact Databases

| File | Description |
|------|-------------|
| `FINAL-SBLO-CONTACT-LIST.csv` | Master SBLO contact list |
| `FINAL-SBLO-CONTACT-LIST-WITH-PORTALS.csv` | With vendor portal URLs |
| `SBLO-CONTACT-DIRECTORY-PDF-READY.html` | PDF-ready directory |
| `sblo-list-compiled.csv` | Compiled from multiple sources |
| `dhs-contacts-*.csv` | DHS-specific contacts |
| `dot-contacts*.csv` | DOT-specific contacts |
| `dod-csp-contacts*.csv` | DoD contacts |

## Prime Contractor Databases

| File | Description |
|------|-------------|
| `FEDERAL-CONTRACTOR-MASTER-DATABASE.csv` | Master database (~2,500+ companies) |
| `FEDERAL-CONTRACTOR-MASTER-DATABASE-SEARCHABLE.html` | Searchable web version |
| `sba-prime-directory-companies.csv` | SBA prime directory extract |
| `contractor-database.json` | JSON format for web tools |
| `contracts-data.js` | JavaScript data file |

## Tier 1 Prime Contractors (Top 100+)

| File | Description |
|------|-------------|
| `tier1-batch-01.csv` through `tier1-batch-12.csv` | Research batches |
| `tier1-vendor-portal-searches.csv` | Vendor portal research |
| `priority-batch-01.csv` through `priority-batch-06.csv` | Priority batches |
| `PRIORITY-COMPANIES-VENDOR-PORTALS.md` | Vendor portal documentation |

## Tier 2 Suppliers (Mid-size Contractors)

| File | Description |
|------|-------------|
| `TIER-2-FINAL-CONTACT-LIST.csv` | Master Tier 2 list |
| `TIER-2-FINAL-CONTACT-LIST-WITH-PORTALS.csv` | With vendor portals |
| `tier2-high-priority-list.csv` | High-priority Tier 2 companies |
| `tier2-priority-batch-01.csv` through `tier2-priority-batch-06.csv` | Research batches |
| `tier2-batch-01.csv` through `tier2-batch-09.csv` | All Tier 2 batches |
| `TIER-2-VENDOR-REGISTRATION-DIRECTORY-PDF-READY.html` | PDF-ready directory |

## Expiring Contracts Data

| File | Description |
|------|-------------|
| `Expiring_Contracts - 2026 - January February.csv` | Jan/Feb 2026 expiring |
| `Expiring Contracts 2025 - Expiring Contracts - December 2.csv` | December 2025 |
| `expiring-contracts.json` | JSON format |
| `expiring-contracts-viewer.html` | Interactive viewer |

## Knowledge Bases (AI Chatbot Training)

**Main Files:**

| File | Size | Description |
|------|------|-------------|
| `highlevel-knowledge-base.md` | 90KB / 1,215 lines | Primary HighLevel chatbot KB |
| `government-contracting-knowledge-base.md` | 81KB / 1,452 lines | Comprehensive GovCon KB |
| `highlevel-kb-complete.md` | 66KB | Complete consolidated KB |
| `highlevel-kb-complete.docx` | 43KB | Word format for upload |
| `highlevel-knowledge-base-compact.md` | 9KB | Compact/summary version |

**Split Files (for chunked uploads):**

| File | Description |
|------|-------------|
| `highlevel-kb-part1.md` | 21KB - Core topics |
| `highlevel-kb-part2.md` | 24KB - Certifications & programs |
| `highlevel-kb-part3.md` | 10KB - Finding opportunities |
| `highlevel-kb-part4.md` | 10KB - Sales & objections |

**KB Categories (30 topics):**
1. General Overview, 2. Multiple Business Ideas, 3. Myths and Misconceptions, 4. Eligibility, 5. Size Standards, 6. Readiness, 7. SAM.gov Registration, 8. UEI and CAGE Code, 9. State and Local Registration, 10. Certifications Overview, 11. WOSB and EDWOSB, 12. SDVOSB, 13. 8(a) Program, 14. HUBZone, 15. State Certifications, 16. Which Certification First, 17. Finding Opportunities, 18. Why Businesses Struggle, 19. Bidding and Proposals, 20. About Us, 21. Free Course, 22. Surge Bootcamp, 23. January Bootcamp, 24. Results and Outcomes, 25. Pricing and Investment, 26. Getting Started, 27. Eric Coffie's 5-Phase Action Plan, 28. Objection Responses, 29. Prospect Assessment, 30. Buyer Psychology

**Configuration Variables in KB:**
```
{{BusinessName}}, {{City}}, {{State}}, {{ServiceName}}
{{ConsultationLink}}, {{PhoneNumber}}, {{Email}}, {{Website}}
{{OpportunityHunterLink}}
```

## Python Scripts

### Data Processing

| Script | Purpose |
|--------|---------|
| `compile-sblo-list.py` | Compile SBLO contacts from sources |
| `create-master-searchable-database.py` | Generate searchable database |
| `create-tier2-priority-batches.py` | Create Tier 2 research batches |
| `merge-all-portal-data.py` | Consolidate vendor portal data |
| `update-database-vendor-portals.py` | Update database with portals |

### Hit List Generation

| Script | Purpose |
|--------|---------|
| `create-hit-list-from-csv.py` | Generate hit lists from CSV |
| `create-gc-hit-list.py` | General contractor hit lists |
| `auto-generate-hit-lists.py` | Automated hit list generation |
| `update-hit-lists-for-month.py` | Monthly updates |
| `combine-hit-lists.py` | Combine multiple lists |

### Web Scraping & Research

| Script | Purpose |
|--------|---------|
| `scrape-dhs-*.py` | DHS contact scraping |
| `scrape-dot-*.py` | DOT directory scraping |
| `search-sba-dsbs-tribal-8a.py` | SBA/DSBS searching |
| `find-tribal-8a-companies.py` | Tribal 8(a) research |
| `find-vendor-registration-links.py` | Vendor portal finder |

### Data Cleanup

| Script | Purpose |
|--------|---------|
| `cleanup-database.py` | Database cleanup |
| `fix-contact-data.py` | Contact data fixes |
| `refine-tier2-list.py` | Tier 2 list refinement |
