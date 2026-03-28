const puppeteer = require('puppeteer');
const path = require('path');

async function exportPDF() {
    const browser = await puppeteer.launch({
        headless: true,
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    // Set viewport
    await page.setViewport({ width: 960, height: 540 });

    // Load the slides HTML file
    const slidesPath = path.join(__dirname, 'march-28-bootcamp-slides.html');
    await page.goto(`file://${slidesPath}`, { waitUntil: 'networkidle0' });

    // Export to PDF with slide dimensions
    const outputPath = path.join(__dirname, 'March-28-Contract-Vehicles-Bootcamp.pdf');

    await page.pdf({
        path: outputPath,
        width: '960px',
        height: '540px',
        printBackground: true,
        margin: { top: 0, right: 0, bottom: 0, left: 0 },
        preferCSSPageSize: true
    });

    await browser.close();
    console.log(`PDF created: ${outputPath}`);
}

exportPDF().catch(console.error);
