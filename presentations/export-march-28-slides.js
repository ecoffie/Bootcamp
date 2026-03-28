const puppeteer = require('puppeteer');
const path = require('path');

async function exportSlides() {
    const browser = await puppeteer.launch({
        headless: 'new',
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    });
    const page = await browser.newPage();

    // Set viewport wide enough
    await page.setViewport({ width: 1200, height: 800 });

    // Load the slides HTML file
    const slidesPath = path.join(__dirname, 'march-28-bootcamp-slides.html');
    await page.goto(`file://${slidesPath}`, { waitUntil: 'networkidle0' });

    // Get all slide positions (absolute, not viewport-relative)
    const slideData = await page.evaluate(() => {
        const slides = document.querySelectorAll('.slide');
        return Array.from(slides).map((slide, i) => {
            const rect = slide.getBoundingClientRect();
            return {
                index: i,
                top: rect.top + window.scrollY,
                left: rect.left + window.scrollX,
                width: rect.width,
                height: rect.height
            };
        });
    });

    console.log(`Found ${slideData.length} slides`);

    for (const slide of slideData) {
        const slideNum = String(slide.index + 1).padStart(2, '0');
        const filename = `march-28-pngs/slide-${slideNum}.png`;

        await page.screenshot({
            path: path.join(__dirname, filename),
            clip: {
                x: slide.left,
                y: slide.top,
                width: 960,
                height: 540
            }
        });

        console.log(`Exported: slide-${slideNum}.png`);
    }

    await browser.close();
    console.log(`\nDone! ${slideData.length} slides exported to march-28-pngs/`);
}

exportSlides().catch(console.error);
