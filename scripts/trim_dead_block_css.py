#!/usr/bin/env python3
"""One-off: strip inline WordPress/Kadence block-editor <style> blocks that
are confirmed dead per post, verified by checking actual class-attribute
usage in each post's own HTML (not just grepping the CSS rule text, which
matches every file regardless of use since the rule definitions are
themselves baked into every page).

NOT touched, on purpose:
  - kadence-global-inline-css: defines --global-paletteN vars that
    brand.css's cascade depends on, plus base h1-h6/container sizing.
    Load-bearing everywhere.
  - wp-block-library-inline-css: mostly LIVE, not dead -- it's what makes
    standard content images responsive (`img[class*=wp-image-]{max-width:
    100%}`), resets figure margins, handles .has-text-align-* (used
    throughout ordinary paragraph content), AND defines .screen-reader-text
    which the site's "Skip to content" link depends on for accessibility.
    Confirmed used broadly; not safe to remove wholesale.
  - wp-img-auto-sizes-contain-inline-css: tiny (135B), not worth the risk.

Removed, per post, only where usage was verified absent:
  - kadence_blocks_palette_css (.has-kb-palette-1-*): 0/78 posts use it --
    removed from all 78.
  - wp-block-button-inline-css and classic-theme-styles-inline-css
    (.wp-block-button__link / .wp-block-file__button): removed only from
    posts that don't contain a `class="wp-block-button` element (64/78).
  - kadence-blocks-global-variables-inline-css (--global-kb-font-size-*):
    removed only from posts with no `kb-`-prefixed class (62/78).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BLOCK_RE = {
    "palette": re.compile(
        r'<style id="kadence_blocks_palette_css">.*?</style>\n?', re.S
    ),
    "classic_theme": re.compile(
        r'<style id="classic-theme-styles-inline-css">.*?</style>\n?', re.S
    ),
    "wp_block_button": re.compile(
        r'<style id="wp-block-button-inline-css">.*?</style>\n?', re.S
    ),
    "kadence_blocks_vars": re.compile(
        r'<style id="kadence-blocks-global-variables-inline-css">.*?</style>\n?',
        re.S,
    ),
}


def main() -> None:
    touched = 0
    saved_bytes = 0
    for path in sorted(ROOT.rglob("index.html")):
        if "wp-content" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if 'id="kadence_blocks_palette_css"' not in text:
            continue  # not a legacy post using this template at all

        orig_len = len(text)
        uses_wp_block_button = 'class="wp-block-button' in text
        uses_kb_class = bool(re.search(r'class="[^"]*\bkb-', text))

        new_text = BLOCK_RE["palette"].sub("", text)
        if not uses_wp_block_button:
            new_text = BLOCK_RE["classic_theme"].sub("", new_text)
            new_text = BLOCK_RE["wp_block_button"].sub("", new_text)
        if not uses_kb_class:
            new_text = BLOCK_RE["kadence_blocks_vars"].sub("", new_text)

        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            touched += 1
            saved_bytes += orig_len - len(new_text)

    print(f"Files touched: {touched}")
    print(f"Bytes saved: {saved_bytes} ({saved_bytes/1024:.1f} KB)")


if __name__ == "__main__":
    main()
