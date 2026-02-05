const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

async function captureSlides() {
  const htmlPath = path.join(__dirname, 'youtube-live-bootcamp-recap-slides.html');
  const outputDir = path.join(__dirname, 'bootcamp-recap-slides-png');

  // Create output directory
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Find Chrome
  const chromePaths = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
  ];

  let executablePath = null;
  for (const p of chromePaths) {
    if (fs.existsSync(p)) {
      executablePath = p;
      break;
    }
  }

  if (!executablePath) {
    console.error('No Chrome/Chromium found');
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    executablePath,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

  // Get the number of slides dynamically
  const totalSlides = await page.evaluate(() => {
    return document.querySelectorAll('.slide').length;
  });

  console.log(`Found ${totalSlides} slides. Capturing...`);

  for (let i = 0; i < totalSlides; i++) {
    // Scroll to slide
    await page.evaluate((index) => {
      const slides = document.querySelectorAll('.slide');
      slides[index].scrollIntoView({ behavior: 'instant' });
    }, i);

    await new Promise(r => setTimeout(r, 200));

    // Screenshot the slide element directly
    const slideHandle = await page.evaluateHandle((index) => {
      return document.querySelectorAll('.slide')[index];
    }, i);

    const slideNum = String(i + 1).padStart(2, '0');
    const outputPath = path.join(outputDir, `slide-${slideNum}.png`);

    await slideHandle.asElement().screenshot({ path: outputPath, type: 'png' });
    console.log(`Captured slide ${i + 1}/${totalSlides}`);
  }

  await browser.close();
  console.log(`\nDone! ${totalSlides} slides saved to: ${outputDir}`);
}

captureSlides().catch(console.error);
