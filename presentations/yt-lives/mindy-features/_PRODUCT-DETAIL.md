REAL PRODUCT DETAIL — Mindy (Market Assassin codebase, getmindy.ai)
Use this to ground the "how Mindy does it" + LIVE DEMO slides. Routes, components, demo steps, and real counts are from the production codebase. Quote real route paths and steps; do not invent UI that isn't listed here.

NOTE ON NUMBERS (grounding rule): For marketing headline figures keep the literature numbers (317K contractors, 88K SAM opps, 125K contacts, 7,700+ forecasts, 170 commands). The codebase shows the same data with some operational counts (e.g. ~29K active opps in the sam_opportunities working table, ~112K contacts synced, 2,700 Tier-2 contractors). When a slide cites the DATABASE size use the literature headline (317K / 88K / 125K). When a slide describes a LIVE DEMO action, the on-screen counts may differ — that's fine; describe the action, not a fabricated number.

LIVE DEMO slides: style them as a distinct slide that says "LIVE DEMO" (use an h3 or a badge) then the steps the host performs on screen. The host screen-shares getmindy.ai. Keep steps to 3-5 short lines.

================================================================
PILLAR 1 — FIND YOUR FEDERAL MARKET
Routes: dashboard /briefings ; onboarding /app/onboarding ; market scanner API GET /api/market-scanner?naics=238220&state=GA ; market research GET /api/app/target-market-research ; code suggestion /api/suggest-codes ; sample opps POST /api/sample-opportunities
Components: MarketScanner.tsx (the 6-question Federal Market Scanner), keyword-coverage.ts (keyword→NAICS coverage engine)
The 6 questions the Market Scanner answers from NAICS + State: 1) WHO is buying? 2) HOW are they buying? 3) WHO has it now? 4) WHAT opportunities exist? 5) WHAT events? 6) WHO to talk to?
Keyword-coverage engine returns: totalMarket ($), coverageCodes (smallest NAICS set for 90% coverage), topCodePct (% in the obvious code), topPsc (what was actually bought). "Sport Mode" uses the FULL coverage set (~8 codes), not just top 3.
Auto-onboarding: user types a business description or pastes a capability statement → /api/suggest-codes suggests NAICS/PSC from real USASpending awards → user browses sample opportunities and picks 3+ that match → system extracts keywords/agencies/set-asides into user_business_profiles.
Industry presets in product: Construction (236/237/238), IT Services (541511-541519), Cybersecurity, Healthcare, Logistics, Facilities, Training. Quick agencies: DHS, VA, GSA, DoD, Army Corps, HHS, DOE, NASA, DOJ, DOT.
LIVE DEMO STEPS: 1) Log in → onboarding. 2) Type business description → AI suggests NAICS. 3) Browse sample opps, select 3+ matches. 4) Confirm → dashboard. 5) Open Federal Market Scanner → enter NAICS + state → the 6 questions answered live.
Grounded headline stats (keep): drones 70+ NAICS / $245M FY2025 / obvious code 28% / miss 72%; cyber 72+ / $2.07B / 26% / 74%; medical 48+ / $25M / 26% / 74%. NAICS=who the seller is; PSC=what was bought (drones top PSC = 1550 Unmanned Aircraft).

