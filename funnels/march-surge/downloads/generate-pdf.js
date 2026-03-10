const puppeteer = require('puppeteer');
const path = require('path');

async function generatePDF() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  const htmlPath = path.join(__dirname, 'recompete-positioning-checklist.html');
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

  await page.pdf({
    path: path.join(__dirname, 'recompete-positioning-checklist.pdf'),
    format: 'letter',
    margin: { top: '0.5in', right: '0.5in', bottom: '0.5in', left: '0.5in' },
    printBackground: true
  });

  await browser.close();
  console.log('PDF generated: recompete-positioning-checklist.pdf');
}

generatePDF().catch(console.error);
