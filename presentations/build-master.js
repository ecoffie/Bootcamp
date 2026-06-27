#!/usr/bin/env node
/*
 * build-master.js — stitch the three Mindy Launch decks into one master file.
 *
 *   node presentations/build-master.js
 *
 * Reads the three standalone source decks, namespaces each one's CSS so their
 * clashing class definitions (.bignum, .title, .shot-wrap, .tool, .cost ...)
 * can coexist, concatenates the slides, and writes:
 *
 *   presentations/mindy-launch-master.src.html   (stitched source, icon/shot tokens intact)
 *   presentations/mindy-launch-master.html       (built — icons + screenshots inlined)
 *
 * Edit any of the source decks, then re-run this to rebuild the master in one shot.
 *
 * How the scoping works: each deck is wrapped in a `.dwrap` element set to
 * `display:contents` (so the wrapper box vanishes and flex-centering on <body>
 * is preserved), and every rule in that deck's stylesheet is prefixed with the
 * deck's scope class (.dOPEN / .dFEAT / .dCLOSE). `*`/`body` rules are emitted
 * once (shared), and @keyframes / @font-face / @media stay global.
 */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const DIR = __dirname;
const OUT_SRC = 'mindy-launch-master.src.html';
const OUT_HTML = 'mindy-launch-master.html';

// Order matters — this is the play order of the keynote.
// `injectAt: 'MARKER'` decks are spliced into another deck's body at the
// matching `<!--INJECT:MARKER-->` comment instead of being appended.
const DECKS = [
  { scope: 'dOPEN',  file: 'mindy-launch-opening.src.html',       label: 'OPENING + BIG PICTURE' },
  { scope: 'dFEAT',  file: 'mindy-launch-demo-features.src.html', label: 'FEATURE DEMOS' },
  { scope: 'dINT',   file: 'mindy-launch-ai-interlude.src.html',  label: 'AI / GROUNDING INTERLUDE', injectAt: 'AI_INTERLUDE' },
  { scope: 'dMISSION', file: 'mindy-launch-mission-closer.src.html', label: 'THE MISSION (closer)' },
  { scope: 'dCLOSE', file: 'mindy-launch-demo-close.src.html',    label: 'OFFER & CLOSE' },
];

function readParts(file) {
  const p = path.join(DIR, file);
  if (!fs.existsSync(p)) {
    console.error(`✗ missing source deck: ${file}`);
    process.exit(1);
  }
  const h = fs.readFileSync(p, 'utf8');
  if (!h.includes('<style>') || !h.includes('<body>')) {
    console.error(`✗ ${file} is missing a <style> or <body> block`);
    process.exit(1);
  }
  const css = h.split('<style>')[1].split('</style>')[0];
  const body = h.split('<body>')[1].split('<script>')[0];
  return { css, body };
}

const sharedGlobal = new Map(); // prelude -> full rule (deduped: *, body, html)
const keyframes = [];           // @keyframes / @font-face / @media — kept global

