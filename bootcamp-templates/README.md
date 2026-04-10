# Bootcamp Templates

Data-driven bootcamp generation system. Define bootcamp content in YAML, generate all deliverables automatically.

## Usage

```bash
/deploy-bootcamp [date] [template-name]

# Examples:
/deploy-bootcamp April 25, 2026 first-partner-challenge
/deploy-bootcamp May 30, 2026 contract-vehicles
```

## Available Templates

| Template | File | Description |
|----------|------|-------------|
| `first-partner-challenge` | `first-partner-challenge.yaml` | Find teaming partner in 1 day |
| `contract-vehicles` | `contract-vehicles.yaml` | IDIQs, GWACs, qualifications |

## What Gets Generated

From a single YAML template, the system generates:

1. **Agenda HTML** - Full 8-hour schedule with breaks
2. **Slides HTML** - All session slides (50-100 slides)
3. **Slide PNGs** - Exported images for each slide
4. **PDF** - Combined slide deck
5. **Email Sequence** - 16 pre/post event emails
6. **Landing Page** - Registration funnel

## Template Schema

### Required Sections

```yaml
meta:
  name: "Bootcamp Name"           # Display name
  slug: "bootcamp-slug"           # URL-safe identifier
  tagline: "One line description" # Subtitle
  duration: "8 hours"             # Or "9 hours" for longer events
  format: "FREE"                  # Or "PRO"
  email_keyword: "keyword"        # For email CTA banners
  registration_url: "..."         # Registration link

objectives:                       # The numbered goals
  title: "The X Objectives"
  items:
    - number: 1
      label: "Step Name"
      description: "What happens"

schedule:
  start_time: "9:00 AM"
  end_time: "5:00 PM"
  timezone: "ET"
  breaks: [...]
  sessions: [...]

deliverables: [...]               # What attendees receive
```

### Optional Sections

```yaml
differentiator:                   # What makes this unique
  headline: "..."
  text: "..."

value_exchange:                   # For teaming-focused bootcamps
  you_bring: [...]
  they_bring: [...]

paths:                            # Multiple tracks (A/B)
  - name: "Path A"
    items: [...]

tools:                            # Featured tools
  - name: "Tool Name"
    icon: "emoji"
    description: "..."

scripts:                          # Reusable scripts/templates
  phone_intro: {...}
  voicemail: {...}

email_sequence:                   # Email generation config
  keyword: "..."
  themes: {...}

landing_page:                     # Landing page structure
  headline: "..."
  sections: [...]

quotes:                           # Reusable quotes
  - text: "..."
    context: "opening"
```

## Session Types

| Type | Color | Use For |
|------|-------|---------|
| `strategy` | Green | Big picture, mindset |
| `workshop` | Green | Hands-on activities |
| `tactical` | Green | Step-by-step how-to |
| `power_hour` | Red | Live action sessions |
| `qa` | Green | Q&A, hot seats |
| `close` | Green | Wrap-up, resources |

## Slide Types

### Content Slides

| Type | Description |
|------|-------------|
| `icon_grid` | 2x2 or 2x3 icons with labels |
| `stat_cards` | 3 stat boxes in a row |
| `two_column` | Side-by-side comparison |
| `bullets` | Arrow bullet list |
| `table` | Data table |
| `quote` | Centered quote |
| `definition` | Term + explanation |

### Interactive Slides

| Type | Description |
|------|-------------|
| `workshop` | Checklist with badge |
| `script` | Yellow script boxes |
| `live_demo` | Demo steps + action |
| `go_slide` | Red full-screen "GO" |

### Structure Slides

| Type | Description |
|------|-------------|
| `session_header` | Green session intro |
| `power_hour_header` | Red power hour intro |
| `cta` | Purple CTA slide |
| `final` | Closing slide |

## Creating a New Template

1. **Copy existing template:**
   ```bash
   cp first-partner-challenge.yaml new-topic.yaml
   ```

2. **Update meta section:**
   - Change name, slug, tagline
   - Set format (FREE/PRO)
   - Define email keyword

3. **Define objectives:**
   - What are the 3-5 goals?
   - What's the key insight?

4. **Build sessions:**
   - 6-8 sessions for 8 hours
   - Include breaks
   - Define slides for each

5. **Add deliverables:**
   - What do they leave with?
   - Templates, recordings, access

6. **Configure emails:**
   - Pre-event sequence
   - Post-event follow-up

7. **Test generation:**
   ```bash
   /deploy-bootcamp [test-date] new-topic
   ```

## Best Practices

### Content
- Keep objectives to 3-5 items
- Session duration: 30-90 minutes
- Include Power Hours for action-based bootcamps
- End with accountability/commitments

### Slides
- 10-20 words per slide max
- Use icon_grid instead of bullets
- Every session starts with session_header
- Include workshop slides for hands-on

### Emails
- 14 pre-event emails
- Day-of email
- 7 post-event follow-ups
- End with next bootcamp invite

## File Structure

```
bootcamp-templates/
├── README.md                      # This file
├── first-partner-challenge.yaml   # FPC bootcamp
├── contract-vehicles.yaml         # CV bootcamp
├── proposal-writing.yaml          # Proposal bootcamp
└── _template.yaml                 # Blank starter
```

## Related Docs

- `/deploy-bootcamp` command: `~/.claude/commands/deploy-bootcamp.md`
- Visual standards: `~/Action Plan/VISUAL-DESIGN-STANDARDS.md`
- Reference slides: `~/Bootcamp/presentations/march-28-bootcamp-slides.html`
- Reference agenda: `~/Bootcamp/january-31-bootcamp-agenda.html`
