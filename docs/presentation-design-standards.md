# GovCon Giants Presentation Design Standards

**Last Updated:** March 22, 2026
**Use For:** YouTube Lives, Bootcamp slides, Webinars, All presentations

---

## Color Palette

### Primary Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Navy Blue | `#1e3a8a` | Primary background, headers |
| Purple | `#7c3aed` | Gradient endpoint, accents |
| Light Purple | `#a855f7` | Highlights, secondary accents |

### Accent Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Green | `#10b981` | CTAs, success, key stats, bullet markers |
| Light Green | `#34d399` | Hover states, secondary green |
| Emerald | `#059669` | Buttons, strong emphasis |

### Alert/Urgency Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Orange | `#f97316` | Warnings, "coming soon" |
| Light Orange | `#fb923c` | Secondary warnings |
| Red | `#dc2626` | Urgency, "final call", deadlines |

### Backgrounds

| Type | CSS |
|------|-----|
| Slide background | `linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%)` |
| CTA box | `linear-gradient(135deg, #059669 0%, #10b981 100%)` |
| Info box | `rgba(255,255,255,0.1)` with `border: 2px solid rgba(255,255,255,0.2)` |
| Stat box | `linear-gradient(135deg, #059669 0%, #10b981 100%)` |

---

## Typography

### Fonts

- **Primary:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Fallback:** System sans-serif stack

### Font Sizes (Slides)

| Element | Size | Weight |
|---------|------|--------|
| Slide title (h2) | `2.8rem` | 800 |
| Section title (h3) | `1.6rem` | 700 |
| Body text | `1.2-1.3rem` | 400 |
| Stat numbers | `3-5rem` | 900 |
| Stat labels | `1-1.4rem` | 400 |
| CTA URL | `1.4rem` | 800 |

### Text Colors

| Element | Color |
|---------|-------|
| Headlines | White |
| Body text | `rgba(255,255,255,0.9)` |
| Accent text | `#10b981` (green) |
| Highlight text | `#a855f7` (light purple) |

---

## Slide Dimensions

| Format | CSS Size | Export Size |
|--------|----------|-------------|
| YouTube/Presentation | 1280x720px | 2560x1440px (@2x retina) |
| Thumbnail | 1280x720px | 2560x1440px (@2x retina) |

---

## Component Styles

### Stat Box

```css
.stat-box {
    background: linear-gradient(135deg, #059669 0%, #10b981 100%);
    border-radius: 16px;
    padding: 30px;
    text-align: center;
}
```

### Info Box

```css
.info-box {
    background: rgba(255,255,255,0.1);
    border: 2px solid rgba(255,255,255,0.2);
    border-radius: 16px;
    padding: 25px;
}
```

### Info Box Variants

| Variant | Border Color | Background |
|---------|--------------|------------|
| `.green` | `#10b981` | `rgba(16, 185, 129, 0.15)` |
| `.purple` | `#a855f7` | `rgba(168, 85, 247, 0.15)` |
| `.blue` | `#3b82f6` | `rgba(59, 130, 246, 0.15)` |
| `.orange` | `#f97316` | `rgba(249, 115, 22, 0.15)` |

### CTA Box

```css
.cta-box {
    background: linear-gradient(135deg, #059669 0%, #10b981 100%);
    color: white;
    border-radius: 20px;
    padding: 50px;
    text-align: center;
}

.cta-box .url {
    display: inline-block;
    background: white;
    color: #059669;
    padding: 18px 50px;
    border-radius: 40px;
    font-weight: 800;
    font-size: 1.4rem;
}
```

### Tables

```css
.vehicle-table th {
    background: rgba(16, 185, 129, 0.3);
    color: white;
    padding: 16px 20px;
    border-bottom: 2px solid #10b981;
}

.vehicle-table td {
    padding: 14px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.vehicle-table tr.highlight {
    background: rgba(16, 185, 129, 0.2);
    border-left: 4px solid #10b981;
}
```

---

## Layout Patterns

### Two-Column

```css
.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
}
```

### Three-Column (Stats)

```css
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
}
```

---

## Slide Structure

### Standard Slide

```html
<div class="slide">
    <h2>Slide Title</h2>
    <p>Introduction text</p>
    <!-- Content: lists, tables, stat boxes, two-col layouts -->
</div>
```

### Title Slide

- Large centered headline
- 3 stat boxes in a row
- Date/event subtitle in green

### CTA Slide (Final)

- Green gradient background
- Large headline
- URL in white pill button
- Event details below

---

## Speech/Script Standards

### Hook Formula (Conor Neill Method)

**Best:** Start with a story about a person
> "Last year, I was sitting with a contractor who..."

**Second:** A shocking factoid
> "55% of federal dollars flow through vehicles you've never heard of."

**Third:** A question that matters
> "How many contracts have you lost without knowing why?"

**Avoid:** Starting with your name, title, or topic announcement.

### Script Labels

| Label | Color | Usage |
|-------|-------|-------|
| HOOK | Red `#dc2626` | Opening 0:00-1:30 |
| CONTENT | Purple `#7c3aed` | Main content |
| CTA | Green `#059669` | Call to action |
| TRANSITION | Orange `#f59e0b` | Between sections |

