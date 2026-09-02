#!/usr/bin/env python3
"""Fix the site-wide canonical-tag bug found in the SEO audit
(bimandbeam.com-audit/findings/technical.md, Finding 3).

Every legacy page carries:
    <base href="./index.html"/>
    ...
    <link href="./index.html" rel="canonical"/>

Per HTML resolution rules this makes the canonical declare the
".../index.html" URL form rather than the trailing-slash directory form
used everywhere else (sitemap, internal links). GitHub Pages serves both
forms live with identical content and no redirect, so this creates a
duplicate-URL surface across ~97% of the site.

This script, for every index.html under the repo except the homepage and
pages that already have a correct absolute self-referencing canonical
(the 4 newest 2026 posts):
  1. Removes the now-redundant <base href="./index.html"/> tag (verified
     safe to remove -- it resolves to the same directory as the document's
     own URL either way, so no other relative link/resource on the page is
     affected).
  2. Replaces <link href="./index.html" rel="canonical"/> with an absolute,
     trailing-slash self-referencing canonical built from the file's real
     path, e.g.
     <link rel="canonical" href="https://bimandbeam.com/2022/01/slug/"/>
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://bimandbeam.com"

BASE_TAG_RE = re.compile(r'\s*<base href="\./index\.html"/>\s*\n?')
CANONICAL_RE = re.compile(r'<link href="\./index\.html" rel="canonical"/>')
ALREADY_ABSOLUTE_RE = re.compile(r'<link rel="canonical" href="https://bimandbeam\.com/')

SKIP_PATHS = {ROOT / "index.html"}  # homepage already correct, has no base/canonical bug


def url_for(index_path: Path) -> str:
    rel = index_path.relative_to(ROOT).parent.as_posix()
    if rel == ".":
        return f"{BASE_URL}/"
    return f"{BASE_URL}/{rel}/"


def fix_file(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")

    if ALREADY_ABSOLUTE_RE.search(text):
        return None  # already correct (homepage template, 4 newest posts)

    if not CANONICAL_RE.search(text):
        return "no matching canonical tag found -- skipped, needs manual check"

    new_text = BASE_TAG_RE.sub("", text, count=1)
    canonical_url = url_for(path)
    new_text = CANONICAL_RE.sub(
        f'<link rel="canonical" href="{canonical_url}"/>', new_text, count=1
    )

    if new_text == text:
        return None

    path.write_text(new_text, encoding="utf-8")
    return "fixed"


def main() -> None:
    fixed = 0
    skipped_ok = 0
    problems = []

    for index_path in sorted(ROOT.rglob("index.html")):
        if index_path in SKIP_PATHS:
            continue
        # Don't touch anything outside the real static site (e.g. a stray
        # node_modules or similar, if one ever exists).
        if "wp-content" in index_path.parts or ".git" in index_path.parts:
            continue

        result = fix_file(index_path)
        if result == "fixed":
            fixed += 1
        elif result is None:
            skipped_ok += 1
        else:
            problems.append((index_path.relative_to(ROOT), result))

    print(f"Fixed: {fixed}")
    print(f"Already correct / skipped: {skipped_ok}")
    if problems:
        print(f"Needs manual review ({len(problems)}):")
        for path, msg in problems:
            print(f"  {path}: {msg}")


if __name__ == "__main__":
    main()
