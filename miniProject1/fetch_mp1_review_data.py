"""
Download recent user reviews for MP1 (ChatGPT, Gemini, Claude) from
Google Play and the Apple App Store without API keys.

- Google Play: ``google-play-scraper`` (unofficial Play Store client).
- App Store: Apple's public iTunes RSS JSON feed for customer reviews (``requests``),
  because the ``app-store-scraper`` library often breaks when Apple's HTML/JSON changes.

Writes one UTF-8 CSV you can load in pandas for A5 and MP1.

Recommended: use a virtual environment (macOS/Homebrew Python blocks global pip).

    cd /path/to/hcde530
    python3 -m venv miniProject1/.venv
    source miniProject1/.venv/bin/activate
    python3 -m pip install -r miniProject1/requirements.txt

Run:

    python3 miniProject1/fetch_mp1_review_data.py

That collects up to **500 reviews per AI app per store** (ChatGPT, Gemini, Claude ×
Google Play × App Store), so up to **3,000 rows** when both stores return a full page
set. Apple’s RSS feed stops at **10 pages (~500 reviews)** per app; Google Play uses
pagination until the cap is reached.

Override for testing: ``MP1_REVIEWS_PER_STORE=50 python3 miniProject1/fetch_mp1_review_data.py``

Install pandas in the same venv when you do A5/MP1 analysis (not required for this fetch script).
"""

from __future__ import annotations

import csv
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from google_play_scraper import Sort, reviews as gp_reviews

# --- Targets (verify anytime in the store listings) ---
# Google Play: package id in the store URL ?id=<package>
# App Store: numeric id in the store URL .../id<digits>
APPS = [
    {
        "slug": "chatgpt",
        "label": "ChatGPT",
        "google_play_package": "com.openai.chatgpt",
        "app_store_id": 6448311069,
    },
    {
        "slug": "gemini",
        "label": "Google Gemini",
        "google_play_package": "com.google.android.apps.bard",
        "app_store_id": 6477489729,
    },
    {
        "slug": "claude",
        "label": "Claude",
        "google_play_package": "com.anthropic.claude",
        "app_store_id": 6473753684,
    },
]

# Up to this many reviews per app **per store** (Google Play and App Store each).
# Apple RSS allows at most ~500 reviews per app (10 pages × 50); values above 500
# still cap at what Apple returns. For a quick test: MP1_REVIEWS_PER_STORE=20 ...
REVIEWS_PER_APP_PER_STORE = 500
DEFAULT_PER_STORE = int(
    os.environ.get("MP1_REVIEWS_PER_STORE", str(REVIEWS_PER_APP_PER_STORE))
)
OUTPUT_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_CSV = OUTPUT_DIR / "mp1_reviews_raw.csv"


def fetch_google_play(package: str, max_reviews: int, pause_s: float = 0.25) -> list[dict]:
    """Return newest Google Play reviews as flat dicts."""
    rows: list[dict] = []
    token = None

    while len(rows) < max_reviews:
        batch_size = min(200, max_reviews - len(rows))
        batch, token = gp_reviews(
            package,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=batch_size,
            continuation_token=token,
        )
        for r in batch:
            at = r.get("at")
            if hasattr(at, "isoformat"):
                date_str = at.isoformat()
            else:
                date_str = str(at) if at is not None else ""

            rows.append(
                {
                    "platform": "google_play",
                    "review_id": r.get("reviewId", ""),
                    "rating": r.get("score"),
                    "review_text": (r.get("content") or "").strip(),
                    "title": "",
                    "date": date_str,
                    "app_version": r.get("reviewCreatedVersion") or "",
                    "thumbs_up": r.get("thumbsUpCount", 0),
                    "user_name": r.get("userName", ""),
                }
            )

        if token is None or not batch:
            break

        time.sleep(pause_s)

    return rows[:max_reviews]


def _rss_label(node) -> str:
    """Apple RSS JSON wraps most leaf values as {'label': '...'}."""
    if node is None:
        return ""
    if isinstance(node, dict) and "label" in node:
        return str(node.get("label") or "")
    return str(node)


