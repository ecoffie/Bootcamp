const fs = require('fs');
const path = require('path');

const inputFile = '/Users/ericcoffie/Bootcamp/youtube-live-expiring-contracts-slides.html';
const outputDir = '/Users/ericcoffie/Bootcamp/youtube-live-expiring-contracts-slides';

// Create output directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

const html = fs.readFileSync(inputFile, 'utf8');

// Extract styles (everything between <style> and </style>)
const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
const styles = styleMatch ? styleMatch[1] : '';

// Find all slide comment positions
const slideCommentRegex = /<!-- SLIDE (\d+):/g;
const slidePositions = [];
let match;
while ((match = slideCommentRegex.exec(html)) !== null) {
    slidePositions.push({ num: match[1], pos: match.index });
}

// Extract each slide by finding content between comments
let count = 0;
for (let i = 0; i < slidePositions.length; i++) {
    const slideNum = slidePositions[i].num;
    const startPos = slidePositions[i].pos;

    let endPos;
    if (i < slidePositions.length - 1) {
        endPos = slidePositions[i + 1].pos;
    } else {
        // Last slide - find the closing </div> for slide-container
        const slideContainerEnd = html.indexOf('\n    </div>\n\n    <div class="slide-counter">', startPos);
        endPos = slideContainerEnd > 0 ? slideContainerEnd : html.length;
    }

    let slideContent = html.substring(startPos, endPos).trim();

    // Remove the comment line
    slideContent = slideContent.replace(/<!-- SLIDE \d+:[^>]*-->\s*/, '');

    // Clean up any trailing content
    if (slideContent.endsWith('-->')) {
        slideContent = slideContent.substring(0, slideContent.lastIndexOf('<!--')).trim();
    }

    // Make slide visible (add active class)
    slideContent = slideContent.replace('class="slide ', 'class="slide active ');
    slideContent = slideContent.replace('class="slide"', 'class="slide active"');

    const slideHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080">
    <title>Slide ${slideNum} - $221B Expiring Contracts</title>
    <style>
${styles}
        /* Override for single slide display */
        body {
            margin: 0;
            padding: 0;
            width: 1920px;
            height: 1080px;
            overflow: hidden;
        }
        .slide {
            display: flex !important;
            width: 1920px;
            height: 1080px;
        }
        .slide-container {
            width: 1920px;
            height: 1080px;
        }
    </style>
</head>
<body>
    <div class="slide-container">
    ${slideContent}
    </div>
</body>
</html>`;

    const paddedNum = slideNum.padStart(2, '0');
    const outputFile = path.join(outputDir, `slide-${paddedNum}.html`);
    fs.writeFileSync(outputFile, slideHtml);
    console.log(`Created: slide-${paddedNum}.html`);
    count++;
}

console.log(`\nDone! ${count} slides exported to:\n${outputDir}`);
