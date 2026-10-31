#!/usr/bin/env python3
"""
Cache-bust the CSS and JS the HTML pages load.

    python3 tools/stamp_assets.py

Rewrites every local <script src="js/x.js"> and <link href="css/x.css"> in the
*.html files to carry a ?v=<hash of that file's contents>. When a file changes
its URL changes, so a browser or CDN can never serve a stale copy alongside
fresh HTML. When nothing changes, the URLs stay identical and stay cached.

build_people.py calls this automatically, so you normally never run it by hand.

Why this exists: js/people-data.json is fetched with cache:'no-cache' and is
always current, but the *renderer* that reads it is a plain <script> and was
being cached. A mismatch between new data and an old renderer silently blanked
fields on the page.
"""

import hashlib
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Local assets only — never touch a CDN or Google Fonts URL.
PATTERN = re.compile(
    r'(?P<attr>src|href)="(?P<path>(?:js|css)/[A-Za-z0-9._-]+\.(?:js|css))'
    r'(?:\?v=[0-9a-f]+)?"'
)


def short_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:8]


def main():
    hashes, changed = {}, []

    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(ROOT, name)
        src = io.open(path, encoding="utf-8").read()

        def sub(m):
            rel = m.group("path")
            full = os.path.join(ROOT, *rel.split("/"))
            if not os.path.exists(full):
                return m.group(0)
            if rel not in hashes:
                hashes[rel] = short_hash(full)
            return f'{m.group("attr")}="{rel}?v={hashes[rel]}"'

        out = PATTERN.sub(sub, src)
        if out != src:
            io.open(path, "w", encoding="utf-8").write(out)
            changed.append(name)

    if changed:
        print("  stamped assets in: " + ", ".join(changed))
    for rel, h in sorted(hashes.items()):
        print(f"    {rel}?v={h}")


if __name__ == "__main__":
    main()