---

## File Naming Convention

### Slides
- `live-01-[topic].html`
- `live-02-[topic].html`

### PNG Exports
- `live-01-pngs/slide-01.png`
- `live-01-pngs/slide-02.png`

### Scripts
- `yt-descriptions.md`
- `[event]-youtube-promos.html`

---

## Export Process

1. Open HTML slide file in browser
2. Run `node export-slides.js` from slides directory
3. PNGs export at 2560x1440 (@2x retina)
4. Upload to YouTube as custom slides or thumbnails

---

## Reference Files

- **Visual Design Standards:** `~/Action Plan/VISUAL-DESIGN-STANDARDS.md` ⭐ PRIMARY
- **Speech openings:** `/Bootcamp/docs/speech-openings-conor-neill.md`
- **Design reference:** `/Bootcamp/january-31-bootcamp-agenda.html`
- **Color source:** `~/CLAUDE.md` (Design System section)

---

---

## Fact-Check Requirements

**ALL content with GovCon data MUST be verified before publishing.**

### Verify These Data Points

| Data Type | Common Errors | Verify Against |
|-----------|---------------|----------------|
| Contract vehicle ceilings | Outdated figures | GSA.gov, agency vehicle pages |
| Vehicle status (open/closed) | Cancelled vehicles (CIO-SP4) | SAM.gov, GSA announcements |
| Sole source thresholds | Old FAR limits | FAR 19.8 (updated Oct 2025) |
| Set-aside requirements | Threshold changes | SBA.gov, FAR updates |
| Agency spending figures | Inflated estimates | USASpending.gov |

### Current Verified Data (March 2026)

| Vehicle | Ceiling | Status | Notes |
|---------|---------|--------|-------|
| OASIS+ | No Cap | Open | All pools accepting |
| 8(a) STARS III | $50B | Open | Ordering ends Jul 2026 (extension pending) |
| Alliant 3 | No Cap | Awarded Feb 2026 | Phase 2 coming |
| Alliant 2 | $82.8B | Active | Expires 2028 |
| CIO-SP3 | $20B | Extended | Thru Apr 2027 (CIO-SP4 cancelled) |
| SEWP V | $20B | Active | ~$2B/year spend |
| SEWP VI | $60B | Source Selection | Coming 2026 |
| VETS 2 | $5B | Open | SDVOSB IT services |
| HCaTS SB | $5.75B | Active | Expires Nov 2026 |
| GSA MAS | Unlimited | Open | ~$41B annually |

### Current Thresholds (Oct 2025 Update)

| Threshold | Amount |
|-----------|--------|
| 8(a) sole source (services) | $5.5M |
| 8(a) sole source (manufacturing) | $8.5M |
| Simplified acquisition | $250K |
| Micro-purchase | $10K |

### Fact-Check Process

1. **Before creating slides**: Search Perplexity/web for current vehicle data
2. **Cross-reference**: GSA.gov, agency vehicle pages, recent news
3. **Flag outdated info**: If data is >6 months old, verify
4. **Update this table**: When verified data changes, update here

### Sources for Verification

- **GSA Vehicles**: gsa.gov/buy-through-us
- **SEWP**: sewp.nasa.gov
- **NITAAC (CIO-SP)**: nitaac.nih.gov
- **FAR Thresholds**: acquisition.gov/far
- **Spending Data**: usaspending.gov
- **Vehicle News**: fedscoop.com, washingtontechnology.com

---

## YouTube Live Email Banner

**Add to 5-6 key slides per presentation for lead capture.**

### Design

```css
.email-banner {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: #dc2626;
    color: white;
    text-align: center;
    padding: 16px 40px;
    font-size: 28px;
    font-weight: 700;
}

.email-banner .keyword {
    background: white;
    color: #dc2626;
    padding: 4px 16px;
    border-radius: 6px;
    margin: 0 8px;
}
```

### Format

```
email "[KEYWORD]" to hello@govconedu.com
```

### Which Slides

| Slide Type | Include Banner |
|------------|----------------|
| Title slide | ✅ Yes |
| Key stat slide | ✅ Yes |
| Key takeaway | ✅ Yes |
| Action items | ✅ Yes |
| Final CTA | ✅ Yes |
| Content slides | ❌ No (distracting) |

### Keyword Examples

| Video Topic | Keyword |
|-------------|---------|
| Sources Sought / Flip Contracts | "flip" |
| IDIQ Overview | "idiq" |
| Contract Vehicles Deep Dive | "vehicles" |
| Final Call / Bootcamp Preview | "ready" |
| Proposal Writing | "proposal" |
| Capability Statement | "capstat" |
| Set-Asides | "setaside" |
| Task Orders | "taskorder" |

### Purpose

- Tracks which video the lead came from
- Low-friction CTA (just email a word)
- Builds email list from YouTube viewers
- Enables follow-up sequences

---

*Apply these standards to all GovCon Giants presentations for brand consistency.*
