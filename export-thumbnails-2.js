const puppeteer = require('puppeteer');
const path = require('path');

async function exportThumbnails() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Set viewport to thumbnail dimensions
    await page.setViewport({ width: 1280, height: 720 });

    // Load the HTML file
    const filePath = path.join(__dirname, 'youtube-live-2-thumbnail.html');
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0' });

    // Get all thumbnails
    const thumbnailCount = await page.evaluate(() => {
        return document.querySelectorAll('.thumbnail').length;
    });

    console.log(`Found ${thumbnailCount} thumbnails. Exporting...`);

    const names = [
        'thumbnail-1-big-number.png',
        'thumbnail-2-pain-opportunity.png',
        'thumbnail-3-agency-quote.png'
    ];

    // Export each thumbnail
    for (let i = 0; i < thumbnailCount; i++) {
        const thumbnailElement = await page.evaluateHandle((index) => {
            return document.querySelectorAll('.thumbnail')[index];
        }, i);

        const outputPath = path.join(__dirname, 'youtube-live-2-thumbnails-images', names[i]);

        await thumbnailElement.screenshot({ path: outputPath });
        console.log(`Exported thumbnail ${i + 1}/${thumbnailCount}: ${names[i]}`);
    }

    await browser.close();
    console.log('\nAll thumbnails exported to youtube-live-2-thumbnails-images/');
}

exportThumbnails().catch(console.error);
