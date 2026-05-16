# Mini Project 1 — stand-alone package

This folder is the **complete MP1 submission**: notebook, data, charts, and scripts.

| Item | Purpose |
|------|---------|
| `mp1.ipynb` | Published analysis (Sections 1–5) |
| `mp1.md` | Competency claim |
| `data/mp1_reviews_raw.csv` | Review dataset |
| `charts/*.png` | Static A6 figures (also embedded in the notebook) |
| `fetch_mp1_review_data.py` | Rebuild the CSV from store sources |
| `a5_mp1_reviews.py` | Week 5 pandas exploration |
| `a6_mp1_charts.py` | Week 6 chart generation |

**Run the notebook:** open `mp1.ipynb`, use **Kernel → Restart & Run All** (first cell installs `jupyter plotly kaleido pandas`).

**Regenerate charts:**

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 a6_mp1_charts.py
```
