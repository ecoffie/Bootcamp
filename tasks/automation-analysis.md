# Automation Analysis - March 24, 2026

Based on analysis of all Claude sessions, CLAUDE.md files, slash commands, and workflows.

---

## BUCKET 1: SKILLS (Reusable Prompts/Workflows)

### 1. Slide Redesign to Visual Standards
**What you keep doing:** Converting text-heavy slides to 80% visual / 20% text following VISUAL-DESIGN-STANDARDS.md
**Why this bucket:** Pure thinking/writing task with consistent rules
**Frequency:** 4-8 times per bootcamp cycle (20-30x/year)
**Time saved:** 45 min → 10 min per deck
**Implementation:** Skill that takes HTML file, outputs redesigned version with icon grids, hero icons, 10-20 words/slide
**Priority:** HIGH

### 2. YouTube Description Generator
**What you keep doing:** Writing descriptions with chapters, timestamps, CTAs, links
**Why this bucket:** Formulaic writing with standard structure
**Frequency:** 4 per bootcamp × 6 bootcamps = 24/year
**Time saved:** 20 min → 3 min
**Implementation:** Skill that takes video topic, generates full description with chapters template
**Priority:** HIGH

### 3. Email Sequence Generator
**What you keep doing:** Creating 7-email nurture sequences for events
**Why this bucket:** Template-based writing with personalization
**Frequency:** 6-8 times/year
**Time saved:** 2 hours → 20 min
**Implementation:** Skill that takes event details, generates all 7 emails with timing
**Priority:** HIGH

### 4. Fact-Check GovCon Data
**What you keep doing:** Verifying contract vehicle ceilings, thresholds, dates against web sources
**Why this bucket:** Research + verification task
**Frequency:** Weekly (before any slide deck or content)
**Time saved:** 30 min → 5 min
**Implementation:** Skill that queries Perplexity/web for current GovCon data, returns verified table
**Priority:** HIGH

### 5. Blog Post SEO Outline
**What you keep doing:** Creating keyword-optimized outlines with H1/H2, meta, JSON-LD
**Why this bucket:** Structured writing with SEO rules
**Frequency:** 3-4 per month
**Time saved:** 45 min → 10 min
**Implementation:** Skill that takes keyword + topic, outputs full SEO-ready outline
**Priority:** MEDIUM

### 6. Bootcamp Agenda HTML Generator
**What you keep doing:** Creating 8-hour agenda HTML with standard times, breaks, sections
**Why this bucket:** Highly templated HTML generation
**Frequency:** 6-8 per year
**Time saved:** 1 hour → 5 min
**Implementation:** Already exists as `/create-bootcamp` - needs refinement
**Priority:** MEDIUM

### 7. CTA/Hook Writing (Conor Neill Method)
**What you keep doing:** Writing hooks using story→factoid→question formula
**Why this bucket:** Creative writing with methodology
**Frequency:** Every presentation/video
**Time saved:** 15 min → 3 min
**Implementation:** Skill that takes topic, generates 3 hook options using documented formula
**Priority:** MEDIUM

### 8. Product Description Sync
**What you keep doing:** Writing consistent product descriptions for shop, funnels, Stripe
**Why this bucket:** Writing task requiring consistency
**Frequency:** Monthly product updates
**Time saved:** 30 min → 5 min
**Implementation:** Skill that takes product details, outputs consistent copy for all 3 locations
**Priority:** LOW

### 9. Testimonial Formatting
**What you keep doing:** Reformatting customer quotes for slides, pages, emails
**Why this bucket:** Editing/formatting task
**Frequency:** 2-3 per month
**Time saved:** 10 min → 2 min
**Implementation:** Skill that takes raw testimonial, outputs formatted versions for each use
**Priority:** LOW

### 10. Session Handoff Summary
**What you keep doing:** Writing session summaries with state, blockers, next steps
**Why this bucket:** Structured writing task
**Frequency:** End of every session
**Time saved:** 10 min → 2 min
**Implementation:** Already exists as `/handoff` - enforce usage
**Priority:** LOW

---

## BUCKET 2: PLUGINS/TOOLS (External Systems, APIs, Integrations)

### 1. SAM.gov/USASpending Data Fetcher
**What you keep doing:** Querying contract data, verifying vehicle status, checking thresholds
**Why this bucket:** Requires API calls to external government systems
**Frequency:** Daily (alerts) + weekly (content verification)
**Time saved:** 20 min → instant
**Implementation:** MCP tool that wraps SAM.gov + USASpending APIs with NAICS parallel request handling
**Priority:** HIGH

### 2. Stripe-KV-Supabase Sync Tool
**What you keep doing:** Verifying access grants, fixing gaps between systems
**Why this bucket:** Requires API calls to 3 external systems
**Frequency:** 2-3 times per week
**Time saved:** 1 hour → 5 min
**Implementation:** Tool that compares all 3 data sources, reports gaps, auto-fixes
**Priority:** HIGH

