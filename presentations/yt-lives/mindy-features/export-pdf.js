// Export each Mindy-feature deck to a single landscape PDF (one slide per page).
// Reuses the proven display-toggle from export-slides.js: slides are display:none
// unless .active, so we force ALL slides visible (block) before printing, then
// print at 16:9 so each .slide becomes one page.
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const DECKS = {
  '01': { file: 'live-01-find-your-market.html',  out: 'Mindy-01-Find-Your-Market.pdf' },
  '02': { file: 'live-02-win-the-recompete.html', out: 'Mindy-02-Win-The-Recompete.pdf' },
  '03': { file: 'live-03-write-the-proposal.html',out: 'Mindy-03-Write-The-Proposal.pdf' },
  '04': { file: 'live-04-know-who-to-call.html',  out: 'Mindy-04-Know-Who-To-Call.pdf' },
  '05': { file: 'live-05-trust-the-data.html',    out: 'Mindy-05-Trust-The-Data.pdf' },
};

(async () => {
  const outDir = path.join(__dirname, 'pdf');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const browser = await puppeteer.launch({ headless: 'new' });
  const only = process.argv[2]; // optional single deck, e.g. "01"

  for (const [key, deck] of Object.entries(DECKS)) {
    if (only && only !== key) continue;
    const page = await browser.newPage();
    const htmlPath = path.join(__dirname, deck.file);
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

    // Force every slide visible + page-break per slide, kill nav chrome.
    await page.addStyleTag({ content: `
      .slide { display: flex !important; page-break-after: always; break-after: page; }
      .slide:last-child { page-break-after: auto; }
      .nav, .slide-nav, .controls, .progress, .slide-counter, [class*="nav-"] { display: none !important; }
    ` });

    const count = await page.$$eval('.slide', (s) => s.length);
    const pdfPath = path.join(outDir, deck.out);
    await page.pdf({
      path: pdfPath,
      width: '1280px',
      height: '720px',          // 16:9 — one slide fills one page
      printBackground: true,
      pageRanges: '',
      margin: { top: 0, right: 0, bottom: 0, left: 0 },
    });
    console.log(`✓ ${deck.out} (${count} slides)`);
    await page.close();
  }

  await browser.close();
  console.log('Done → ' + outDir);
})();
