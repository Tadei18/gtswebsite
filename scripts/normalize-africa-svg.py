#!/usr/bin/env python3
"""
One-shot normalizer for assets/img/maps/africa.svg.

- Strips per-path inline style attributes (so CSS controls styling).
- Adds class="country" to every <path>.
- Adds data-iso="<ISO-3>" to every <path>, mapped from the SVG's ISO-2 id.

Idempotent: re-running on a normalized file is a no-op.
"""

import re
import sys
from pathlib import Path

# ISO-2 (SimpleMaps africa.svg) -> ISO-3 (matches /data/heat-map.json).
ISO2_TO_ISO3 = {
    "AO": "AGO", "BF": "BFA", "BI": "BDI", "BJ": "BEN", "BW": "BWA",
    "CD": "COD", "CF": "CAF", "CG": "COG", "CI": "CIV", "CM": "CMR",
    "DJ": "DJI", "DZ": "DZA", "EG": "EGY", "EH": "ESH", "ER": "ERI",
    "ET": "ETH", "GA": "GAB", "GH": "GHA", "GM": "GMB", "GN": "GIN",
    "GQ": "GNQ", "GW": "GNB", "KE": "KEN", "LR": "LBR", "LS": "LSO",
    "LY": "LBY", "MA": "MAR", "MG": "MDG", "ML": "MLI", "MR": "MRT",
    "MW": "MWI", "MZ": "MOZ", "NA": "NAM", "NE": "NER", "NG": "NGA",
    "RW": "RWA", "SD": "SDN", "SL": "SLE", "SN": "SEN", "SO": "SOM",
    "SS": "SSD", "SZ": "SWZ", "TD": "TCD", "TG": "TGO", "TN": "TUN",
    "TZ": "TZA", "UG": "UGA", "ZA": "ZAF", "ZM": "ZMB", "ZW": "ZWE",
}

PATH_RE = re.compile(r"<path\b([^>]*?)/>", re.DOTALL)
ID_RE = re.compile(r'\bid="([A-Z]{2,3})"')
STYLE_RE = re.compile(r'\s*style="[^"]*"')
CLASS_RE = re.compile(r'\bclass="[^"]*"')
DATA_ISO_RE = re.compile(r'\bdata-iso="[^"]*"')


def normalize_path(match: re.Match) -> str:
    attrs = match.group(1)
    id_match = ID_RE.search(attrs)
    if not id_match:
        return match.group(0)
    code = id_match.group(1)
    iso3 = ISO2_TO_ISO3.get(code) if len(code) == 2 else code

    # Strip inline style.
    attrs = STYLE_RE.sub("", attrs)
    # Replace or add class.
    if CLASS_RE.search(attrs):
        attrs = CLASS_RE.sub('class="country"', attrs)
    else:
        attrs = attrs.rstrip() + '\n     class="country"'
    # Replace or add data-iso.
    if iso3:
        if DATA_ISO_RE.search(attrs):
            attrs = DATA_ISO_RE.sub(f'data-iso="{iso3}"', attrs)
        else:
            attrs = attrs.rstrip() + f'\n     data-iso="{iso3}"'

    return f"<path{attrs}/>"


def main() -> int:
    svg_path = Path(__file__).resolve().parent.parent / "assets" / "img" / "maps" / "africa.svg"
    src = svg_path.read_text(encoding="utf-8")
    out = PATH_RE.sub(normalize_path, src)
    svg_path.write_text(out, encoding="utf-8")

    # Coverage report.
    iso3_codes = {ISO2_TO_ISO3[c] for c in ISO2_TO_ISO3 if c in re.findall(r'id="([A-Z]{2,3})"', src)}
    print(f"Normalized {svg_path}")
    print(f"Paths with data-iso: {len(iso3_codes)}")
    missing_map = sorted(c for c in re.findall(r'id="([A-Z]{2,3})"', src) if len(c) == 2 and c not in ISO2_TO_ISO3)
    if missing_map:
        print(f"WARNING: SVG ISO-2 codes not in mapping table: {missing_map}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