### 3. Health Check Aggregator
**What you keep doing:** Running health checks across 3 projects, checking URLs, links, images
**Why this bucket:** Requires HTTP requests across multiple domains
**Frequency:** Daily automated + weekly manual review
**Time saved:** 30 min → 2 min
**Implementation:** Tool that runs unified check across govcongiants.org, shop.*, tools.*
**Priority:** MEDIUM

### 4. PNG Slide Exporter
**What you keep doing:** Running Puppeteer to export HTML slides to PNG
**Why this bucket:** Requires headless browser automation
**Frequency:** 4-8 times per bootcamp cycle
**Time saved:** 5 min → 1 min (already exists, just needs cleanup)
**Implementation:** Already have `export-slides.js` - add to MCP as tool
**Priority:** LOW

### 5. Google Search Console Indexing Tool
**What you keep doing:** Submitting URLs for indexing, checking index status
**Why this bucket:** Requires GSC API
**Frequency:** After each blog post / page creation
**Time saved:** 10 min → instant
**Implementation:** Tool that submits URL list to GSC, returns index status
**Priority:** LOW

---

## BUCKET 3: AGENTS (Multi-Step Autonomous Workflows)

### 1. Bootcamp Deployment Agent
**What you keep doing:** Creating agenda → slides → emails → landing page → handouts → promos
**Why this bucket:** 7+ step workflow with decision-making
**Frequency:** 6-8 times per year
**Time saved:** 6-8 hours → 30 min setup + review
**Implementation:** Already exists as `/deploy-bootcamp` - needs full autonomy
**Priority:** HIGH

### 2. Cross-Project Sync Agent
**What you keep doing:** Updating product info in market-assassin → govcon-shop → Stripe → CLAUDE.md
**Why this bucket:** Multi-system updates with validation
**Frequency:** 2-3 times per week
**Time saved:** 30 min → 5 min
**Implementation:** Agent that reads products.ts, syncs to all locations, validates consistency
**Priority:** HIGH

### 3. Content Publishing Agent
**What you keep doing:** Creating blog → adding schema → updating sitemap → submitting to GSC
**Why this bucket:** Multi-step with external integrations
**Frequency:** 3-4 times per month
**Time saved:** 1 hour → 10 min
**Implementation:** Agent that handles full publish workflow with verification
**Priority:** MEDIUM

### 4. Access Issue Debugger Agent
**What you keep doing:** Checking Stripe → KV → Supabase → Email for customer access problems
**Why this bucket:** Multi-system investigation with fixes
**Frequency:** 1-2 times per week
**Time saved:** 30 min → 5 min
**Implementation:** Agent that traces customer access through all systems, reports gaps, auto-fixes
**Priority:** MEDIUM

### 5. YT Live Content Package Agent
**What you keep doing:** Creating slides → promos → descriptions → scripts for each live
**Why this bucket:** Multi-output workflow per video
**Frequency:** 4 per bootcamp = 24-32/year
**Time saved:** 2 hours → 20 min per live
**Implementation:** Agent that takes live topic, outputs all 4 deliverables
**Priority:** MEDIUM

---

## BUCKET 4: CLAUDE.MD (Rules, Preferences, Standards)

### Missing/Incomplete Sections to Add:

### 1. Visual Design Standards Reference (MISSING)
**Add to:** Root CLAUDE.md
**Content:**
```markdown
## Visual Design Standards
- Primary reference: `~/Action Plan/VISUAL-DESIGN-STANDARDS.md`
- Presentation standards: `~/Bootcamp/docs/presentation-design-standards.md`
- Rule: 10-20 words/slide, 80% visual, icons not bullets
- Email banner CTA format: email "[KEYWORD]" to hello@govconedu.com
```

### 2. Fact-Check Requirements (MISSING)
**Add to:** Root CLAUDE.md
**Content:**
```markdown
## Fact-Check Before Publishing
ALL GovCon data must be web-verified before slides/content:
- Vehicle ceilings: GSA.gov, agency pages
- Threshold changes: FAR updates, SBA.gov
- Vehicle status: SAM.gov announcements
- See verified data table in presentation-design-standards.md
```

### 3. v2 File Convention (MISSING)
**Add to:** Root CLAUDE.md
**Content:**
```markdown
## Versioning Convention
- When redesigning files, create v2: `file-v2.html`
- Keep original for reference
- Update export scripts to support both versions
- Document changes in README
```

### 4. Email Banner Standards (MISSING)
**Add to:** Root CLAUDE.md
**Content:**
```markdown
## YouTube Live Email Banners
- Add red banner to 5-6 key slides per presentation
- Format: email "[KEYWORD]" to hello@govconedu.com
- Keywords by topic: flip, ready, vehicles, proposal, capstat
- Purpose: Track which video leads came from
```

