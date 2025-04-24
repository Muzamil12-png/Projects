import csv

from collections import Counter

with open("Favourites.csv", "r") as file:
    reader = csv.DictReader(file)
    counts = Counter()

    for row in reader:
        favourite = row["problem"]
        counts[favourite] += 1

for favourite in sorted(counts, key=counts.get, reverse=True):
    print(f"{favourite}: {counts[favourite]}")