def fetch_app_store_itunes_rss(
    app_id: int,
    max_reviews: int,
    country: str = "us",
    pause_s: float = 0.35,
) -> list[dict]:
    """
    Return newest App Store reviews using Apple's public RSS JSON endpoint.

    Example URL pattern (document for MP1 provenance):
    https://itunes.apple.com/us/rss/customerreviews/page=1/id=6448311069/sortby=mostrecent/json
    """
    rows: list[dict] = []
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (compatible; HCDE530-MP1/1.0; +https://example.invalid/) "
                "AppleWebKit/537.36 (KHTML, like Gecko)"
            ),
            "Accept": "application/json,text/plain,*/*",
        }
    )

    page = 1
    while len(rows) < max_reviews:
        url = (
            f"https://itunes.apple.com/{country}/rss/customerreviews/"
            f"page={page}/id={app_id}/sortby=mostrecent/json"
        )
        response = session.get(url, timeout=45)
        response.raise_for_status()
        payload = response.json()

        feed = payload.get("feed") or {}
        entries = feed.get("entry") or []

        # When there is exactly one review, ``entry`` may be a dict instead of a list.
        if isinstance(entries, dict):
            entries = [entries]

        if not entries:
            break

        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if "im:rating" not in entry:
                continue

            title = _rss_label(entry.get("title")).strip()
            body = _rss_label(entry.get("content")).strip()
            combined = f"{title}\n{body}".strip() if title else body

            rating_raw = _rss_label(entry.get("im:rating")).strip()
            try:
                rating_val = int(rating_raw) if rating_raw else None
            except ValueError:
                rating_val = None

            rows.append(
                {
                    "platform": "app_store",
                    "review_id": _rss_label(entry.get("id")),
                    "rating": rating_val,
                    "review_text": combined,
                    "title": title,
                    "date": _rss_label(entry.get("updated")),
                    "app_version": _rss_label(entry.get("im:version")),
                    "thumbs_up": _rss_label(entry.get("im:voteSum")),
                    "user_name": _rss_label((entry.get("author") or {}).get("name")),
                }
            )

            if len(rows) >= max_reviews:
                break

        if len(rows) >= max_reviews:
            break

        page += 1
        time.sleep(pause_s)

        # Apple serves at most 10 RSS pages (~50 reviews each); page 11 returns HTTP 400.
        if page > 10:
            break

    return rows[:max_reviews]


def write_csv(path: Path, fieldnames: list[str], table: list[dict]) -> None:
    """Write rows to CSV with UTF-8 encoding."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(table)


def main() -> None:
    per_store = DEFAULT_PER_STORE
    scraped_at = datetime.now(timezone.utc).isoformat()
    print(
        f"Target: up to {per_store} reviews per app per store "
        f"({len(APPS)} apps × 2 stores; App Store RSS max ~500 per app)."
    )

    fieldnames = [
        "scraped_at_utc",
        "app_slug",
        "app_label",
        "platform",
        "review_id",
        "rating",
        "review_text",
        "title",
        "date",
        "app_version",
        "thumbs_up",
        "user_name",
    ]

    all_rows: list[dict] = []

    for app in APPS:
        slug = app["slug"]
        label = app["label"]

        print(f"\n=== {label} (Google Play) ===")
        gp_rows = fetch_google_play(app["google_play_package"], per_store)
        print(f"Collected {len(gp_rows)} Google Play reviews.")
        for row in gp_rows:
            row_out = {
                "scraped_at_utc": scraped_at,
                "app_slug": slug,
                "app_label": label,
                **row,
            }
            all_rows.append(row_out)

        print(f"=== {label} (App Store) ===")
        ios_rows = fetch_app_store_itunes_rss(int(app["app_store_id"]), per_store)
        print(f"Collected {len(ios_rows)} App Store reviews.")
        for row in ios_rows:
            row_out = {
                "scraped_at_utc": scraped_at,
                "app_slug": slug,
                "app_label": label,
                **row,
            }
            all_rows.append(row_out)

    write_csv(OUTPUT_CSV, fieldnames, all_rows)
    print(f"\nWrote {len(all_rows)} rows to {OUTPUT_CSV}")

    print("\nPreview (first 3 rows):")
    with OUTPUT_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 3:
                break
            snippet = (row.get("review_text") or "")[:80].replace("\n", " ")
            print(
                f"  {row.get('app_slug')} | {row.get('platform')} | "
                f"★{row.get('rating')} | {snippet}…"
            )


if __name__ == "__main__":
    main()
