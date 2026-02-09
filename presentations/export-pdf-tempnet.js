const puppeteer = require('puppeteer');
const path = require('path');
const { execSync } = require('child_process');

async function exportToPDF() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  const slidesPath = path.join(__dirname, 'tempnet-staffing-presentation-v1.html');
  await page.goto(`file://${slidesPath}`, { waitUntil: 'networkidle0' });

  // Print-specific styles for clean 960x540 pages
  await page.addStyleTag({
    content: `
      @media print {
        body { background: white !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
        #nav-bar { display: none !important; }
        #slide-viewer { height: auto !important; overflow: visible !important; scroll-snap-type: none !important; }
        #slide-viewer .slide {
          scroll-snap-align: unset !important;
          margin: 0 !important;
          box-shadow: none !important;
          page-break-after: always !important;
          page-break-inside: avoid !important;
          width: 960px !important;
          height: 540px !important;
          min-height: 540px !important;
          max-height: 540px !important;
          overflow: hidden !important;
          padding: 30px 45px !important;
        }
        #slide-viewer .slide:last-child { page-break-after: auto !important; }
        * { -webkit-font-smoothing: antialiased !important; text-rendering: optimizeLegibility !important; }
        .green { color: #8BC34A !important; }
        .red { color: #E53935 !important; }
        .code-block, [style*="background"] { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }

        /* Tighten spacing */
        h1 { font-size: 2.4rem !important; margin-bottom: 15px !important; }
        h2 { font-size: 1.9rem !important; margin-bottom: 15px !important; }
        h3 { font-size: 1.3rem !important; margin-bottom: 10px !important; }
        p { font-size: 1.15rem !important; line-height: 1.4 !important; }
        ul.bullets li { font-size: 1.15rem !important; padding: 6px 0 6px 40px !important; }
        ul.simple li { font-size: 1.05rem !important; padding: 5px 0 !important; }
        .highlight-box { padding: 15px 20px !important; margin-top: 15px !important; }
        .highlight-box p { font-size: 1.1rem !important; }
        .green-box { padding: 15px 20px !important; margin-top: 15px !important; }
        .green-box h4 { font-size: 1.1rem !important; margin-bottom: 6px !important; }
        .green-box p { font-size: 1.05rem !important; }
        .code-block { padding: 16px 20px !important; margin-top: 12px !important; font-size: 0.92rem !important; line-height: 1.5 !important; }
        .code-block p { font-size: 0.92rem !important; margin-bottom: 4px !important; }
        table { margin-top: 12px !important; font-size: 0.98rem !important; }
        table th { padding: 10px 14px !important; }
        table td { padding: 10px 14px !important; }
        .slide-footer { bottom: 10px !important; left: 45px !important; font-size: 0.85rem !important; }
        .slide-num { bottom: 10px !important; right: 20px !important; font-size: 0.8rem !important; }
        .two-col { gap: 28px !important; margin-top: 10px !important; }
        .stats-row { margin-top: 18px !important; }
        .stat .value { font-size: 2.3rem !important; }
      }
    `,
  });

  await page.evaluateHandle('document.fonts.ready');
  await new Promise((resolve) => setTimeout(resolve, 1200));

  const outputPath = path.join(__dirname, 'TempNet-Staffing-Presentation.pdf');

  await page.pdf({
    path: outputPath,
    width: '960px',
    height: '540px',
    printBackground: true,
    preferCSSPageSize: false,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });

  console.log('PDF exported to:', outputPath);
  await browser.close();

  if (process.platform === 'darwin') {
    try {
      execSync(`open "${outputPath}"`);
      console.log('Opened PDF in default viewer.');
    } catch (e) {
      console.log('Run: open', outputPath);
    }
  }

  return outputPath;
}

exportToPDF().catch(console.error);

