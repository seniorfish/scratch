#!/usr/bin/env python3
"""Print per-column summary statistics for a CSV file.

Example:
    python tools/csv_stats.py data.csv --delimiter ';'

Columns whose non-empty values all parse as numbers report count, min, max and
mean; other columns report count and the number of distinct values.
"""
import argparse
import csv
import statistics
import sys


def main() -> None:
    ap = argparse.ArgumentParser(description="Summarise CSV columns.")
    ap.add_argument("path", help="input CSV file")
    ap.add_argument("--delimiter", default=",", help="field delimiter (default: ,)")
    a = ap.parse_args()

    with open(a.path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh, delimiter=a.delimiter))

    if not rows:
        sys.exit("empty file")
    if not rows[0]:
        sys.exit("no header row")

    width = max(len(name) for name in rows[0])
    for col in rows[0]:
        values = [r[col] for r in rows if r.get(col, "").strip()]
        numbers = []
        for value in values:
            try:
                numbers.append(float(value))
            except ValueError:
                pass

        if values and len(numbers) == len(values):
            print(f"{col:<{width}}  n={len(values):<5} numeric  "
                  f"min={min(numbers):g}  max={max(numbers):g}  "
                  f"mean={statistics.fmean(numbers):.4g}")
        else:
            print(f"{col:<{width}}  n={len(values):<5} text     "
                  f"unique={len(set(values))}")


if __name__ == "__main__":
    main()
