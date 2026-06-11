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
        '01': 'live-01-replace-samgov.html',
        '02': 'live-02-750b-market.html',
        '03': 'live-03-never-sleeps.html',
        '04': 'live-04-build-week.html',
        '05': 'live-05-lockheed-alternative.html'
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

    // Export each slide at consistent 1280x720.
    // Slides are display:none unless .active — force each one visible before the shot.
    for (let i = 0; i < slides.length; i++) {
        const slideNum = String(i + 1).padStart(2, '0');
        const filename = `slide-${slideNum}.png`;
        const filepath = path.join(outputDir, filename);

        await page.evaluate((idx) => {
            const all = document.querySelectorAll('.slide');
            all.forEach((s, j) => { s.style.display = (j === idx) ? 'flex' : 'none'; });
        }, i);

        await slides[i].screenshot({
            path: filepath,
            type: 'png'
        });

        console.log(`Exported: ${filename}`);
    }

    await browser.close();
    console.log(`\nDone! All slides exported to: ${outputDir}`);
})();
