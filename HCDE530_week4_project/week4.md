# Week 4 — Competency Claim

## What I built

I wrote `week4_pokeapi.py`, a Python script that calls PokéAPI, follows the detail URL for each Pokemon, and extracts five fields: `name`, `types`, `height`, `weight`, and `base_experience`. The script prints a readable summary for each Pokemon and saves the same data to `week4_pokemon_data.csv`.

## What I learned

I learned how to work with nested API responses by making one call for a list endpoint and then a second call for each detail record. I also practiced turning JSON into a clean table format so the output can be inspected in the terminal and reused later in CSV form.

## HCD reflection

From an HCD perspective, choosing fields matters because they shape what users can understand from the data. I picked fields that are easy to compare quickly (name, type, height, weight, experience), then formatted the output for readability so a teammate can scan and use it without reading raw JSON.
