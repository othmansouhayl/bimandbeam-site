#!/usr/bin/env python3
"""One-off: normalize the lowercase 'souhaylothman' identity string to
'Souhayl Othman' wherever it's used as DISPLAY text (schema name/caption
fields, visible bylines, meta tags, link titles) -- while leaving every
URL path (/author/souhaylothman/, escaped \\/author\\/souhaylothman\\/),
the author-souhaylothman CSS class, and the arch_author tracking value
untouched, since those are identifiers, not display text.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Negative lookbehind covers: URL path prefix (plain or JSON-escaped),
# CSS class token, and the Jetpack-stats tracking field.
# Negative lookahead covers: URL path suffix (plain or JSON-escaped).
PATTERN = re.compile(
    r'(?<!/author/)(?<!\\/author\\/)(?<!author-)(?<!arch_author":")souhaylothman(?!/)(?!\\/)'
)


def main() -> None:
    touched = 0
    total = 0
    for path in sorted(ROOT.rglob("index.html")):
        if "wp-content" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = PATTERN.subn("Souhayl Othman", text)
        if n:
            path.write_text(new_text, encoding="utf-8")
            touched += 1
            total += n
    print(f"Files touched: {touched}")
    print(f"Total replacements: {total}")


if __name__ == "__main__":
    main()
