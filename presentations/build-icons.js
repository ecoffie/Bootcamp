// Inlines Lucide icons (<i data-icon>) and screenshot frames (<div data-shot>) into a deck.
// Usage: node presentations/build-icons.js src.html out.html
const fs=require('fs'),path=require('path');
const [,,src,out]=process.argv;
const ICONS=path.join(__dirname,'icons','lucide'), SHOTS=path.join(__dirname,'screenshots');
let html=fs.readFileSync(src,'utf8');
const cache={};
const svg=n=>cache[n]||(cache[n]=fs.readFileSync(path.join(ICONS,n+'.svg'),'utf8').replace(/<!--[\s\S]*?-->/g,'').trim());
html=html.replace(/<i[^>]*\bdata-icon="([^"]+)"[^>]*><\/i>/g,(m,n)=>`<span class="luc">${svg(n)}</span>`);
let real=0,ph=0;
html=html.replace(/<div class="shot" data-shot="([^"]+)"(?: data-url="([^"]*)")?><\/div>/g,(m,n,url)=>{
  const label=url||('getmindy.ai / '+n);
  const bar=`<div class="shot-bar"><span class="shot-dot d-r"></span><span class="shot-dot d-y"></span><span class="shot-dot d-g"></span><span class="shot-url">${label.replace(/ /g,'&nbsp;')}</span></div>`;
  if(fs.existsSync(path.join(SHOTS,n+'.png'))){real++;return `<div class="shot-wrap">${bar}<img src="screenshots/${n}.png"></div>`;}
  ph++;return `<div class="shot-wrap">${bar}<div class="shot-ph"><b>📸  Drop screenshot</b><span>screenshots/${n}.png</span></div></div>`;
});
fs.writeFileSync(out,html);
console.log(`built ${out} | real screenshots: ${real} | placeholders: ${ph}`);
