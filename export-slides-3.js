const puppeteer = require('puppeteer');
const path = require('path');

async function exportSlides() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Set viewport to slide dimensions
    await page.setViewport({ width: 1920, height: 1080 });

    // Load the HTML file
    const filePath = path.join(__dirname, 'youtube-live-3-slides.html');
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0' });

    // Get all slides
    const slideCount = await page.evaluate(() => {
        return document.querySelectorAll('.slide').length;
    });

    console.log(`Found ${slideCount} slides. Exporting...`);

    // Export each slide
    for (let i = 0; i < slideCount; i++) {
        // Scroll to the slide
        await page.evaluate((index) => {
            const slides = document.querySelectorAll('.slide');
            slides[index].scrollIntoView();
        }, i);

        // Wait a moment for any animations
        await new Promise(resolve => setTimeout(resolve, 100));

        // Get the slide element and screenshot it
        const slideElement = await page.evaluateHandle((index) => {
            return document.querySelectorAll('.slide')[index];
        }, i);

        const slideNumber = String(i + 1).padStart(2, '0');
        const outputPath = path.join(__dirname, 'youtube-live-3-slides-images', `slide-${slideNumber}.png`);

        await slideElement.screenshot({ path: outputPath });
        console.log(`Exported slide ${i + 1}/${slideCount}: slide-${slideNumber}.png`);
    }

    await browser.close();
    console.log('\nAll slides exported to youtube-live-3-slides-images/');
}

exportSlides().catch(console.error);
