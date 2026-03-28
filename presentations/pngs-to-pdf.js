const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');

async function createPDF() {
    const pngsDir = path.join(__dirname, 'march-28-pngs');
    const files = fs.readdirSync(pngsDir)
        .filter(f => f.endsWith('.png'))
        .sort();

    console.log(`Found ${files.length} slide images`);

    // Create PDF with 16:9 dimensions (960x540 at 72 DPI)
    const doc = new PDFDocument({
        size: [960, 540],
        margins: { top: 0, bottom: 0, left: 0, right: 0 }
    });

    const outputPath = path.join(__dirname, 'March-28-Contract-Vehicles-Bootcamp.pdf');
    doc.pipe(fs.createWriteStream(outputPath));

    for (let i = 0; i < files.length; i++) {
        if (i > 0) doc.addPage();

        const imagePath = path.join(pngsDir, files[i]);
        doc.image(imagePath, 0, 0, { width: 960, height: 540 });
        console.log(`Added: ${files[i]}`);
    }

    doc.end();
    console.log(`\nPDF created: ${outputPath}`);
}

createPDF().catch(console.error);
