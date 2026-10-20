#!/usr/bin/env python3
"""Retire every Gumroad (gum.co) CTA: book buttons now point to the /book/ landing page,
the free preview wording is replaced, and the free-checklist promos are removed."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CTA_RE = re.compile(r'<a( class="[^"]*")? href="https://gum\.co/u/h0eoqfrh" rel="noopener" target="_blank">Get the free preview</a>')
PREVIEW_SENTENCE = "Free 9-page preview, no strings attached."
NEW_SENTENCE = "Now available on Amazon Kindle, in English and French."

HOME_BUTTONS_RE = re.compile(
    r'<a class="bb-btn bb-btn-fill" href="https://gum\.co/u/h0eoqfrh"[^>]*>Get free preview</a>\s*'
    r'<a class="bb-btn bb-btn-outline" href="https://gum\.co/u/t6dmjbeu"[^>]*>Buy the full book</a>')
HOME_COPY = "Get a free 9-page preview, no strings attached, or grab the full book."
HOME_COPY_NEW = "Now available on Amazon Kindle, in English and French."
HOME_CHECKLIST_RE = re.compile(r'<section class="bb-book" style="background:#0a0a0a;.*?</section>\s*', re.S)
POST_CHECKLIST_RE = re.compile(r'<div style="background:#0a0a0a;border:1px solid #22C55E;.*?Get the checklist</a>\s*</div>\s*', re.S)


def main():
    changed = 0
    for f in sorted(ROOT.rglob("index.html")):
        text = f.read_text(encoding="utf-8")
        if "gum.co" not in text and PREVIEW_SENTENCE not in text:
            continue
        rel = f.relative_to(ROOT)
        depth = len(rel.parts) - 1
        book = "./" + "../" * depth + "book/index.html"
        new = text
        if rel == Path("index.html"):
            new = HOME_BUTTONS_RE.sub(f'<a class="bb-btn bb-btn-fill" href="{book}">Get the book</a>', new)
            new = new.replace(HOME_COPY, HOME_COPY_NEW)
            new = HOME_CHECKLIST_RE.sub("", new)
        new = POST_CHECKLIST_RE.sub("", new)
        new = CTA_RE.sub(lambda m: f'<a{m.group(1) or ""} href="{book}">Get the book</a>', new)
        new = new.replace(PREVIEW_SENTENCE, NEW_SENTENCE)
        if new != text:
            f.write_text(new, encoding="utf-8")
            changed += 1
    left = [str(p) for p in ROOT.rglob("*.html") if "gum.co" in p.read_text(encoding="utf-8")]
    print(f"changed: {changed}, files still containing gum.co: {left}")


if __name__ == "__main__":
    main()
