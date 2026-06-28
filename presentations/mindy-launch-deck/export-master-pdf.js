// Export the real Mindy Launch master deck → clean landscape PDF, one slide per
// page. Slides are display:none unless .active and scoped by section prefixes;
// force every .slide visible. SKIP the "Drop screenshot" placeholder slides
// (live screen-shares that were never baked into the file — they'd render as
// empty grey boxes) so the recap PDF is clean, professional content only.
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  const htmlPath = path.join(__dirname, 'mindy-launch-master.html');
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

  // Remove placeholder slides, then force the rest visible + one-per-page.
  const removed = await page.evaluate(() => {
    let n = 0;
    document.querySelectorAll('.slide').forEach((s) => {
      if (/Drop screenshot/i.test(s.textContent || '')) { s.remove(); n++; }
    });
    return n;
  });

  await page.addStyleTag({ content: `
    .slide { display: flex !important; page-break-after: always; break-after: page; }
    .slide:last-child { page-break-after: auto; }
    .nav, .controls, .progress, .slide-counter, .dots, [class*="nav"] { display: none !important; }
  ` });

  const count = await page.$$eval('.slide', (s) => s.length);
  const outDir = path.join(__dirname, 'pdf');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  const pdfPath = path.join(outDir, 'Mindy-Launch-Slides.pdf');

  await page.pdf({
    path: pdfPath,
    width: '1280px',
    height: '720px',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  console.log(`✓ Mindy-Launch-Slides.pdf — ${count} clean slides (removed ${removed} placeholders) → ${pdfPath}`);
  await browser.close();
})();
