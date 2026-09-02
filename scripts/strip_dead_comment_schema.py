#!/usr/bin/env python3
"""One-off: remove dead WordPress-comment-system artifacts baked into the
Yoast JSON-LD schema graph on legacy posts -- the static site has no
comment form (#respond) or comment functionality at all, so these fields
are disconnected from what the page actually offers a visitor.

Removes, from the Article node in each file's schema:
  - "commentCount":<N>,          (some values are clearly stale WP spam,
                                   e.g. one post shows 17,814)
  - ,"potentialAction":[{"@type":"CommentAction",...}]
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

COMMENT_COUNT_RE = re.compile(r'"commentCount":\d+,')
COMMENT_ACTION_RE = re.compile(r',"potentialAction":\[\{"@type":"CommentAction".*?\}\]')


def main() -> None:
    touched = 0
    total = 0
    for path in sorted(ROOT.rglob("index.html")):
        if "wp-content" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n1 = COMMENT_COUNT_RE.subn("", text)
        new_text, n2 = COMMENT_ACTION_RE.subn("", new_text)
        if n1 or n2:
            path.write_text(new_text, encoding="utf-8")
            touched += 1
            total += n1 + n2
    print(f"Files touched: {touched}")
    print(f"Total fields removed: {total}")


if __name__ == "__main__":
    main()
