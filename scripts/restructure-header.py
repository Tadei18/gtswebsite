#!/usr/bin/env python3
"""
Restructure the site header into a two-column CSS grid: a dedicated brand
block (full stacked logo) in the top-left corner spanning both the
pre-header strip and the main nav row, with all other header content in
the right column.

The current pre-header + header block is byte-identical across every
inlined page, so we extract it once from index.html, transform it, and do
an exact old→new string replacement everywhere it appears.

Idempotent: files already carrying the new .site-header block are skipped.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_START = '  <div class="pre-header">'
OLD_END_TOKEN = '  </header>'


def extract_old_block(text: str) -> str | None:
    s = text.find(OLD_START)
    e = text.find(OLD_END_TOKEN)
    if s == -1 or e == -1:
        return None
    return text[s:e + len(OLD_END_TOKEN)]


def match_div(html: str, open_idx: int) -> int:
    """Given index of a '<div' opening tag, return index just past its matching '</div>'."""
    depth = 0
    i = open_idx
    while i < len(html):
        nxt_open = html.find('<div', i)
        nxt_close = html.find('</div>', i)
        if nxt_close == -1:
            raise ValueError('unbalanced div')
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            i = nxt_open + 4
        else:
            depth -= 1
            i = nxt_close + len('</div>')
            if depth == 0:
                return i
    raise ValueError('unbalanced div')


def extract_inner(old_block: str) -> tuple[str, str, str]:
    # pre-header__inner (balanced)
    pi = old_block.find('<div class="pre-header__inner">')
    pre_inner = old_block[pi:match_div(old_block, pi)]

    # nav (no nested <nav>)
    ns = old_block.find('<nav class="nav"')
    ne = old_block.find('</nav>', ns) + len('</nav>')
    nav = old_block[ns:ne]

    # header__cta (balanced)
    cs = old_block.find('<div class="header__cta">')
    cta = old_block[cs:match_div(old_block, cs)]

    return pre_inner, nav, cta


def build_new_block(pre_inner: str, nav: str, cta: str) -> str:
    return (
'  <header class="site-header" id="site-header">\n'
'    <div class="site-header__grid">\n'
'      <a href="/" class="brand-block" aria-label="GTS Risk Advisory — home">\n'
'        <picture>\n'
'          <source media="(max-width: 900px)" srcset="/assets/img/brand/gts-shield.png">\n'
'          <img src="/assets/img/brand/gts-logo-full.svg" alt="GTS Security &amp; Risk Consulting" class="brand-block__logo">\n'
'        </picture>\n'
'      </a>\n'
'      <div class="site-header__main">\n'
'        <div class="pre-header">\n'
'          ' + pre_inner + '\n'
'        </div>\n'
'        <div class="primary-nav">\n'
'          ' + nav + '\n'
'          ' + cta + '\n'
'        </div>\n'
'      </div>\n'
'    </div>\n'
'  </header>'
    )


def main() -> int:
    ref_text = (ROOT / 'index.html').read_text(encoding='utf-8')
    old_block = extract_old_block(ref_text)
    if not old_block:
        print('Could not locate old block in index.html', file=sys.stderr)
        return 1

    pre_inner, nav, cta = extract_inner(old_block)
    new_block = build_new_block(pre_inner, nav, cta)

    # Sanity: the new block must still carry the key nav landmarks.
    for needle in ['data-active-paths="/intelligence/,/insights/"', 'class="nav-toggle"', 'id="intel-dropdown-posts"']:
        assert needle in new_block, f'new block missing {needle}'

    count = 0
    for p in sorted(ROOT.rglob('*.html')):
        text = p.read_text(encoding='utf-8')
        if old_block in text:
            p.write_text(text.replace(old_block, new_block), encoding='utf-8')
            count += 1
            print(f'  {p.relative_to(ROOT).as_posix()}')
    print(f'\nRestructured {count} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
