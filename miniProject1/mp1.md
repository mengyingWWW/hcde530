# Mini Project 1 — competency claim

All MP1 deliverables live in this **`miniProject1/`** directory: **`mp1.ipynb`**, **`data/mp1_reviews_raw.csv`**, **`charts/*.png`**, and supporting scripts.

## What I demonstrated

I produced a **public, runnable Jupyter notebook** (`mp1.ipynb`) that tells a complete analysis story for someone unfamiliar with the data: **what** I studied (mobile AI assistant reviews from two stores), **where** it came from (documented scrape paths and limitations), **which questions** from MP1a I pursued, and **what I conclude** in plain language—not a walkthrough of code for its own sake.

In **Section 2 (Data Profile)** I ran **`head`**, **`info`**, **`describe`**, and **`isnull().sum()`** and wrote a short interpretation for each so a reader understands table shape, dtypes, and missing fields that constrain claims (for example sparse `app_version` on some rows).

In **Section 3 (Analysis)** I integrated **three static Plotly exports** (built with **kaleido**, committed under `charts/`) so each MP1a question has a **purpose-matched chart type** from the Week 6 guide (bar for categorical comparisons, line for an ordered trend, grouped bars for comparing buckets). Each figure is followed by markdown that states **what the chart argues**—the honest takeaway—rather than narrating Python line-by-line.

In **Section 4 (Conclusions)** I answered each research question in **two to four sentences** as takeaways and named **credible next steps** (thematic coding, release alignment, longer calendar coverage), which mirrors how I would brief a design partner after an early quantitative pass.

**Section 5 (Process)** documents how the work was built (fetch script, A5 pandas, A6 charts, and the chart Q2 redesign) so learning is visible beyond the final PNGs.

## Why this satisfies the competency

I combined **reproducible programmatic analysis** (pandas profile + committed artifacts in one folder), **responsible visualization choices** (full star-scale framing in the underlying A6 exports, aligned recency view where calendar time was misleading), and **communication aimed at HCD practice**—turning noisy public feedback into **prioritized questions** for product judgment rather than over-claiming from a single convenience sample.
