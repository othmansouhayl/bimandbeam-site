#!/usr/bin/env python3
"""Injects the sitewide bimaturity.app ad banner into every page's <body>, right before .bb-nav (or right after <body> as a fallback). Idempotent: skips files that already contain the banner marker."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "bbAdBanner"
IMG_REL = "wp-content/uploads/2026/09/bimaturity-banner-ad.webp"

NAV_RE = re.compile(r'(<nav class="bb-nav">)')
BODY_RE = re.compile(r'(<body[^>]*>)')


def banner_html(prefix: str) -> str:
    img_src = f"{prefix}{IMG_REL}"
    return (
        f'<div class="bb-ad-banner-wrap" id="{MARKER}">'
        f'<a class="bb-ad-banner" href="https://bimaturity.app/en" target="_blank" rel="noopener sponsored" '
        f'aria-label="BIM Maturity — Advertisement, opens in new tab">'
        f'<span class="bb-ad-tag">Ad</span>'
        f'<img src="{img_src}" alt="BIM Maturity — assess and improve your organization’s BIM maturity" '
        f'width="560" height="228" loading="eager"/>'
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
    injected, skipped, fallback = 0, 0, 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        if MARKER in text:
            skipped += 1
            continue

        depth = len(f.relative_to(ROOT).parts) - 1
        prefix = "../" * depth if depth > 0 else "./"

        snippet = banner_html(prefix)

        if NAV_RE.search(text):
            new_text = NAV_RE.sub(snippet + r"\1", text, count=1)
            injected += 1
        elif BODY_RE.search(text):
            new_text = BODY_RE.sub(r"\1" + snippet, text, count=1)
            injected += 1
            fallback += 1
        else:
            print(f"SKIP (no body/nav found): {f}")
            continue

        f.write_text(new_text, encoding="utf-8")

    print(f"Injected: {injected} (fallback body-insert: {fallback}), already had banner: {skipped}, total files: {len(files)}")


if __name__ == "__main__":
    main()
