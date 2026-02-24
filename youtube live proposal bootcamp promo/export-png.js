const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.join(__dirname, 'slides-png');
const HTML_FILE = path.join(__dirname, 'youtube-live-proposal-bootcamp-slides.html');
const TOTAL_SLIDES = 31;

async function exportSlides() {
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    await page.goto(`file://${HTML_FILE}`, { waitUntil: 'networkidle0' });

    // Hide navigation elements
    await page.evaluate(() => {
        const navHint = document.querySelector('.nav-hint');
        const slideCounter = document.querySelector('.slide-counter');
        if (navHint) navHint.style.display = 'none';
        if (slideCounter) slideCounter.style.display = 'none';
    });

    console.log(`Exporting ${TOTAL_SLIDES} slides to ${OUTPUT_DIR}...`);

    for (let i = 1; i <= TOTAL_SLIDES; i++) {
        // Show only current slide
        await page.evaluate((slideNum) => {
            const slides = document.querySelectorAll('.slide');
            slides.forEach((slide, index) => {
                slide.style.display = (index === slideNum - 1) ? 'flex' : 'none';
            });
        }, i);

        await new Promise(resolve => setTimeout(resolve, 100));

        const filename = `slide-${String(i).padStart(2, '0')}.png`;
        await page.screenshot({
            path: path.join(OUTPUT_DIR, filename),
            type: 'png'
        });
        console.log(`✓ Exported ${filename}`);
    }

    await browser.close();
    console.log(`\nDone! ${TOTAL_SLIDES} slides exported to ${OUTPUT_DIR}`);
}

exportSlides().catch(console.error);
