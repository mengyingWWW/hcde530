import csv

# Load the survey data from a CSV file
filename = "week3_survey_messy.csv"
cleaned_filename = "week3_survey_cleaned.csv"
rows = []
cleaned_rows = []

with open(filename, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    # This loop visits each survey row, cleans key fields, and stores cleaned rows.
    for row in reader:
        # Clean role text so different capitalization is counted as one role value.
        row["role"] = row["role"].strip().title()
        if not row["role"]:
            row["role"] = "Unknown"

        # Clean experience_years so later int() math does not crash on text values.
        experience_value = row["experience_years"].strip().lower()
        if experience_value == "fifteen":
            row["experience_years"] = "15"

        rows.append(row)
        cleaned_rows.append(row)

# Count responses by role
# Normalize role names so "ux researcher" and "UX Researcher" are counted together
role_counts = {}

for row in rows:
    role = row["role"]
    if role in role_counts:
        role_counts[role] += 1
    else:
        role_counts[role] = 1

print("Responses by role:")
for role, count in sorted(role_counts.items()):
    print(f"  {role}: {count}")

# Calculate the average years of experience
total_experience = 0
for row in rows:
    total_experience += int(row["experience_years"])

avg_experience = total_experience / len(rows)
print(f"\nAverage years of experience: {avg_experience:.1f}")

# Find the top 5 highest satisfaction scores
scored_rows = []
for row in rows:
    if row["satisfaction_score"].strip():
        scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))

scored_rows.sort(key=lambda x: x[1], reverse=True)
top5 = scored_rows[:5]

print("\nTop 5 satisfaction scores:")
for name, score in top5:
    print(f"  {name}: {score}")

# Save cleaned rows so the script produces a cleaned output file.
with open(cleaned_filename, "w", newline="", encoding="utf-8") as out_f:
    writer = csv.DictWriter(out_f, fieldnames=fieldnames)
    # Write the same CSV header columns to the cleaned output file.
    writer.writeheader()
    # Write all cleaned rows (normalized role and fixed experience values).
    writer.writerows(cleaned_rows)

print(f"\nCleaned file written: {cleaned_filename}")
