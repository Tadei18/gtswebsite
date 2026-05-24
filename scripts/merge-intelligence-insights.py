#!/usr/bin/env python3
"""
One-shot merge of the standalone "Intelligence" and "Insights" top-level
nav items into a single "Intelligence" mega-menu dropdown (desktop) and
accordion (mobile).

Idempotent — re-running on a merged tree is a no-op.

Indentation is captured from the OLD markup and propagated to the NEW block
so the output stays diff-friendly in both partials/ (10-space indent) and
inlined pages (12-space indent).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- Desktop: replace the two standalone <li>s with a single dropdown <li> ---
DESKTOP_OLD_RE = re.compile(
    r'(?P<indent>[ \t]+)<li class="nav__item"><a class="nav__link" href="/intelligence/">Intelligence</a></li>\n'
    r'[ \t]+<li class="nav__item"><a class="nav__link" href="/insights/">Insights</a></li>'
)

DESKTOP_NEW_TEMPLATE = """{indent}<li class="nav__item">
{indent}  <a class="nav__link" href="/intelligence/" data-active-paths="/intelligence/,/insights/" aria-haspopup="true" aria-expanded="false">Intelligence
{indent}    <svg class="nav__caret" viewBox="0 0 12 8" aria-hidden="true"><path d="M6 8 0 0h12z" fill="currentColor"/></svg>
{indent}  </a>
{indent}  <div class="dropdown dropdown--two-col" role="menu">
{indent}    <div class="dropdown__col">
{indent}      <h4>Intelligence Advisory</h4>
{indent}      <ul class="dropdown__list">
{indent}        <li><a class="dropdown__link" href="/intelligence/#reports"><strong>Customized Intelligence Reports</strong><small>Tailored analytical products</small></a></li>
{indent}        <li><a class="dropdown__link" href="/intelligence/#political"><strong>Political &amp; Country Risk Analysis</strong><small>Geopolitical and regulatory</small></a></li>
{indent}        <li><a class="dropdown__link" href="/intelligence/#monitoring"><strong>Daily Monitoring Briefs</strong><small>Verified-source updates</small></a></li>
{indent}        <li><a class="dropdown__link" href="/intelligence/#situational"><strong>Situational Risk Analysis</strong><small>Real-time, incident-driven</small></a></li>
{indent}        <li><a class="dropdown__link" href="/intelligence/heat-map/"><strong>Risk Heat Map</strong><small>Africa-wide visual prioritisation</small></a></li>
{indent}      </ul>
{indent}      <a href="/intelligence/" class="dropdown__view-all">View all intelligence services →</a>
{indent}    </div>
{indent}    <div class="dropdown__col">
{indent}      <h4>Insights &amp; Briefings</h4>
{indent}      <div class="dropdown__posts" id="intel-dropdown-posts" data-skeleton="3">
{indent}        <span class="dropdown__post is-skeleton" aria-hidden="true"><span class="skeleton-line skeleton-line--meta"></span><span class="skeleton-line skeleton-line--title"></span></span>
{indent}        <span class="dropdown__post is-skeleton" aria-hidden="true"><span class="skeleton-line skeleton-line--meta"></span><span class="skeleton-line skeleton-line--title"></span></span>
{indent}        <span class="dropdown__post is-skeleton" aria-hidden="true"><span class="skeleton-line skeleton-line--meta"></span><span class="skeleton-line skeleton-line--title"></span></span>
{indent}      </div>
{indent}      <a href="/insights/" class="dropdown__view-all">All insights →</a>
{indent}    </div>
{indent}  </div>
{indent}</li>"""


# --- Mobile: replace the two standalone <a>s with a <details> accordion ---
MOBILE_OLD_RE = re.compile(
    r'(?P<indent>[ \t]+)<a class="mobile-nav__link" href="/intelligence/">Intelligence</a>\n'
    r'[ \t]+<a class="mobile-nav__link" href="/insights/">Insights</a>'
)

MOBILE_NEW_TEMPLATE = """{indent}<details class="mobile-nav__group">
{indent}  <summary>Intelligence</summary>
{indent}  <div class="mobile-nav__sublist" role="region" aria-label="Intelligence menu">
{indent}    <a href="/intelligence/">Intelligence Advisory</a>
{indent}    <a href="/intelligence/#reports">Customized Intelligence Reports</a>
{indent}    <a href="/intelligence/#political">Political &amp; Country Risk Analysis</a>
{indent}    <a href="/intelligence/#monitoring">Daily Monitoring Briefs</a>
{indent}    <a href="/intelligence/#situational">Situational Risk Analysis</a>
{indent}    <a href="/intelligence/heat-map/">Risk Heat Map</a>
{indent}    <div class="mobile-nav__sep" aria-hidden="true"></div>
{indent}    <a href="/insights/">Latest Insights</a>
{indent}    <div class="mobile-nav__posts" id="mobile-intel-posts"></div>
{indent}  </div>
{indent}</details>"""


def swap_file(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    original = text

    def desktop_sub(m: re.Match) -> str:
        return DESKTOP_NEW_TEMPLATE.format(indent=m.group("indent"))

    def mobile_sub(m: re.Match) -> str:
        return MOBILE_NEW_TEMPLATE.format(indent=m.group("indent"))

    text, n_desktop = DESKTOP_OLD_RE.subn(desktop_sub, text)
    text, n_mobile = MOBILE_OLD_RE.subn(mobile_sub, text)

    if text != original:
        path.write_text(text, encoding="utf-8")
    return (n_desktop, n_mobile)


def main() -> int:
    targets = sorted(ROOT.rglob("*.html"))
    # Skip the local logo-preview helper and admin templates (those don't ship).
    skip = ("_assemble/logo-preview.html",)
    targets = [p for p in targets if not any(s in p.as_posix() for s in skip)]

    total_desktop = 0
    total_mobile = 0
    rows = []
    for p in targets:
        rel = p.relative_to(ROOT).as_posix()
        n_d, n_m = swap_file(p)
        total_desktop += n_d
        total_mobile += n_m
        if n_d or n_m:
            rows.append((rel, n_d, n_m))

    for rel, n_d, n_m in rows:
        print(f"  {rel}  desktop×{n_d} mobile×{n_m}")
    print(f"\nTotals — desktop:{total_desktop}  mobile:{total_mobile}  (files: {len(rows)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
