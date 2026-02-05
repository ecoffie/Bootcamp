const puppeteer = require('puppeteer');
const path = require('path');

async function exportToPDF() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Load the slides HTML file
    const slidesPath = path.join(__dirname, 'january-2026-bootcamp-slides-v2.html');
    await page.goto(`file://${slidesPath}`, { waitUntil: 'networkidle0' });

    // Add print-specific styles for better readability
    await page.addStyleTag({
        content: `
            @media print {
                body {
                    background: white !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
                .slide {
                    margin: 0 !important;
                    box-shadow: none !important;
                    page-break-after: always !important;
                    page-break-inside: avoid !important;
                    width: 960px !important;
                    height: 540px !important;
                }
                /* Ensure text is crisp */
                * {
                    -webkit-font-smoothing: antialiased !important;
                    text-rendering: optimizeLegibility !important;
                }
                /* Make sure colors print correctly */
                .green { color: #8BC34A !important; }
                .red { color: #E53935 !important; }
                /* Ensure backgrounds print */
                [style*="background"] {
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
            }
        `
    });

    // Wait for fonts to load
    await page.evaluateHandle('document.fonts.ready');
    await new Promise(resolve => setTimeout(resolve, 1000));

    const outputPath = path.join(__dirname, 'January-2026-GovCon-Bootcamp-Slides.pdf');

    await page.pdf({
        path: outputPath,
        width: '960px',
        height: '540px',
        printBackground: true,
        preferCSSPageSize: true,
        margin: { top: 0, right: 0, bottom: 0, left: 0 }
    });

    console.log(`PDF exported to: ${outputPath}`);
    await browser.close();
}

exportToPDF().catch(console.error);
