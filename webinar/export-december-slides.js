const puppeteer = require('puppeteer');
const path = require('path');

async function exportSlides() {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    await page.setViewport({ width: 1920, height: 1080 });

    const slidesPath = path.join(__dirname, 'slides.html');
    await page.goto(`file://${slidesPath}`, { waitUntil: 'networkidle0' });

    const totalSlides = 17;
    const outputDir = path.join(__dirname, 'december-slides-images');

    console.log(`Exporting ${totalSlides} December slides to ${outputDir}...`);

    for (let i = 1; i <= totalSlides; i++) {
        await page.evaluate((slideNum) => {
            document.querySelectorAll('.slide').forEach(slide => {
                slide.classList.remove('active');
            });
            document.querySelector(`[data-slide="${slideNum}"]`).classList.add('active');
        }, i);

        await new Promise(resolve => setTimeout(resolve, 200));

        const filename = `slide-${String(i).padStart(2, '0')}.png`;
        await page.screenshot({
            path: path.join(outputDir, filename),
            fullPage: false
        });

        console.log(`  ✓ Exported ${filename}`);
    }

    await browser.close();
    console.log(`\nDone! ${totalSlides} slides exported to december-slides-images/`);
}

exportSlides().catch(console.error);
