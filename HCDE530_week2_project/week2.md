# Week 2 — Competency claim

Short competency claims for HCDE 530 (Week 2). Each section is a few sentences tied to work in this repo.

## Data handling and analysis

I practiced treating `demo_responses.csv` as structured input: opening it with an explicit path and UTF-8 encoding, reading rows with `csv.DictReader`, and turning free-text responses into a measurable quantity (word counts) I could scan in the terminal. Summarizing those counts gave me a simple way to compare response length across participants instead of only reading answers one at a time.

## Programming and implementation

I kept the Python script beginner-readable by using a small reusable function for counting words and printing a labeled, column-aligned table so output is easy to sanity-check. I also used Cursor prompts to move through the script step by step when I was unsure about the next change, which helped me connect syntax to intent without skipping the reasoning.

## Code literacy and documentation

I asked for inline comments where the intent is not obvious from the code alone (for example, how `DictReader` maps headers to keys), because comments anchor my memory when I reopen the file later. I also skimmed project-level Cursor rules so I could align with expectations that apply across the whole repo, not only in one script.

## Reflection (where I felt friction)

The terminal still took the most mental energy this week—knowing what to type, whether a command “worked,” and how that connects to the files on disk. Naming that friction matters to me because it tells me what to practice next so the technical workflow feels less like a barrier to the analysis itself.
