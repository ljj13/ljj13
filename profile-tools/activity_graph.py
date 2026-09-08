#!/usr/bin/env python3
import argparse
import json
import os
import urllib.error
import urllib.request
from html import escape

GRAPHQL_URL = "https://api.github.com/graphql"


def fetch_contributions(username: str, token: str):
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    payload = json.dumps({"query": query, "variables": {"login": username}}).encode()
    request = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "FogPurification-profile-action",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub GraphQL request failed: HTTP {exc.code}: {body}") from exc

    if result.get("errors"):
        raise RuntimeError(f"GitHub GraphQL errors: {result['errors']}")

    user = result.get("data", {}).get("user")
    if not user:
        raise RuntimeError(f"GitHub user {username!r} was not found")

    weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [day for week in weeks for day in week["contributionDays"]]
    days.sort(key=lambda item: item["date"])
    return days[-31:]


def render_svg(display_name: str, days):
    width, height = 900, 260
    left, right, top, bottom = 58, 28, 72, 52
    plot_width = width - left - right
    plot_height = height - top - bottom
    counts = [int(day["contributionCount"]) for day in days]
    total = sum(counts)
    maximum = max(counts, default=0)
    y_max = max(1, maximum)

    if len(days) <= 1:
        xs = [left] * len(days)
    else:
        xs = [left + i * plot_width / (len(days) - 1) for i in range(len(days))]
    ys = [top + plot_height - (count / y_max) * plot_height for count in counts]

    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    area_points = " ".join(
        [f"{left:.1f},{top + plot_height:.1f}", points, f"{left + plot_width:.1f},{top + plot_height:.1f}"]
    )

    grid = []
    for i in range(5):
        y = top + i * plot_height / 4
        value = round(y_max * (1 - i / 4))
        grid.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" class="grid" />'
            f'<text x="{left - 12}" y="{y + 4:.1f}" text-anchor="end" class="axis">{value}</text>'
        )

    labels = []
    if days:
        candidate_indexes = sorted(set([0, len(days) // 4, len(days) // 2, (3 * len(days)) // 4, len(days) - 1]))
        for index in candidate_indexes:
            x = xs[index]
            date = escape(days[index]["date"][5:])
            labels.append(f'<text x="{x:.1f}" y="{height - 20}" text-anchor="middle" class="axis">{date}</text>')

    circles = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" class="dot"><title>{escape(day["date"])}: {count}</title></circle>'
        for x, y, day, count in zip(xs, ys, days, counts)
    )

    safe_name = escape(display_name)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" data-point-count="{len(days)}">
<style>
  :root {{ --bg:#ffffff; --fg:#1f2328; --muted:#656d76; --grid:#d0d7de; --line:#0969da; --area:#54aeff; --dot:#0969da; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg:#0d1117; --fg:#e6edf3; --muted:#8b949e; --grid:#30363d; --line:#58a6ff; --area:#1f6feb; --dot:#58a6ff; }} }}
  text {{ font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; }}
  .title {{ fill:var(--fg); font-size:20px; font-weight:600; }}
  .subtitle {{ fill:var(--muted); font-size:13px; }}
  .axis {{ fill:var(--muted); font-size:11px; }}
  .grid {{ stroke:var(--grid); stroke-width:1; opacity:.65; }}
  .area {{ fill:var(--area); opacity:.16; }}
  .line {{ fill:none; stroke:var(--line); stroke-width:2.5; stroke-linecap:round; stroke-linejoin:round; }}
  .dot {{ fill:var(--dot); }}
</style>
<rect width="100%" height="100%" rx="8" fill="transparent" />
<text x="{left}" y="30" class="title">Contribution Activity · {safe_name}</text>
<text x="{left}" y="52" class="subtitle">Last {len(days)} days · Total {total} contributions · Peak {maximum} per day</text>
{''.join(grid)}
<polygon points="{area_points}" class="area" />
<polyline points="{points}" class="line" />
{circles}
{''.join(labels)}
<text x="{width - right}" y="30" text-anchor="end" class="subtitle">Total {total} contributions</text>
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

    days = fetch_contributions(args.username, token)
    svg = render_svg(args.display_name or args.username, days)
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(svg)


if __name__ == "__main__":
    main()
