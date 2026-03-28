const PptxGenJS = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

async function createPptx() {
    const pptx = new PptxGenJS();

    // Set presentation properties
    pptx.author = 'GovCon Giants';
    pptx.title = 'Contract Vehicles Bootcamp - March 28, 2026';
    pptx.subject = 'Master IDIQs, GWACs, Qualifications & Team Building';

    // Set slide dimensions to 16:9 widescreen (matches 960x540 ratio)
    pptx.defineLayout({ name: 'CUSTOM', width: 10, height: 5.625 });
    pptx.layout = 'CUSTOM';

    const pngsDir = path.join(__dirname, 'march-28-pngs');
    const files = fs.readdirSync(pngsDir)
        .filter(f => f.endsWith('.png'))
        .sort();

    console.log(`Found ${files.length} slide images`);

    for (const file of files) {
        const slide = pptx.addSlide();
        const imagePath = path.join(pngsDir, file);

        // Add image covering full slide
        slide.addImage({
            path: imagePath,
            x: 0,
            y: 0,
            w: '100%',
            h: '100%'
        });

        console.log(`Added: ${file}`);
    }

    const outputPath = path.join(__dirname, 'March-28-Contract-Vehicles-Bootcamp.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`\nPowerPoint created: ${outputPath}`);
}

createPptx().catch(console.error);
