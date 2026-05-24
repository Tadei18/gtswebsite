#!/usr/bin/env python3
"""
One-shot scrub of the Media / Gallery section from the GTS site.

Idempotent: re-running on a cleaned tree is a no-op.

Operates on plain string removal because every reference uses one of three
exact, repo-wide-identical markup patterns (verified via grep before this
script was written).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Three nav/footer patterns — identical wherever they appear in the inlined
# chrome across every HTML page. Each pattern is removed including its
# trailing newline.
HTML_REMOVALS = [
    '            <li class="nav__item"><a class="nav__link" href="/media/">Media</a></li>\n',
    '      <a class="mobile-nav__link" href="/media/">Media</a>\n',
    '            <li><a href="/media/">Media</a></li>\n',
]

# Files containing the chrome — these get the 3-line scrub.
HTML_FILES = [
    "404.html",
    "about/index.html",
    "careers/index.html",
    "contact/index.html",
    "contact/thank-you.html",
    "index.html",
    "industries/index.html",
    "insights/index.html",
    "insights/posts/behavioural-security-awareness.html",
    "insights/posts/east-africa-elections-outlook-2026.html",
    "insights/posts/supply-chain-security-2026.html",
    "intelligence/index.html",
    "intelligence/heat-map/index.html",
    "consulting/index.html",
    "consulting/business-process-audits/index.html",
    "consulting/capacity-building/index.html",
    "consulting/embedded-consultancy/index.html",
    "consulting/market-entry/index.html",
    "consulting/mergers-acquisitions/index.html",
    "consulting/policy-sops/index.html",
    "consulting/safety-evacuation/index.html",
    "consulting/security-risk-assessments/index.html",
    "consulting/tailored-investigations/index.html",
    "consulting/travel-security/index.html",
    "consulting/vetting-due-diligence/index.html",
    "services/index.html",
    "services/command-centre/index.html",
    "services/corporate-security/index.html",
    "services/events-security/index.html",
    "services/executive-protection/index.html",
    "services/forensic-investigations/index.html",
    "services/fraud-security-training/index.html",
    "services/manned-guarding/index.html",
    "services/reception-security/index.html",
    "services/residential-security/index.html",
    "services/risk-management/index.html",
    "services/security-systems/index.html",
    "services/supply-chain-security/index.html",
]

# Partials + chrome build inputs — same patterns but smaller subsets per file
# (some files only have header items, others only footer).
PARTIAL_FILES = [
    "partials/header.html",
    "partials/footer.html",
    "_assemble/chrome-top.html",
    "_assemble/chrome-bottom.html",
]


def scrub_html_file(path: Path) -> int:
    """Remove the three Media nav/footer lines from one file. Returns line count removed."""
    text = path.read_text(encoding="utf-8")
    original = text
    for needle in HTML_REMOVALS:
        text = text.replace(needle, "")
    if text != original:
        path.write_text(text, encoding="utf-8")
        return original.count("\n") - text.count("\n")
    return 0


def scrub_pages_css(path: Path) -> bool:
    """Excise the MEDIA / GALLERY + Lightbox block (header comment through last lightbox rule)."""
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"/\* -+\n\s*MEDIA / GALLERY\n\s*-+ \*/\n.*?(?=\n/\* -+\n   CONTACT\n)",
        re.DOTALL,
    )
    new = pattern.sub("", text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def scrub_build_py(path: Path) -> bool:
    """Remove the four media-specific blocks from the build script."""
    text = path.read_text(encoding="utf-8")
    original = text

    # Block A: GALLERY_ITEMS + header comment "# MEDIA / GALLERY".
    text = re.sub(
        r"# MEDIA / GALLERY\n# -+\nGALLERY_ITEMS = \[[^\]]*?\]\n+",
        "",
        text,
        count=1,
    )

    # Block B: _media_body() function definition through its closing return.
    text = re.sub(
        r"def _media_body\(\):.*?(?=\n\n\ndef |\nclass |\nif __name__)",
        "",
        text,
        count=1,
        flags=re.DOTALL,
    )

    # Block C: the render() call for media/.
    text = re.sub(
        r"    # ---- Media\n    render\([^)]*?\)\n+",
        "",
        text,
        count=1,
        flags=re.DOTALL,
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def scrub_sitemap(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"  <url>\n"
        r"    <loc>https://gtsriskadvisory\.com/media/</loc>\n"
        r"    <lastmod>[^<]*</lastmod>\n"
        r"    <priority>[^<]*</priority>\n"
        r"  </url>\n"
    )
    new = pattern.sub("", text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def write_redirects(path: Path) -> None:
    path.write_text(
        "# Media / Gallery section was removed; preserve link equity from old\n"
        "# bookmarks, search-engine caches, and any stray inbound references.\n"
        "/media     /  301\n"
        "/media/*   /  301\n",
        encoding="utf-8",
    )


def main() -> int:
    print("Scrubbing inlined chrome from page HTML…")
    touched_html = 0
    for rel in HTML_FILES + PARTIAL_FILES:
        p = ROOT / rel
        if not p.exists():
            print(f"  skip (missing): {rel}")
            continue
        removed = scrub_html_file(p)
        if removed:
            touched_html += 1
            print(f"  {rel}  (-{removed} lines)")

    print(f"\nHTML files scrubbed: {touched_html}")

    print("\nScrubbing pages.css gallery block…")
    if scrub_pages_css(ROOT / "assets/css/pages.css"):
        print("  pages.css updated")
    else:
        print("  pages.css unchanged (already clean?)")

    print("\nScrubbing build.py media generator…")
    if scrub_build_py(ROOT / "_assemble/build.py"):
        print("  build.py updated")
    else:
        print("  build.py unchanged (already clean?)")

    print("\nScrubbing sitemap.xml…")
    if scrub_sitemap(ROOT / "sitemap.xml"):
        print("  sitemap.xml updated")
    else:
        print("  sitemap.xml unchanged (already clean?)")

    print("\nWriting _redirects…")
    write_redirects(ROOT / "_redirects")
    print("  _redirects written")

    return 0


if __name__ == "__main__":
    sys.exit(main())
