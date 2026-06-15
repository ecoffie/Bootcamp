const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();

    // Set viewport for 16:9 slides (1280x720)
    await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });

    // Load the HTML file
    const htmlFile = 'live-01-mi-launch.html';
    const htmlPath = path.join(__dirname, htmlFile);
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

    // Create output directory
    const outputDir = path.join(__dirname, 'live-01-pngs');
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    // Get all slides
    const slides = await page.$$('.slide');
    console.log(`Found ${slides.length} slides`);

    // Export each slide
    for (let i = 0; i < slides.length; i++) {
        const slideNum = String(i + 1).padStart(2, '0');
        const filename = `slide-${slideNum}.png`;
        const filepath = path.join(outputDir, filename);

        // Make slide visible
        await page.evaluate((index) => {
            document.querySelectorAll('.slide').forEach((s, i) => {
                s.style.display = i === index ? 'flex' : 'none';
            });
        }, i);

        // Wait for animations
        await new Promise(r => setTimeout(r, 100));

        // Screenshot the visible slide
        await page.screenshot({
            path: filepath,
            type: 'png',
            clip: { x: 0, y: 0, width: 1280, height: 720 }
        });

        console.log(`Exported: ${filename}`);
    }

    await browser.close();
    console.log(`\nDone! All slides exported to: ${outputDir}`);
})();
