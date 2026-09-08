#!/usr/bin/env python3
import argparse
import json
import os
import urllib.request
from datetime import datetime, timezone
from html import escape

from activity_graph import fetch_contributions

API = "https://api.github.com"


def _get_json(url: str):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "FogPurification-profile-action",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_stats(username: str, token: str):
    user = _get_json(f"{API}/users/{username}")
    repos = _get_json(f"{API}/users/{username}/repos?per_page=100&type=owner&sort=updated")
    contributions = fetch_contributions(username, token)

    created = datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
    years = max(0, int((datetime.now(timezone.utc) - created).days / 365.2425))

    return {
        "stars": sum(int(repo.get("stargazers_count", 0)) for repo in repos),
        "repos": int(user.get("public_repos", len(repos))),
        "followers": int(user.get("followers", 0)),
        "forks": sum(int(repo.get("forks_count", 0)) for repo in repos),
        "contributions": sum(int(day["contributionCount"]) for day in contributions),
        "years": years,
    }


def render_trophy_svg(display_name: str, stats):
    items = [
        ("Stars", stats["stars"], "★"),
        ("Repositories", stats["repos"], "R"),
        ("Followers", stats["followers"], "F"),
        ("Forks", stats["forks"], "⑂"),
        ("Contributions", stats["contributions"], "C"),
        ("Years on GitHub", stats["years"], "Y"),
    ]
    width, height = 960, 205
    panel_w, gap, left = 142, 14, 17
    top = 54

    panels = []
    for index, (label, value, icon) in enumerate(items):
        x = left + index * (panel_w + gap)
        panels.append(f'''<g transform="translate({x},{top})">
  <rect width="{panel_w}" height="132" rx="12" class="panel" />
  <circle cx="71" cy="30" r="18" class="medal" />
  <text x="71" y="36" text-anchor="middle" class="icon">{escape(str(icon))}</text>
  <text x="71" y="79" text-anchor="middle" class="value">{escape(str(value))}</text>
  <text x="71" y="108" text-anchor="middle" class="label">{escape(label)}</text>
</g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
  :root {{ --fg:#1f2328; --muted:#656d76; --border:#d0d7de; --panel:#f6f8fa; --accent:#0969da; --medal:#ddf4ff; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --fg:#e6edf3; --muted:#8b949e; --border:#30363d; --panel:#161b22; --accent:#58a6ff; --medal:#0c2d6b; }} }}
  text {{ font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; }}
  .title {{ fill:var(--fg); font-size:20px; font-weight:600; }}
  .panel {{ fill:var(--panel); stroke:var(--border); stroke-width:1; }}
  .medal {{ fill:var(--medal); stroke:var(--accent); stroke-width:1.5; }}
  .icon {{ fill:var(--accent); font-size:16px; font-weight:700; }}
  .value {{ fill:var(--fg); font-size:26px; font-weight:700; }}
  .label {{ fill:var(--muted); font-size:12px; }}
</style>
<text x="17" y="31" class="title">Trophy Board · {escape(display_name)}</text>
{''.join(panels)}
</svg>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--display-name", default=None)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required")

    stats = fetch_stats(args.username, token)
    svg = render_trophy_svg(args.display_name or args.username, stats)
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(svg)


if __name__ == "__main__":
    main()
