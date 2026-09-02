#!/usr/bin/env python3
"""One-off: remove the empty <aside class="primary-sidebar"> from all 78
legacy posts and drop the `has-sidebar` body class that reserves a ~400px
grid column for it (Kadence's own CSS in
wp-content/themes/kadence/assets/css/global.min.css scopes the two-column
grid to `.has-sidebar .content-container` -- removing the class alone is
enough to fall back to Kadence's default single-column, no-sidebar layout;
no CSS file needs editing). Verified via headless-browser render before
this rollout: main content width goes from 845px to 1242px on desktop,
with 0px mobile overflow.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ASIDE_RE = re.compile(
    r'<aside class="primary-sidebar widget-area sidebar-slug-sidebar-secondary sidebar-link-style-normal" id="secondary" role="complementary">\n'
    r'<div class="sidebar-inner-wrap">\n'
    r'</div>\n'
    r'</aside><!-- #secondary -->\n?'
)


def main() -> None:
    touched = 0
    problems = []
    for path in sorted(ROOT.rglob("index.html")):
        if "wp-content" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if "has-sidebar" not in text:
            continue

        new_text, n1 = re.subn(r"has-sidebar ", "", text, count=1)
        new_text, n2 = ASIDE_RE.subn("", new_text)

        if n1 != 1 or n2 != 1:
            problems.append((path.relative_to(ROOT), n1, n2))
            continue

        path.write_text(new_text, encoding="utf-8")
        touched += 1

    print(f"Files fixed: {touched}")
    if problems:
        print(f"Skipped (unexpected pattern, needs manual check): {len(problems)}")
        for p, n1, n2 in problems:
            print(f"  {p}: has-sidebar removed={n1}, aside removed={n2}")


if __name__ == "__main__":
    main()
