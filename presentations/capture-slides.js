const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function captureSlides() {
    const outputDir = path.join(__dirname, 'january-bootcamp-slides-images');

    // Create output directory if it doesn't exist
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Set viewport to match slide dimensions (960x540 is 16:9)
    await page.setViewport({ width: 960, height: 540 });

    // Load the slides HTML file
    const slidesPath = path.join(__dirname, 'january-2026-bootcamp-slides-v2.html');
    await page.goto(`file://${slidesPath}`, { waitUntil: 'networkidle0' });

    // Get all slides
    const slideCount = await page.evaluate(() => {
        return document.querySelectorAll('.slide').length;
    });

    console.log(`Found ${slideCount} slides to export...`);

    for (let i = 0; i < slideCount; i++) {
        // Get the slide element and scroll it into view
        const slideElement = await page.evaluateHandle((index) => {
            const slides = document.querySelectorAll('.slide');
            const slide = slides[index];
            slide.scrollIntoView();
            return slide;
        }, i);

        // Wait a moment for fonts/styles to render
        await new Promise(resolve => setTimeout(resolve, 200));

        // Screenshot just this slide
        const filename = `slide-${String(i + 1).padStart(2, '0')}.png`;
        await slideElement.screenshot({
            path: path.join(outputDir, filename),
            type: 'png'
        });

        console.log(`Exported: ${filename}`);
    }

    await browser.close();
    console.log(`\nDone! ${slideCount} slides exported to: ${outputDir}`);
    console.log('\nNext steps:');
    console.log('1. Go to Google Slides: slides.google.com');
    console.log('2. Create a new presentation');
    console.log('3. For each slide: Insert > Image > Upload from computer');
    console.log('4. Or use "Insert > Image > Upload" and select all images at once');
}

captureSlides().catch(console.error);
