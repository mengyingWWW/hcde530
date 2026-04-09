import csv


# Load the CSV file
filename = "demo_responses.csv"
responses = []

with open(filename, newline="", encoding="utf-8") as f:
    # DictReader maps each row to a dict using the header names as keys.
    reader = csv.DictReader(f)
    for row in reader:
        # Store each participant record so we can process it later.
        responses.append(row)


def count_words(response):
    """Count the number of words in a response string.

    Takes a string, splits it on whitespace, and returns the word count.
    Used to measure response length across all participants.
    """
    return len(response.split())


# Count words in each response and print a row-by-row summary so that we have readable output
# Print a fixed-width header so columns line up in the terminal.
print(f"{'ID':<6} {'Role':<22} {'Words':<6} {'Response (first 60 chars)'}")
print("-" * 75)

# Collect all word counts for summary stats at the end.
word_counts = []

for row in responses:
    # Pull values from each CSV row by column name.
    participant = row["participant_id"]
    role = row["role"]
    response = row["response"]

    # Call our function to count words in this response
    count = count_words(response)
    word_counts.append(count)

    # Truncate the response preview for display
    if len(response) > 60:
        # Keep table output compact by showing only the first 60 characters.
        preview = response[:60] + "..."
    else:
        preview = response

    # Print one formatted row per participant.
    print(f"{participant:<6} {role:<22} {count:<6} {preview}")

# Print summary statistics
print()
print("── Summary ─────────────────────────────────")
print(f"  Total responses : {len(word_counts)}")
# min/max/average summarize response-length spread across all participants.
print(f"  Shortest        : {min(word_counts)} words")
print(f"  Longest         : {max(word_counts)} words")
print(f"  Average         : {sum(word_counts) / len(word_counts):.1f} words")
