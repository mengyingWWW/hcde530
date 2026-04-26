# Week 2 — Competency Claim

## What I built

I wrote a Python script (`demo_word_count.py`) that reads `demo_responses.csv` with `csv.DictReader`, so each row is accessed by column names like `participant_id`, `role`, and `response`. The script prints a fixed-width table in the terminal and truncates long responses to 60 characters so each row stays readable. It then prints summary stats (`Total responses`, `Shortest`, `Longest`, `Average`) from the collected word counts.

## What I learned

`csv.DictReader` was the piece that clicked for me because it made the loop clearer: I could pull fields by name instead of tracking index positions. Writing `count_words(response)` helped me see how a small helper function makes the main loop easier to read and reuse. I also learned that comments are strongest when they explain intent (for example, why I truncate previews and why min/max/average are included), not when they just restate Python syntax.

## How this shows my competency

This artifact shows competency because the code makes deliberate, visible choices: dictionary-based CSV reading, a named counting function, readable terminal formatting, and explicit summary metrics. Those choices demonstrate that I can move from raw text responses to interpretable evidence rather than just printing raw rows. It also shows code literacy and documentation practice, because the inline comments explain why these steps exist and make the script understandable when I revisit it.
