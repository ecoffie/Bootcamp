const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.join(__dirname, 'youtube-live-expiring-contracts-png');
const HTML_FILE = path.join(__dirname, 'youtube-live-expiring-contracts-slides.html');
const TOTAL_SLIDES = 25;

async function exportSlides() {
    // Create output directory
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    // Load the HTML file
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
        // Navigate to slide
        await page.evaluate((slideNum) => {
            const slides = document.querySelectorAll('.slide');
            slides.forEach(slide => slide.classList.remove('active'));
            const targetSlide = document.getElementById(`slide-${slideNum}`);
            if (targetSlide) {
                targetSlide.classList.add('active');
                targetSlide.style.transform = 'scale(1)';
            }
        }, i);

        // Wait for any animations
        await new Promise(resolve => setTimeout(resolve, 100));

        // Get the active slide element
        const slideElement = await page.$('.slide.active');

        if (slideElement) {
            const filename = `slide-${String(i).padStart(2, '0')}.png`;
            await slideElement.screenshot({
                path: path.join(OUTPUT_DIR, filename),
                type: 'png'
            });
            console.log(`✓ Exported ${filename}`);
        } else {
            console.log(`✗ Could not find slide ${i}`);
        }
    }

    await browser.close();
    console.log(`\nDone! ${TOTAL_SLIDES} slides exported to ${OUTPUT_DIR}`);
}

exportSlides().catch(console.error);
