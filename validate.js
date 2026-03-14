const fs = require('fs');
const html = fs.readFileSync('game/index.html', 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (m === null) { console.log('No script tag'); process.exit(1); }
try {
  new Function(m[1]);
  console.log('JS syntax: OK');
} catch(e) {
  console.log('JS syntax ERROR:', e.message);
}
console.log('Size:', Math.round(html.length/1024) + 'KB');
console.log('Lines:', html.split('\n').length);
