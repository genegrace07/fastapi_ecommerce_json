import csv
import json

csv_file = "data.csv"
json_file = "data.json"

data = []

with open(csv_file, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        row["price"] = int(row["price"])
        row["quantity"] = int(row["quantity"])
        row["id"] = int(row["id"])  # optional but recommended
        data.append(row)

with open(json_file, "w") as file:
    json.dump(data, file, indent=4)

print("CSV converted to JSON successfully!")