function scopeCSS(css, scope) {
  css = css.replace(/\/\*[\s\S]*?\*\//g, ''); // strip comments
  let i = 0, n = css.length, out = [];
  while (i < n) {
    while (i < n && /\s/.test(css[i])) i++;          // skip whitespace
    if (i >= n) break;
    const pstart = i;
    while (i < n && css[i] !== '{') i++;             // read prelude up to '{'
    const prelude = css.slice(pstart, i).trim();
    if (i >= n) break;
    let depth = 0, bstart = i;                        // read balanced { ... }
    do { if (css[i] === '{') depth++; else if (css[i] === '}') depth--; i++; } while (i < n && depth > 0);
    const block = css.slice(bstart, i);
    if (!prelude) continue;

    if (/^@(-webkit-)?keyframes/i.test(prelude) || /^@font-face/i.test(prelude) ||
        /^@media/i.test(prelude) || /^@supports/i.test(prelude)) {
      keyframes.push(prelude + block);               // global — names must stay un-namespaced
      continue;
    }
    const sels = prelude.split(',').map(s => s.trim());
    const onlyGlobal = sels.every(s => s === '*' || s === 'body' || s === 'html');
    if (onlyGlobal) {
      sels.forEach(s => { if (!sharedGlobal.has(s)) sharedGlobal.set(s, s + block); });
    } else {
      const scoped = sels
        .map(s => (s === '*' || s === 'body' || s === 'html') ? s : `.${scope} ${s}`)
        .join(',');
      out.push(scoped + block);
    }
  }
  return out.join('\n');
}

const scopedBlocks = [];
const injections = {};   // marker -> wrapped body to splice in
let masterBody = '';
let total = 0;
for (const d of DECKS) {
  const { css, body } = readParts(d.file);
  const count = (body.match(/class="slide/g) || []).length;
  total += count;
  scopedBlocks.push(`  /* ===== ${d.label} (${count} slides) ===== */\n` + scopeCSS(css, d.scope));
  const wrapped = `\n<!-- ================= ${d.label} ================= -->\n<div class="dwrap ${d.scope}">\n${body}\n</div>\n`;
  if (d.injectAt) {
    injections[d.injectAt] = wrapped;
    console.log(`  • ${d.label.padEnd(26)} ${String(count).padStart(3)} slides  → injected @ ${d.injectAt}`);
  } else {
    masterBody += wrapped;
    console.log(`  • ${d.label.padEnd(26)} ${String(count).padStart(3)} slides  (${d.file})`);
  }
}

// Splice injection decks into their markers.
for (const [marker, wrapped] of Object.entries(injections)) {
  const tag = `<!--INJECT:${marker}-->`;
  if (!masterBody.includes(tag)) {
    console.error(`✗ injection marker ${tag} not found in any appended deck`);
    process.exit(1);
  }
  masterBody = masterBody.replace(tag, wrapped);
}

const headCSS =
  `*{margin:0;padding:0;box-sizing:border-box}\n` +
  `.dwrap{display:contents}\n` +
  [...sharedGlobal.values()].filter(r => !r.startsWith('*')).join('\n') + '\n' +
  keyframes.join('\n') + '\n' +
  scopedBlocks.join('\n');

const script = `
  document.querySelectorAll('.dotfield').forEach(d=>{const k=+d.dataset.n||0;for(let i=0;i<k;i++)d.appendChild(document.createElement('span'));});
  let currentSlide=0;const slides=document.querySelectorAll('.slide');
  slides.forEach((s,i)=>{const t=(i+1)+' / '+slides.length;let e=s.querySelector('.slide-number');if(!e){e=document.createElement('div');e.className='slide-number';s.appendChild(e);}e.textContent=t;});
  function showSlide(n){slides[currentSlide].classList.remove('active');currentSlide=(n+slides.length)%slides.length;slides[currentSlide].classList.add('active');slides[currentSlide].scrollIntoView({block:'nearest'});}
  function nextSlide(){showSlide(currentSlide+1)}function prevSlide(){showSlide(currentSlide-1)}
  document.addEventListener('keydown',(e)=>{if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();nextSlide();}if(e.key==='ArrowLeft')prevSlide();});
  document.addEventListener('click',(e)=>{if(e.target.closest('a'))return;nextSlide();});
  slides[0].classList.add('active');
`;

const out = `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>The Mindy Launch — Master Deck (Opening · Demo · Close)</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800;900&display=swap" rel="stylesheet">
<style>
body{font-family:'Inter',system-ui,sans-serif;background:#0f172a;color:#fff;display:flex;justify-content:center;flex-wrap:wrap}
${headCSS}
</style></head><body>
${masterBody}
<script>${script}</script>
</body></html>`;

fs.writeFileSync(path.join(DIR, OUT_SRC), out);
console.log(`\n✓ stitched ${total} slides → presentations/${OUT_SRC}`);

// Inline icons + screenshots into the final master.
try {
  const res = execFileSync('node', [path.join(DIR, 'build-icons.js'), path.join(DIR, OUT_SRC), path.join(DIR, OUT_HTML)], { encoding: 'utf8' });
  process.stdout.write(res);
} catch (e) {
  console.error('✗ build-icons.js failed:', e.message);
  process.exit(1);
}
