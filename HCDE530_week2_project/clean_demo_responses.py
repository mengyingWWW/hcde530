import csv


INPUT_FILE = "demo_responses.csv"
OUTPUT_FILE = "responses_cleaned.csv"


def clean_responses(input_file, output_file):
    """Clean survey data and write cleaned rows to a new CSV file.

    - Drops rows where the 'name' column exists and is empty.
    - Uppercases values in the 'role' column.
    """
    with open(input_file, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        if not fieldnames:
            raise ValueError("Input CSV has no header row.")

        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                # Remove rows only when a 'name' field exists but is empty.
                if "name" in row and row["name"].strip() == "":
                    continue

                # Convert role values to uppercase when the column exists.
                if "role" in row and row["role"] is not None:
                    row["role"] = row["role"].upper()

                writer.writerow(row)


if __name__ == "__main__":
    clean_responses(INPUT_FILE, OUTPUT_FILE)
    print(f"Cleaned data written to: {OUTPUT_FILE}")
