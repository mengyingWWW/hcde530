# Week 2 — Competency Claim

## What I built

I wrote a Python script (`demo_word_count.py`) that reads `demo_responses.csv` (participant id, role, and a short text response), counts words in each response, prints a neat row-by-row table in the terminal, and ends with summary stats (count, shortest, longest, and average word length).

## What I learned

`csv.DictReader` was the piece that clicked for me: each row becomes a dictionary keyed by the header names, so I can pull `response` without remembering column indexes. I also got more comfortable breaking logic into a small function (`count_words`) and adding comments where the code alone would not remind me why something works the way it does. The terminal is still the part that felt the most confusing at first—running the script, checking paths, and trusting that the output I see matches the file I think I edited.

## How this shows my competency

This week’s work connects directly to working with data in a plain, reproducible way (structured CSV in, summarized numbers out) instead of only skimming the spreadsheet by eye. I used Cursor as a pair-programming aid for small steps and explanations, while still reading and owning the Python so I understand what runs. Together with writing and reading code (functions, loops, formatted printing) and keeping the project in Github repository, the script is a concrete artifact I can point to that shows I can load a dataset, transform it, and communicate what I found.