================================================================
PILLAR 2 — WIN THE RECOMPETE
Routes: /briefings → Recompetes tab ; incumbent GET /api/app/incumbent?naics=&agency=&title= ; award detail GET /api/app/award-detail?id=  or ?piid= ; IDV/IDIQ GET /api/app/idv-contracts
Components: RecompetesPanel.tsx
Recompetes panel shows ExpiringContract rows: title, incumbent name+UEI, agency, NAICS, value, expirationDate, daysUntilExpiration, bidsReceived, competitionLevel, location. Urgency badges: "🔥 3 DAYS LEFT" (red), "⚡ X days" (orange), "📅 2 weeks" (yellow). Filters: NAICS, Agency, State, Set-Aside.
Incumbent intel API returns {found, incumbent:{name, state, obligated, ceiling, expires, vehicle, fundingAccount, confidence, usaSpendingUrl}} — and honestly returns {found:false} when there's no good match (no fake data). 1-hour cache per (naics,agency,title).
Award drill-down (Contract Summary): obligated → ceiling (real prize size), parent IDV/vehicle you must hold, period of performance (POP) dates, recipient city/state/congressional district, NAICS/PSC description, funding account, USASpending link.
IDV/task-order rows from USASpending spending_by_award with award_type_codes:[IDV_*] — shows the parent vehicle behind each task order.
"in your area" signal: classifyLocation() classifies a contract vs the user's HQ / service area / neighboring states.
LIVE DEMO STEPS: 1) Dashboard → Recompetes panel. 2) See the table of expiring contracts (user's NAICS+agency). 3) Click a row → "▸ Who holds this now?" expander → incumbent, value, expiration, bid count, competition badge. 4) Click View Award Details → obligated vs ceiling, POP, recipient location, funding account, USASpending link. 5) If it's a task order → View Vehicle → parent IDIQ.
Grounded stats (keep): ~80% of opps are recompetes. Example incumbent readout from literature: Jones Lang LaSalle; ceiling $55.9M; expires 2033; vehicle 47PF0022A0012. Vehicle counts in-cache: IDIQ 195, CSO 40, BPA 29, BAA 19, Other Transaction 11; 40% have no NAICS (Special Notices). SOW recovery is roadmap — badge "(coming)".

================================================================
PILLAR 3 — WRITE THE WINNING PROPOSAL
Routes (all under /api/app/proposal/): wizard (intake: upload solicitation / paste link) ; bid-gates (bid/no-bid gate) ; compliance (compliance matrix) ; draft (Vault-grounded drafts) ; extract-sow (pull SOW/PWS) ; export + doc-download (.docx) ; chat (refine)
Proposal Wizard: upload RFP PDF, paste solicitation number, or SAM.gov link → auto-extracts requirements, compliance clauses, NAICS, agency, deadline, SOW/PWS.
Bid/No-Bid gate: pulls incumbent intel ("who currently holds this?"), weighs incumbent strength + bid-count competition + alignment to user's NAICS/keywords → user picks Bid / No-Bid / Maybe (tracked in pipeline). Surfaces the recompete angle.
Compliance matrix: auto-maps every RFP requirement → user's answer → status (Gap / Met / Exceed), each cell linkable to a Vault doc. Columns: Requirement | Your Answer | Status. Exportable.
Vault-grounded drafts: Vault = the user's library (past proposals, SOWs, team bios, similar awards, org charts, CLIN samples). LLM reads RFP requirements + Vault docs → drafts sections (Executive Summary, Technical Approach, Management Plan, CLIN pricing) grounded in the user's REAL past language, with citations back to Vault sources. Real UEI/CAGE/past performance filled in, not [placeholders].
Has SOW/PWS filter: badges opportunities that include a real Statement of Work / Performance Work Statement so you cut to bid-ready ones.
Export: downloads Compliance Matrix + Draft sections as a formatted Word .docx (sections, tables, TOC preserved).
Pipeline next-action engine: computes "Draft Compliance Matrix" → "Refine Draft" → "Submit Proposal" from stage + deadline + draft status.
LIVE DEMO STEPS: 1) Pipeline opportunity → Start Proposal. 2) Upload RFP PDF or paste link → auto-extract. 3) Bid/No-Bid gate shows incumbent + competition → pick BID. 4) Compliance matrix builds (Requirement | Your Answer | Gap). 5) Browse Vault → pick a past SOW → draft grounds in it with citations. 6) Export to Word.
Roadmap: semantic "funny names" matching — badge "(coming)".

