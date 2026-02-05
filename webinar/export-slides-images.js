const puppeteer = require('puppeteer');
const path = require('path');

async function exportSlides() {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // Set viewport to 1920x1080 for HD slides
    await page.setViewport({ width: 1920, height: 1080 });

    // Load the slides
    const slidesPath = path.join(__dirname, 'january-2026-slides.html');
    await page.goto(`file://${slidesPath}`, { waitUntil: 'networkidle0' });

    const totalSlides = 17;
    const outputDir = path.join(__dirname, 'slides-images');

    console.log(`Exporting ${totalSlides} slides to ${outputDir}...`);

    for (let i = 1; i <= totalSlides; i++) {
        // Navigate to slide
        await page.evaluate((slideNum) => {
            document.querySelectorAll('.slide').forEach(slide => {
                slide.classList.remove('active');
            });
            document.querySelector(`[data-slide="${slideNum}"]`).classList.add('active');
        }, i);

        // Wait for any animations
        await new Promise(resolve => setTimeout(resolve, 200));

        // Take screenshot
        const filename = `slide-${String(i).padStart(2, '0')}.png`;
        await page.screenshot({
            path: path.join(outputDir, filename),
            fullPage: false
        });

        console.log(`  ✓ Exported ${filename}`);
    }

    await browser.close();
    console.log(`\nDone! ${totalSlides} slides exported to slides-images/`);
}

exportSlides().catch(console.error);
