import csv
import json
from urllib.parse import urlencode
from urllib.request import urlopen


BASE_URL = "https://hcde530-week4-api.onrender.com/reviews"
OUTPUT_FILE = "week4_category_helpful_votes.csv"


def fetch_all_reviews(limit=100):
    """Fetch all review rows from the paginated API endpoint."""
    all_reviews = []
    offset = 0

    while True:
        query = urlencode({"offset": offset, "limit": limit})
        url = f"{BASE_URL}?{query}"

        with urlopen(url) as response:
            payload = json.loads(response.read().decode("utf-8"))

        reviews = payload.get("reviews", [])
        all_reviews.extend(reviews)

        returned = payload.get("returned", len(reviews))
        total = payload.get("total", len(all_reviews))
        if offset + returned >= total or returned == 0:
            break

        offset += returned

    return all_reviews


def save_category_votes_to_csv(rows, output_file):
    """Write category + helpful votes fields to a CSV file."""
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "helpful_votes"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    reviews = fetch_all_reviews()

    category_votes = []
    for review in reviews:
        category = review.get("category", "")
        helpful_votes = review.get("helpful_votes", 0)

        print(f"Category: {category} | Helpful votes: {helpful_votes}")
        category_votes.append(
            {"category": category, "helpful_votes": helpful_votes}
        )

    save_category_votes_to_csv(category_votes, OUTPUT_FILE)
    print(f"\nSaved {len(category_votes)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
