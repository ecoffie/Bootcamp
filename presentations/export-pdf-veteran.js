const puppeteer = require('puppeteer');
const path = require('path');
const { execSync } = require('child_process');

async function exportToPDF() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    const slidesPath = path.join(__dirname, 'veteran-vosb-sdvosb-presentation-v2.html');
    await page.goto(`file://${slidesPath}`, { waitUntil: 'networkidle0' });

    await page.addStyleTag({
        content: `
            @media print {
                body { background: white !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
                #nav-bar { display: none !important; }
                #slide-viewer {
                    height: auto !important;
                    overflow: visible !important;
                    scroll-snap-type: none !important;
                }
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
                .code-block, [style*="background"] { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }

                /* Tighten spacing to fit within 540px pages */
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
                .code-block { padding: 18px 22px !important; margin-top: 15px !important; font-size: 0.95rem !important; line-height: 1.5 !important; }
                .code-block p { font-size: 0.95rem !important; margin-bottom: 4px !important; }
                .stats-row { margin-top: 20px !important; }
                .stat .value { font-size: 2.4rem !important; }
                table { margin-top: 15px !important; font-size: 1rem !important; }
                table th { padding: 12px 18px !important; }
                table td { padding: 12px 18px !important; }
                .slide-footer { bottom: 10px !important; left: 45px !important; font-size: 0.85rem !important; }
                .slide-num { bottom: 10px !important; right: 20px !important; font-size: 0.8rem !important; }
                .two-col { gap: 30px !important; margin-top: 10px !important; }

                /* Data-vis slides: constrain images */
                .slide-data-vis .data-vis-image { max-height: 320px !important; }
                .slide-data-vis .data-vis-caption { font-size: 0.85rem !important; margin-top: 8px !important; }

                /* Title slides */
                .slide-title h1 { font-size: 2.5rem !important; }
                .slide-title .subtitle { font-size: 1.5rem !important; margin-bottom: 20px !important; }
            }
        `
    });

    await page.evaluateHandle('document.fonts.ready');
    await new Promise(resolve => setTimeout(resolve, 1500));

    const outputPath = path.join(__dirname, 'Veteran-War-Room-Presentation.pdf');

    await page.pdf({
        path: outputPath,
        width: '960px',
        height: '540px',
        printBackground: true,
        preferCSSPageSize: false,
        margin: { top: 0, right: 0, bottom: 0, left: 0 }
    });

    console.log('PDF exported to:', outputPath);
    await browser.close();

    // Open the PDF (macOS)
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
