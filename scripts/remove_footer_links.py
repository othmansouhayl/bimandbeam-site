#!/usr/bin/env python3
"""One-off: remove the 'Revit Sync Analyzer', 'Free IDS Editor', and
'Sponsor' footer links site-wide, ahead of deleting the revit-sync/ and
sponsor-us/ pages entirely."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PATTERNS = [
    re.compile(r'\s*<li><a href="[^"]*revit-sync/index\.html"[^>]*>Revit Sync Analyzer</a></li>'),
    re.compile(r'\s*<li><a href="https://ids-editor-pro--othmansouhayl\.replit\.app/"[^>]*>Free IDS Editor</a></li>'),
    re.compile(r'\s*<li><a href="[^"]*sponsor-us/index\.html"[^>]*>Sponsor</a></li>'),
]


def main() -> None:
    touched = 0
    total_removed = 0
    for path in sorted(ROOT.rglob("index.html")):
        if "wp-content" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        new_text = text
        removed_here = 0
        for pattern in PATTERNS:
            new_text, n = pattern.subn("", new_text)
            removed_here += n
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            touched += 1
            total_removed += removed_here
    print(f"Files touched: {touched}")
    print(f"Total <li> entries removed: {total_removed}")


if __name__ == "__main__":
    main()
