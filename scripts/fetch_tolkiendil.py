import html, re, sys, time, unicodedata, urllib.request
from pathlib import Path

search_file, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
dry = '--dry' in sys.argv
out_dir.mkdir(parents=True, exist_ok=True)
page = search_file.read_text(encoding='utf-8')

results = re.findall(
    r'<div class="search_result"><a href="([^"?]+)[^"]*"[^>]*>(.*?)</a>: <span class="search_cnt">(\d+) Occurrence',
    page)

def slug(title):
    t = unicodedata.normalize('NFKD', html.unescape(re.sub(r'<[^>]+>', '', title)))
    t = t.encode('ascii', 'ignore').decode()
    t = re.sub(r'[^A-Za-z0-9]+', '_', t).strip('_')
    return t[:120].rstrip('_') or 'sans_titre'

seen, errors = set(), []
for i, (href, title, cnt) in enumerate(results):
    name = f'{int(cnt):03d}_{slug(title)}'
    base, n = name, 2
    while name in seen:
        name, n = f'{base}_{n}', n + 1
    seen.add(name)
    if dry:
        print(name); continue
    url = 'https://www.tolkiendil.com' + href
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=30).read()
        (out_dir / f'{name}.html').write_bytes(data)
    except Exception as e:
        errors.append(f'{url}: {e}')
    time.sleep(1)

print(f'{len(results)} résultats, {len(seen)} fichiers, {len(errors)} erreurs')
print('\n'.join(errors))
