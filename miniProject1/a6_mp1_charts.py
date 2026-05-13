"""
A6: build Plotly charts from MP1 review CSV and save static PNGs under charts/.

Run from anywhere:

    python3 miniProject1/a6_mp1_charts.py

Requires: pip install plotly kaleido pandas
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px

MP1_DIR = Path(__file__).resolve().parent
DATA_PATH = MP1_DIR / "data" / "mp1_reviews_raw.csv"
CHART_DIR = MP1_DIR / "charts"


def load_reviews() -> pd.DataFrame:
    """Load MP1 review table and parse review timestamps."""
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["review_dt"] = pd.to_datetime(df["date"], utc=True, format="mixed")
    return df


def chart_q1_low_star_share_by_app(df: pd.DataFrame) -> None:
    """
    MP1a Q1 (proxy): where is visible dissatisfaction concentrated before full
    thematic coding of usability complaints?
    """
    low = df["rating"] <= 2
    summary = (
        df.assign(low_star=low.astype(float))
        .groupby("app_label", dropna=False)["low_star"]
        .mean()
        .mul(100)
        .reset_index()
        .rename(columns={"low_star": "pct_low_star"})
    )

    fig = px.bar(
        summary,
        x="app_label",
        y="pct_low_star",
        text=summary["pct_low_star"].round(1).astype(str) + "%",
        title="Share of 1–2 star reviews by AI app (proxy for concentrated pain)",
        labels={
            "app_label": "App",
            "pct_low_star": "Percent of reviews (%)",
        },
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        yaxis_title="Percent of reviews (%)",
        yaxis=dict(range=[0, max(45, summary["pct_low_star"].max() * 1.15)]),
        xaxis_title="App",
        template="plotly_white",
    )
    fig.write_image(str(CHART_DIR / "chart_q1_low_star_share_by_app.png"), scale=2)


def _assign_recency_decile(group: pd.DataFrame) -> pd.DataFrame:
    """
    Within one app, sort newest-first and tag equal-count deciles (1=newest 10%).
    Aligns apps on scrape position instead of mismatched calendar windows.
    """
    g = group.sort_values("review_dt", ascending=False, na_position="last").copy()
    positions = range(len(g))
    g["decile"] = pd.qcut(positions, q=10, labels=False, duplicates="drop").astype(int) + 1
    return g


def chart_q2_mean_rating_by_recency_decile(df: pd.DataFrame) -> None:
    """
    MP1a Q2 (aligned view): does mean rating change from the newest slice of each
    app's scrape to the oldest slice? Calendar weeks mislead when each app's
    reviews span different date ranges for the same row count.
    """
    core = df.dropna(subset=["review_dt", "rating"]).copy()
    deciled_parts = []
    for _, g in core.groupby("app_label"):
        deciled_parts.append(_assign_recency_decile(g))
    deciled = pd.concat(deciled_parts, ignore_index=True)
    summary = (
        deciled.groupby(["app_label", "decile"], observed=False)["rating"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        summary,
        x="decile",
        y="rating",
        color="app_label",
        markers=True,
        title=(
            "Mean star rating by recency decile within each app's sample "
            "(1 = newest 10% of reviews in scrape, 10 = oldest 10%)"
        ),
        labels={
            "decile": "Recency decile (1 = newest 10% in this scrape)",
            "rating": "Mean star rating (1–5 scale)",
            "app_label": "App",
        },
    )
    fig.update_layout(
        yaxis=dict(range=[0, 5], title="Mean star rating (1–5 scale)"),
        xaxis=dict(dtick=1, title="Recency decile (1 = newest 10% in this scrape)"),
        template="plotly_white",
        legend_title_text="App",
    )
    fig.write_image(
        str(CHART_DIR / "chart_q2_mean_rating_by_recency_decile.png"), scale=2
    )


def chart_q3_keyword_themes_1_vs_5_star(df: pd.DataFrame) -> None:
    """
    MP1a Q3 (pilot): simple keyword flags — how often do 1-star vs 5-star
    reviews mention speed, accuracy, or memory/context language?
    """
    themes = {
        "Speed / responsiveness": r"slow|fast|speed|lag|latency|delay|quick",
        "Accuracy / trust": r"wrong|incorrect|mistake|hallucin|inaccurate|error|lie",
        "Memory / context": r"memory|forget|context|history|remembers|previous",
    }

    subset = df[df["rating"].isin([1, 5])].copy()
    text = subset["review_text"].fillna("").str.lower()

    for name, pattern in themes.items():
        subset[name] = text.str.contains(pattern, regex=True, na=False)

    long = subset.melt(
        id_vars=["rating"],
        value_vars=list(themes.keys()),
        var_name="theme",
        value_name="mentioned",
    )
    agg = (
        long.groupby(["rating", "theme"], as_index=False)["mentioned"]
        .mean()
        .assign(pct=lambda d: d["mentioned"] * 100)
    )
    agg["rating_label"] = agg["rating"].astype(int).astype(str) + " stars"

    fig = px.bar(
        agg,
        x="theme",
        y="pct",
        color="rating_label",
        barmode="group",
        title="Pilot keyword themes: share of 1-star vs 5-star reviews mentioning each theme",
        labels={
            "theme": "Theme (simple keyword match in review text)",
            "pct": "Percent of reviews in that star bucket (%)",
            "rating_label": "Star rating",
        },
    )
    fig.update_layout(
        yaxis=dict(range=[0, max(35, agg["pct"].max() * 1.1)]),
        yaxis_title="Percent of reviews in that star bucket (%)",
        xaxis_title="Theme (simple keyword match in review text)",
        template="plotly_white",
        legend_title_text="Star rating",
    )
    fig.write_image(str(CHART_DIR / "chart_q3_keyword_themes_1_vs_5_star.png"), scale=2)


def main() -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    df = load_reviews()
    chart_q1_low_star_share_by_app(df)
    chart_q2_mean_rating_by_recency_decile(df)
    chart_q3_keyword_themes_1_vs_5_star(df)
    print(f"Wrote PNG charts to {CHART_DIR}")


if __name__ == "__main__":
    main()
