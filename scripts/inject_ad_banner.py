#!/usr/bin/env python3
"""Injects the sitewide bimaturity.app ad banner into the content flow of every page
(below the hero on the homepage, right after the nav elsewhere — never pinned above
the header/nav where it clashes with the browser chrome). Idempotent: strips any
previously injected banner before re-inserting, so it's safe to re-run after edits."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "bbAdBanner"
IMG_REL = "wp-content/uploads/2026/09/bimaturity-banner-ad.webp"

OLD_BANNER_RE = re.compile(
    r'<div class="bb-ad-banner-wrap" id="bbAdBanner">.*?</script>'
)
BB_NAV_OPEN_RE = re.compile(r'<nav class="bb-nav">')
NAV_CLOSE_RE = re.compile(r'</nav>')
HEADER_CLOSE_RE = re.compile(r'(</header>)')
BOOK_SECTION_RE = re.compile(r'(<section class="bb-book")')


def banner_html(prefix: str) -> str:
    img_src = f"{prefix}{IMG_REL}"
    return (
        f'<div class="bb-ad-banner-wrap" id="{MARKER}">'
        f'<a class="bb-ad-banner" href="https://bimaturity.app/en" target="_blank" rel="noopener sponsored" '
        f'aria-label="BIM Maturity — Advertisement, opens in new tab">'
        f'<span class="bb-ad-tag">Ad</span>'
        f'<img src="{img_src}" alt="BIM Maturity — assess and improve your organization’s BIM maturity" '
        f'width="560" height="228" loading="lazy"/>'
        f'</a>'
        f'<button class="bb-ad-close" id="bbAdClose" aria-label="Close advertisement">&times;</button>'
        f'</div>'
        f'<script>(function(){{try{{'
        f"if(localStorage.getItem('bbAdDismissed')==='1'){{var b=document.getElementById('{MARKER}');if(b)b.style.display='none';}}"
        f"var c=document.getElementById('bbAdClose');if(c)c.addEventListener('click',function(){{"
        f"var b=document.getElementById('{MARKER}');if(b)b.style.display='none';"
        f"try{{localStorage.setItem('bbAdDismissed','1');}}catch(e){{}}"
        f"}});"
        f'}}catch(e){{}}}})();</script>'
    )


def main():
    files = sorted(ROOT.rglob("index.html"))
    placed_hero, placed_nav, placed_header, removed_old, missed = 0, 0, 0, 0, 0

    for f in files:
        text = f.read_text(encoding="utf-8")

        if OLD_BANNER_RE.search(text):
            text = OLD_BANNER_RE.sub("", text, count=1)
            removed_old += 1

        depth = len(f.relative_to(ROOT).parts) - 1
        prefix = "../" * depth if depth > 0 else "./"
        snippet = banner_html(prefix)

        rel = f.relative_to(ROOT)
        bb_nav_match = BB_NAV_OPEN_RE.search(text)

        if rel == Path("index.html") and BOOK_SECTION_RE.search(text):
            new_text = BOOK_SECTION_RE.sub(snippet + r"\1", text, count=1)
            placed_hero += 1
        elif bb_nav_match:
            nav_close = NAV_CLOSE_RE.search(text, bb_nav_match.end())
            if not nav_close:
                print(f"MISS (bb-nav open but no matching close): {f}")
                missed += 1
                continue
            insert_at = nav_close.end()
            new_text = text[:insert_at] + snippet + text[insert_at:]
            placed_nav += 1
        elif HEADER_CLOSE_RE.search(text):
            new_text = HEADER_CLOSE_RE.sub(r"\1" + snippet, text, count=1)
            placed_header += 1
        else:
            print(f"MISS (no insertion point found): {f}")
            missed += 1
            continue

        f.write_text(new_text, encoding="utf-8")

    print(
        f"After hero (homepage): {placed_hero}, after </nav>: {placed_nav}, "
        f"after </header> fallback: {placed_header}, old banners removed first: {removed_old}, "
        f"missed: {missed}, total files: {len(files)}"
    )


if __name__ == "__main__":
    main()
