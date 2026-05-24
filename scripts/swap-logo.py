#!/usr/bin/env python3
"""
One-shot logo swap.

The supplied 'horizontal' SVG is actually a shield-only export on a square
canvas, so we use the FULL logo (shield + GTS + tagline stacked) everywhere
and rely on CSS sizing — the documented fallback in the brief.

Per-region replacement strategy:
  - Header link wrapper (has aria-label): rewritten to <a class="brand"> with
    an <img class="brand__logo">.
  - Mobile-nav link wrapper (inside .mobile-nav__head): same <a class="brand">
    + <img>, but the smaller height kicks in via .mobile-nav__head .brand__logo.
  - Footer (inside .footer__col): bare <img class="footer__logo"> with no
    anchor wrap, per spec.

Also rewrites the favicon link in <head> and the JSON-LD "logo" field.
Idempotent.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LOGO_SRC = "/assets/img/brand/gts-logo-full.svg"

HEADER_LOGO_RE = re.compile(
    r'<a href="/" class="logo" aria-label="GTS Risk Advisory — Home">\s*'
    r'<span class="logo__mark">GTS</span>\s*'
    r'<span class="logo__rule" aria-hidden="true"></span>\s*'
    r'<span class="logo__name">Risk Advisory</span>\s*'
    r'</a>'
)

PLAIN_LOGO_RE = re.compile(
    r'<a href="/" class="logo">\s*'
    r'<span class="logo__mark">GTS</span>\s*'
    r'<span class="logo__rule" aria-hidden="true"></span>\s*'
    r'<span class="logo__name">Risk Advisory</span>\s*'
    r'</a>'
)

HEADER_REPLACEMENT = (
    f'<a href="/" class="brand" aria-label="GTS Risk Advisory — home">'
    f'<img src="{LOGO_SRC}" alt="GTS Risk Advisory" class="brand__logo" width="64" height="64"></a>'
)

MOBILE_REPLACEMENT = (
    f'<a href="/" class="brand" aria-label="GTS Risk Advisory — home">'
    f'<img src="{LOGO_SRC}" alt="GTS Risk Advisory" class="brand__logo" width="52" height="52"></a>'
)

FOOTER_REPLACEMENT = (
    f'<img src="{LOGO_SRC}" '
    f'alt="GTS Risk Advisory — Security &amp; Risk Consulting" '
    f'class="footer__logo" width="100" height="100">'
)

# <head> swaps.
OLD_FAVICON_LINK = '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
NEW_FAVICON_LINKS = (
    '<link rel="icon" type="image/png" href="/favicon.png">\n'
    '  <link rel="apple-touch-icon" href="/apple-touch-icon.png">'
)

# JSON-LD logo URL — only on home page.
OLD_JSONLD_LOGO = '"logo": "https://gtsriskadvisory.com/favicon.svg"'
NEW_JSONLD_LOGO = '"logo": "https://gtsriskadvisory.com/assets/img/brand/gts-logo-full.svg"'


def swap_file(path: Path) -> tuple[int, int, int, int, int]:
    """Returns counts: (header, mobile, footer, favicon, jsonld) edits."""
    text = path.read_text(encoding="utf-8")
    original = text

    # Header (always first; aria-label disambiguates it from the plain ones).
    text, n_header = HEADER_LOGO_RE.subn(HEADER_REPLACEMENT, text, count=1)

    # Of the remaining plain wrappers, the first is mobile-nav, the second is footer.
    # Replace them in document order with the appropriate substitution.
    text, n_mobile = PLAIN_LOGO_RE.subn(MOBILE_REPLACEMENT, text, count=1)
    text, n_footer = PLAIN_LOGO_RE.subn(FOOTER_REPLACEMENT, text, count=1)

    # Favicon link.
    n_fav = text.count(OLD_FAVICON_LINK)
    text = text.replace(OLD_FAVICON_LINK, NEW_FAVICON_LINKS)

    # JSON-LD logo (home only).
    n_ld = text.count(OLD_JSONLD_LOGO)
    text = text.replace(OLD_JSONLD_LOGO, NEW_JSONLD_LOGO)

    if text != original:
        path.write_text(text, encoding="utf-8")
    return (n_header, n_mobile, n_footer, n_fav, n_ld)


def main() -> int:
    targets = sorted(ROOT.rglob("*.html"))
    # Skip the local logo-preview helper and any backups.
    targets = [p for p in targets if "_assemble/logo-preview.html" not in p.as_posix()]

    tot = [0, 0, 0, 0, 0]
    rows = []
    for p in targets:
        rel = p.relative_to(ROOT).as_posix()
        counts = swap_file(p)
        for i, c in enumerate(counts):
            tot[i] += c
        if any(counts):
            rows.append((rel, counts))

    for rel, counts in rows:
        h, m, f, fav, ld = counts
        flags = []
        if h: flags.append(f"header×{h}")
        if m: flags.append(f"mobile×{m}")
        if f: flags.append(f"footer×{f}")
        if fav: flags.append(f"favicon×{fav}")
        if ld: flags.append(f"jsonld×{ld}")
        print(f"  {rel}  {' '.join(flags)}")

    print(
        f"\nTotals — header:{tot[0]}  mobile:{tot[1]}  footer:{tot[2]}  "
        f"favicon:{tot[3]}  jsonld:{tot[4]}  (files touched: {len(rows)})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
