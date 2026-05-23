"""Generate sitemap.xml from the actual built HTML files."""
from pathlib import Path
import datetime

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://gtsriskadvisory.com'
TODAY = datetime.date.today().isoformat()

SKIP_DIRS = {'_assemble', 'admin', 'assets', 'data', 'partials'}
SKIP_FILES = {'404.html'}


def collect_urls():
    urls = []
    for p in ROOT.rglob('*.html'):
        rel = p.relative_to(ROOT).as_posix()
        # Skip helper directories
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        if p.name in SKIP_FILES:
            continue
        # Convert /path/index.html to /path/, /file.html stays as /file.html
        if rel.endswith('/index.html'):
            url = '/' + rel[:-len('index.html')]
        elif rel == 'index.html':
            url = '/'
        else:
            url = '/' + rel
        urls.append(url)
    return sorted(set(urls))


def write_sitemap():
    urls = collect_urls()
    body = '<?xml version="1.0" encoding="UTF-8"?>\n'
    body += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        priority = '1.0' if u == '/' else ('0.9' if u.count('/') <= 2 else '0.7')
        body += f'  <url>\n    <loc>{BASE}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{priority}</priority>\n  </url>\n'
    body += '</urlset>\n'
    (ROOT / 'sitemap.xml').write_text(body, encoding='utf-8')
    print(f'sitemap.xml written: {len(urls)} URLs')


if __name__ == '__main__':
    write_sitemap()