================================================================
PILLAR 4 — KNOW WHO TO CALL
Routes: /briefings → Contacts tab ; directory GET /api/app/federal-contacts?search=&agency=&office=&role= ; facets ?facets=agencies / ?facets=offices&agency=VA / ?facets=office-roster&agency=&office= ; teaming GET/POST /api/teaming ; incumbent → OSBP via /api/app/incumbent
Components: ContactsPanel.tsx (+ teaming CRM)
Federal contacts directory: federal_contacts table synced daily from SAM Point-of-Contact API. Filters: Agency, Office, Role, Title keyword. Role badges: Contracting Officer | Small Business (OSBP/SBLO) | Contract Specialist | Program/Technical | Leadership. Title cleanup: extracts real job titles out of generic "Primary Contact" POC slots (honest about which is a real role). Military office codes decoded: NAVSUP → Naval Supply Systems Command, NAVFAC → Naval Facilities Engineering Command, DLA → Defense Logistics Agency, ACC → Army Contracting Command, MICC, DITCO, DISA, etc. Overseas offices filtered out (Yokosuka, Okinawa, Ramstein, Bahrain…).
Office rosters: ?facets=office-roster returns the COMPLETE roster (min 3 people) for a specific contracting office, DoDAAC-decoded for DoD/DLA/Navy (civilian agencies = preview). Uses dodaac_directory to decode codes. Shows office spending tier + OSBP contact + key KOs.
Teaming/subcontracting CRM: track partners as Prime | Sub | Joint Venture | Mentor; outreach status Not Started → Contacted → Responded → Meeting Set → Partnered; stores name, UEI, CAGE, contact, NAICS, certs, past performance, notes, source. Link partners to pipeline pursuits ("this pursuit needs 3 subs → quick-add from CRM").
Multi-client / workspace mode: multiple workspaces; contacts + teaming roster synced per workspace, privacy-gated by team role; each client onboarded from a pasted capability statement.
LIVE DEMO STEPS: 1) Contacts panel. 2) Search "Navy small business officer" → filters to agency=Navy, role=Small Business. 3) Results show contacts with OSBP badge. 4) Office Rosters → pick "Naval Supply Systems Command" → full roster (names, roles, phones, emails). 5) Save a contact to CRM → choose teaming type → add note. 6) View Teaming Partners → filter by status.
Grounded stats (keep marketing headline): 125,000+ contacts, 170-command OSBP directory. (Operational: ~112K synced rows, 56 distinct agencies — fine for demo context.)

================================================================
PILLAR 5 — TRUST THE DATA
Routes: admin command center GET /api/admin/data-sources ; freshness watchdog GET /api/cron/check-data-freshness (quarterly cron, flags overdue, emails a checklist). Registry doc: docs/DATA-SOURCES-REGISTRY.md → data_sources table (28 sources).
Live API sources (real-time, no refresh): USASpending awards (market totals, top agencies, suggest-codes $, teaming primes, bid/no-bid competitors); USASpending IDV/IDIQ (vehicles, task orders, real UEIs); USASpending offices (office-level drill-down); SAM.gov Opportunities (active opps, all notice types, daily); Grants.gov ($700B+ grants).
Built/curated sources (real provenance, periodic refresh): Tier-2 contractor DB (2,700+ with SBLO contacts; from SBA Prime Directory + DoD CSP + DHS OSDBU; quarterly); DoD command/OSBP directory (170 commands; quarterly names); Agency pain points (3,045 points / 307 agencies; from GAO high-risk + NDAA; quarterly); DoDAAC directory (military codes→names; from BigQuery FPDS); Forecast intelligence (7,764 forecasts; 13 agency sources; weekly).
Refresh policy: Real-time (SAM/USASpending/Grants/LLM) ; Quarterly (SBLO/tier-2, tribal, pain points, agency intel) ; Annual (NAICS/PSC codes, agency budgets, DoDAAC, command names, NDAA) ; As-published (forecasts weekly). Stale = built/curated source >100 days old; never auto-fake freshness — stamp after a real refresh (?stamp=<source-key>).
The promise: "Mindy never guesses. Every code, every dollar, every contact traces to a real government source — and we refresh on a schedule." Trust differentiator vs generic AI; due-diligence story for investors/acquirers.
LIVE DEMO STEPS (admin-facing, optional): 1) Command Center → Data Sources. 2) Table: Source | Category | Record Count | Last Built | Cadence | Status (green/yellow/red). 3) Click a source → see provenance citation. 4) Check Freshness → cron flags overdue sources.
Grounded headline counts (keep, cite 317K NOT 2.7K for the contractor DATABASE): 317,106 contractors (USASpending BigQuery recipients universe) ; 125,000+ contacts ; 88,000+ live SAM opps ; 7,700+ forecasts across 11+ agencies ($94B+) ; 170 OSBP commands. Email-any-opportunity is roadmap — badge "(coming)".
