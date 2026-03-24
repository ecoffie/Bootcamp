# Lessons Learned - Contract Vehicles Bootcamp

## Slide Design

### Always start with a hook, not a title slide
The audience needs to be grabbed immediately. Title slides waste precious attention.
- Bad: "Welcome to Contract Vehicles 101"
- Good: "55% of federal dollars flow through vehicles - NOT the open market"

### One stat per hook slide
Don't combine multiple stats on one slide. Let each stat breathe.
- Slide 1: 55% stat
- Slide 2: $77T stat

### Slides must match script structure exactly
Before creating slides, map out the script sections and create corresponding slides:
- HOOK → Hook slides
- CONTENT Section 1-4 → Content slides
- CTA → CTA slides

### No slide labels in exports
"SLIDE 1 - HOOK" labels are for internal reference only. Hide them with `display: none` before exporting PNGs.

### Consistent 16:9 dimensions
Set fixed width/height on slides for consistent PNG export:
```css
.slide {
    width: 1280px;
    min-height: 720px;
}
```

### Use dark theme from January bootcamp
Reference: `/Users/ericcoffie/Bootcamp/january-31-bootcamp-agenda.html`
- Background: `linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%)`
- Text: white
- Accents: green (#10b981)

---

## Puppeteer Export

### Use 2x deviceScaleFactor for retina
```javascript
await page.setViewport({
    width: 1920,
    height: 1080,
    deviceScaleFactor: 2
});
```

### Export script location
Keep export script in same directory as HTML for simple relative paths:
`/contract-vehicles/export-slides.js`

---

---

## YouTube Descriptions

### Every YT Live needs a description file
Create `yt-descriptions.md` with:
- Hook line (the big stat or insight)
- Bullet list of what's covered
- CTA with registration link
- Chapters with timestamps
- Engagement question ("Drop in chat...")
- Hashtags

### Description format template
```markdown
**[HOOK - Big stat or insight]**

[Context paragraph - why this matters]

Tonight I'm covering:
- Point 1
- Point 2
- Point 3

[CTA with link]

Chapters
00:00 - [Topic]
02:00 - [Topic]
...

[Engagement question] 👇

#GovCon #GovernmentContracts #[Topic] #SmallBusiness
```

---

*Updated: March 15, 2026*
