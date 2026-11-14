"""Refresh public GitHub stats using only Python's standard library."""

import json
import os
from collections import Counter
from datetime import datetime, timezone
from urllib.request import Request, urlopen

from build_assets import PALETTES, svg, text

OWNER = "DivyanathaDantu"


def api(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "divy-profile-readme"}
    if token := os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(f"https://api.github.com/{path}", headers=headers), timeout=30) as response:
        return json.load(response)


def main():
    repos = []
    page = 1
    while True:
        batch = api(f"users/{OWNER}/repos?per_page=100&type=owner&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    original = [repo for repo in repos if not repo["fork"]]
    languages = Counter(repo["language"] for repo in original if repo["language"])
    top = languages.most_common(1)[0][0] if languages else "—"
    stats = [(str(len(repos)), "Public repos"), (str(sum(repo["stargazers_count"] for repo in original)), "Stars on my repos"), (top, "Top language by repo count")]
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for theme, p in PALETTES.items():
        for mobile in (False, True):
            w, h = (440, 282) if mobile else (960, 150)
            body = f'<rect width="{w}" height="{h}" rx="16" fill="{p["bg"]}"/>'
            for i, (value, label) in enumerate(stats):
                x, y = (24, 45+i*76) if mobile else (32+i*310, 55)
                body += text(x,y,value,30,p["fg"],'font-weight="650"')
                body += text(x,y+25,label,13,p["muted"])
            body += text(24 if mobile else 32,h-18,f"PUBLIC GITHUB SNAPSHOT · {date}",10,p["muted"],'class="mono"')
            svg(f'stats-{theme}{"-mobile" if mobile else ""}.svg',w,h,"Public GitHub activity",f"{len(repos)} public repositories. {stats[1][0]} stars on original repositories. Most common language by original repo count: {top}. Updated {date}.",body)


if __name__ == "__main__":
    main()
