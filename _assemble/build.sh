#!/usr/bin/env bash
# Page assembler — combines head + chrome + body + footer into final HTML.
# Usage:
#   ./build.sh OUT_PATH TITLE DESC CANONICAL [EXTRA_HEAD] [EXTRA_SCRIPTS] < BODY_HTML
# Reads body content from stdin.
set -euo pipefail

OUT="$1"
TITLE="$2"
DESC="$3"
CANON="$4"
EXTRA_HEAD="${5:-}"
EXTRA_SCRIPTS="${6:-}"

# Read body content from stdin
BODY=$(cat)

# Escape ampersand and pipe in titles/descs for sed (use python for safety on title/desc replacement)
python3 - "$OUT" "$TITLE" "$DESC" "$CANON" "$EXTRA_HEAD" "$EXTRA_SCRIPTS" "$BODY" <<'PY'
import sys, os
out, title, desc, canon, extra_head, extra_scripts, body = sys.argv[1:8]
top = open('_assemble/chrome-top.html').read()
bot = open('_assemble/chrome-bottom.html').read()
top = top.replace('__CANONICAL_PATH__', canon)
top = top.replace('__OG_TITLE__', title)
top = top.replace('__OG_DESC__', desc)
top = top.replace('__EXTRA_HEAD__', extra_head)
bot = bot.replace('__EXTRA_SCRIPTS__', extra_scripts)
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
{top}
{body}
{bot}'''
os.makedirs(os.path.dirname(out), exist_ok=True) if os.path.dirname(out) else None
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Wrote {out} ({len(html)} bytes)")
PY
