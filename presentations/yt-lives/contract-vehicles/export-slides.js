const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();

    // Set viewport for 16:9 slides (1280x720)
    await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });

    // Load the HTML file - change this for different lives
    const liveNumber = process.argv[2] || '01';
    const liveFiles = {
        '01': 'live-01-idiq-guide.html',
        '02': 'live-02-vehicles-breakdown.html',
        '03': 'live-03-sources-sought.html',
        '03v2': 'live-03-sources-sought-v2.html',
        '04': 'live-04-final-call.html',
        '04v2': 'live-04-final-call-v2.html'
    };
    const htmlFile = liveFiles[liveNumber] || liveFiles['01'];
    const htmlPath = path.join(__dirname, htmlFile);
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

    // Create output directory
    const outputDir = path.join(__dirname, `live-${liveNumber}-pngs`);
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    // Get all slides
    const slides = await page.$$('.slide');
    console.log(`Found ${slides.length} slides`);

    // Export each slide at consistent 1280x720
    for (let i = 0; i < slides.length; i++) {
        const slideNum = String(i + 1).padStart(2, '0');
        const filename = `slide-${slideNum}.png`;
        const filepath = path.join(outputDir, filename);

        // Screenshot the slide element with clip to ensure 16:9
        await slides[i].screenshot({
            path: filepath,
            type: 'png'
        });

        console.log(`Exported: ${filename}`);
    }

    // Export the CTA box as a slide
    const ctaBox = await page.$('.cta-box');
    if (ctaBox) {
        await ctaBox.screenshot({
            path: path.join(outputDir, 'slide-11-cta.png'),
            type: 'png'
        });
        console.log('Exported: slide-11-cta.png');
    }

    await browser.close();
    console.log(`\nDone! All slides exported to: ${outputDir}`);
})();
