const puppeteer = require('puppeteer');
const path = require('path');

async function exportSlides() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Set viewport to 1280x720 (YouTube thumbnail/slide size)
    await page.setViewport({ width: 1280, height: 720 });

    // Load the slides HTML file
    const slidesPath = path.join(__dirname, 'slides.html');
    await page.goto(`file://${slidesPath}`, { waitUntil: 'networkidle0' });

    const totalSlides = 17;

    for (let i = 1; i <= totalSlides; i++) {
        // Navigate to slide
        await page.evaluate((slideNum) => {
            showSlide(slideNum);
        }, i);

        // Wait for any transitions
        await new Promise(resolve => setTimeout(resolve, 300));

        // Screenshot the slide
        const filename = `slide-exports/slide-${String(i).padStart(2, '0')}.png`;
        await page.screenshot({
            path: path.join(__dirname, filename),
            type: 'png'
        });

        console.log(`Exported: ${filename}`);
    }

    await browser.close();
    console.log('\nDone! All 17 slides exported to slide-exports/');
}

exportSlides().catch(console.error);
