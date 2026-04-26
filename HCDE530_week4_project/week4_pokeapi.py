import csv
import json
from urllib.request import Request, urlopen


# This URL calls the Pokemon list endpoint.
# It gives us a page of Pokemon names and detail links (not full stats yet).
LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=200&offset=0"
OUTPUT_FILE = "week4_pokemon_data.csv"


def fetch_json(url):
    """Request JSON data from a URL and return it as a Python dictionary."""
    # Some public APIs reject requests with no user agent header.
    request = Request(url, headers={"User-Agent": "hcde530-week4-script/1.0"})
    with urlopen(request) as response:
        # Each API call returns JSON text, so we decode it and load it into Python.
        return json.loads(response.read().decode("utf-8"))


def extract_pokemon_fields(pokemon_detail):
    """Pull selected fields we want to analyze and store."""
    # These are the five fields we care about for simple comparison:
    # identity (name), category label (types), and size/power signals
    # (height, weight, base_experience).
    name = pokemon_detail.get("name", "")
    height = pokemon_detail.get("height", "")
    weight = pokemon_detail.get("weight", "")
    base_experience = pokemon_detail.get("base_experience", "")

    # Join all type names so each Pokemon has a readable type label.
    type_names = []
    for entry in pokemon_detail.get("types", []):
        type_names.append(entry["type"]["name"])
    types = ", ".join(type_names)

    return {
        "name": name,
        "height": height,
        "weight": weight,
        "base_experience": base_experience,
        "types": types,
    }


def fetch_all_pokemon_items(start_url):
    """Follow paginated list responses until we collect all Pokemon items."""
    all_items = []
    next_url = start_url
    total_count = 0

    while next_url:
        payload = fetch_json(next_url)
        # "count" is the API's total available records.
        total_count = payload.get("count", total_count)
        # "results" holds this page's Pokemon name + detail URL pairs.
        all_items.extend(payload.get("results", []))
        # "next" gives the next page URL; when it is None, we are done.
        next_url = payload.get("next")

    return all_items, total_count


def main():
    # First step gets all paginated Pokemon list rows and their detail URLs.
    pokemon_items, total_count = fetch_all_pokemon_items(LIST_URL)
    print(f"Found {total_count} total Pokemon records from the API.")

    extracted_rows = []
    for item in pokemon_items:
        # We call each detail URL to get full Pokemon data for one record.
        detail_payload = fetch_json(item["url"])
        row = extract_pokemon_fields(detail_payload)
        extracted_rows.append(row)

    # Write a clean table to CSV so this API data can be reused in later analysis.
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "types", "height", "weight", "base_experience"],
        )
        writer.writeheader()
        writer.writerows(extracted_rows)

    # Print a small preview instead of all rows so output stays readable.
    print("\nPreview (first 10 rows):")
    for row in extracted_rows[:10]:
        print(
            f"{row['name']}: types={row['types']}, "
            f"height={row['height']}, weight={row['weight']}, "
            f"base_experience={row['base_experience']}"
        )

    print(f"\nSaved {len(extracted_rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