### 5. Export Workflow (INCOMPLETE)
**Add to:** Bootcamp CLAUDE.md
**Content:**
```markdown
## Slide Export Workflow
1. Ensure slides have `display: flex` (not `display: none`)
2. Run: `node export-slides.js [version]`
3. Versions: 01, 02, 03, 03v2, 04, 04v2
4. Output: `live-[version]-pngs/`
5. Open folder to verify quality
```

### 6. Session Lessons Protocol (INCOMPLETE)
**Add to:** Root CLAUDE.md
**Content:**
```markdown
## After Any Correction
1. Immediately update tasks/lessons.md with the pattern
2. Write rule format: "Always X, not Y because Z"
3. If impacts multiple projects, update all CLAUDE.md files
4. If new design standard, update presentation-design-standards.md
```

---

## TOP 10 SKILLS TO BUILD

| Rank | Skill | Frequency | Time Saved | Priority |
|------|-------|-----------|------------|----------|
| 1 | Slide Redesign to Visual Standards | 20-30x/year | 35 min each | HIGH |
| 2 | Fact-Check GovCon Data | Weekly | 25 min | HIGH |
| 3 | YouTube Description Generator | 24x/year | 17 min each | HIGH |
| 4 | Email Sequence Generator | 6-8x/year | 100 min each | HIGH |
| 5 | Blog Post SEO Outline | 36-48x/year | 35 min each | MEDIUM |
| 6 | CTA/Hook Writing | Every presentation | 12 min | MEDIUM |
| 7 | Bootcamp Agenda Generator | 6-8x/year | 55 min each | MEDIUM |
| 8 | Product Description Sync | Monthly | 25 min | LOW |
| 9 | Testimonial Formatting | 24-36x/year | 8 min each | LOW |
| 10 | Session Handoff Summary | Every session | 8 min | LOW |

---

## TOP 5 TOOLS/PLUGINS TO BUILD

| Rank | Tool | Integration | Time Saved/Use | Priority |
|------|------|-------------|----------------|----------|
| 1 | Stripe-KV-Supabase Sync | 3 APIs | 55 min | HIGH |
| 2 | SAM.gov/USASpending Fetcher | 2 APIs | 20 min | HIGH |
| 3 | Health Check Aggregator | HTTP + 3 domains | 28 min | MEDIUM |
| 4 | PNG Slide Exporter | Puppeteer | 4 min | LOW |
| 5 | GSC Indexing Tool | GSC API | 10 min | LOW |

---

## TOP 5 AGENTS TO BUILD

| Rank | Agent | Steps | Time Saved | Priority |
|------|-------|-------|------------|----------|
| 1 | Bootcamp Deployment | 7+ steps | 6-8 hours | HIGH |
| 2 | Cross-Project Sync | 4 systems | 25 min/use | HIGH |
| 3 | YT Live Content Package | 4 outputs | 100 min/live | MEDIUM |
| 4 | Access Issue Debugger | 4 systems | 25 min/issue | MEDIUM |
| 5 | Content Publishing | 5 steps | 50 min/post | MEDIUM |

---

## RECOMMENDED BUILD ORDER

Based on impact × frequency × ease:

### Week 1: Quick Wins
1. **Add CLAUDE.md sections** (30 min) - Missing standards documentation
2. **Fact-Check Skill** (1 hour) - Use before every presentation
3. **YouTube Description Skill** (1 hour) - Template-based, high frequency

### Week 2: High-Impact Tools
4. **Stripe-KV-Supabase Sync Tool** (2-3 hours) - Eliminates recurring access debugging
5. **SAM.gov Data Fetcher** (2 hours) - Powers fact-checking and alerts

### Week 3: Workflow Automation
6. **Slide Redesign Skill** (2 hours) - Codify visual standards transformation
7. **Cross-Project Sync Agent** (3 hours) - End manual product syncing

### Week 4: Full Autonomy
8. **Bootcamp Deployment Agent enhancement** (4 hours) - Full lifecycle automation
9. **YT Live Content Package Agent** (3 hours) - All 4 deliverables per live

### Ongoing
10. **Health Check Aggregator** - After other priorities complete

---

## IMMEDIATE ACTIONS

1. **Update root CLAUDE.md** with missing sections above
2. **Create `/fact-check` skill** for GovCon data verification
3. **Create `sync-access` tool** endpoint for Stripe-KV-Supabase
4. **Enhance `/deploy-bootcamp`** to include visual standards compliance

---

*Analysis based on: 11 slash commands, 6 CLAUDE.md files, 12 task/todo files, 100+ git commits, multiple session histories*

*Last Updated: March 24, 2026*
