// Injecte scripts/nav-verticale.js dans le HTML produit par Marp.
// Usage : node scripts/inject-nav.mjs 3-presentation/tolkien.html
import { readFileSync, writeFileSync } from 'node:fs';

const file = process.argv[2];
const js = readFileSync(new URL('./nav-verticale.js', import.meta.url), 'utf8');
const html = readFileSync(file, 'utf8');
const tag = `<script id="nav-verticale">\n${js}</script>`;

if (html.includes('id="nav-verticale"')) process.exit(0);
const i = html.lastIndexOf('</body>');
if (i < 0) throw new Error(`</body> introuvable dans ${file}`);
writeFileSync(file, html.slice(0, i) + tag + html.slice(i));
console.log(`Navigation verticale injectée dans ${file}`);
