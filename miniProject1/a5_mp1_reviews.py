"""
A5: exploratory pandas analysis on MP1 app review data (ChatGPT, Gemini, Claude).

Loads miniProject1/data/mp1_reviews_raw.csv produced by fetch_mp1_review_data.py.

Run (from repo root, with pandas installed):

    python3 miniProject1/a5_mp1_reviews.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "data" / "mp1_reviews_raw.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")

    # --- Shared exploration (course operations: head, info) ---

    # What am I asking: what do individual rows look like, and which columns will I use for MP1?
    # What the answer means: I can confirm each row is one review with app, store, rating, text, and timestamps aligned with my scrape.
    print("=== df.head() ===")
    print(df.head())

    # What am I asking: how many reviews loaded, what dtypes does pandas infer, and are any columns stored as strings when they should be numeric?
    # What the answer means: I learn the table size (~3k rows if full scrape), non-null counts per column, and whether I need to coerce types before math.
    print("\n=== df.info() ===")
    df.info()

    # What am I asking: which fields are missing, and will gaps block questions about version or thumbs-up?
    # What the answer means: larger counts here flag columns I should treat carefully (for example App Store rows often lack app_version in this dataset).
    print("\n=== df.isnull().sum() ===")
    print(df.isnull().sum())

    # Coerce rating for reliable comparisons (some rows may parse as float after nulls).
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    # ------------------------------------------------------------------
    # Question 1: How are star ratings distributed across the whole dataset?
    # ------------------------------------------------------------------

    # What am I asking: which star ratings are most common overall, suggesting overall sentiment skew?
    # What the answer means: if 5 dominates, the sample leans positive; a heavier 1–2 tail would signal widespread frustration worth mining in text.
    print("\n=== Q1: value_counts — rating ===")
    print(df["rating"].value_counts(dropna=False).sort_index())

    # ------------------------------------------------------------------
    # Question 2: For each AI app and each store, what is the average star rating?
    # ------------------------------------------------------------------

    # What am I asking: after grouping by app and platform, what is the mean rating in each bucket?
    # What the answer means: I can compare ChatGPT vs Gemini vs Claude on Google Play vs App Store and spot systematic store-level differences (for example stricter reviewers on one side).
    print("\n=== Q2: groupby mean rating by app and platform ===")
    grouped = (
        df.groupby(["app_label", "platform"], dropna=False)["rating"]
        .mean()
        .round(3)
    )
    print(grouped)

    # ------------------------------------------------------------------
    # Question 3: How many low-star (1–2) reviews exist per app for deeper text analysis later?
    # ------------------------------------------------------------------

    # What am I asking: which rows are clearly critical feedback (rating 1 or 2) so I can study pain points?
    # What the answer means: the row count per app tells me how much negative voice I have for MP1 thematic coding (more rows means stronger evidence for usability issues).
    print("\n=== Q3: filter rating <= 2, then counts by app ===")
    critical = df[df["rating"] <= 2]
    print(critical["app_label"].value_counts())
    print(f"\nTotal critical reviews (1–2 stars): {len(critical)}")


if __name__ == "__main__":
    main()
