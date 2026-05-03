# Week 5 — A5 competency claim

This file sits in `HCDE530_week5_project/` with other Week 5 materials. The **MP1 review dataset**, fetch script, and **pandas A5 script** are in `miniProject1/` at the repo root (paths below are from that root).

## Dataset

I am working with `miniProject1/data/mp1_reviews_raw.csv`: recent user reviews for **ChatGPT**, **Google Gemini**, and **Claude** from **Google Play** and the **App Store**, collected programmatically with `miniProject1/fetch_mp1_review_data.py` (no API keys). Each row is one review with fields such as `app_label`, `platform`, `rating`, `review_text`, and `date`.

## What I demonstrated in code

In `miniProject1/a5_mp1_reviews.py` I load that CSV with pandas and answer **three** analytical questions: (1) how star ratings are distributed in the full sample, (2) how **mean rating** compares **by app and by store**, and (3) how many **low-star (1–2)** reviews each app contributes for later qualitative analysis. I used the course pandas patterns (`head`, `info`, `isnull().sum`, `value_counts`, filtering with a boolean condition, and `groupby` with `mean`) and added plain-English comments above each call explaining **what I wanted to learn** and **how to read the output**.

## Why this satisfies the competency

I **identified and accessed** real review data tied to my MP1 topic, **posed specific questions** the table can support, **applied basic aggregation and filtering**, and **communicated findings** through printed summaries plus this short claim. This A5 work is the quantitative backbone I will extend in the Week 6 MP1 notebook (themes, cross-app complaints, and update windows).
