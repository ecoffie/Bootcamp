const puppeteer = require('puppeteer');
const path = require('path');

async function exportThumbnails() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Set viewport large enough to fit thumbnails
    await page.setViewport({ width: 1400, height: 2000 });

    // Load the HTML file
    const filePath = path.join(__dirname, 'youtube-live-1-thumbnail.html');
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0' });

    // Get all thumbnails
    const thumbnailCount = await page.evaluate(() => {
        return document.querySelectorAll('.thumbnail').length;
    });

    console.log(`Found ${thumbnailCount} thumbnails. Exporting...`);

    const names = ['money-focus', 'ndaa-focus', 'urgency-focus'];

    // Export each thumbnail
    for (let i = 0; i < thumbnailCount; i++) {
        // Get the thumbnail element and screenshot it
        const thumbElement = await page.evaluateHandle((index) => {
            return document.querySelectorAll('.thumbnail')[index];
        }, i);

        const outputPath = path.join(__dirname, 'youtube-live-1-thumbnails-images', `thumbnail-${i + 1}-${names[i]}.png`);

        await thumbElement.screenshot({ path: outputPath });
        console.log(`Exported thumbnail ${i + 1}/${thumbnailCount}: thumbnail-${i + 1}-${names[i]}.png`);
    }

    await browser.close();
    console.log('\nAll thumbnails exported to youtube-live-1-thumbnails-images/');
}

exportThumbnails().catch(console.error);
