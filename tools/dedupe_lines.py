#!/usr/bin/env python3
"""Drop duplicate lines from a text file, keeping the first occurrence.

Examples:
    python tools/dedupe_lines.py notes.txt
    python tools/dedupe_lines.py log.csv --ignore-case -o clean.csv
"""
import argparse


def main() -> None:
    ap = argparse.ArgumentParser(description="Remove duplicate lines, keep order.")
    ap.add_argument("path", help="input text file")
    ap.add_argument("-o", "--out", help="write to this file instead of stdout")
    ap.add_argument("--ignore-case", action="store_true",
                    help="treat lines differing only in case as duplicates")
    a = ap.parse_args()

    seen = set()
    kept = []
    with open(a.path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            key = line.rstrip("\r\n")
            if a.ignore_case:
                key = key.lower()
            if key in seen:
                continue
            seen.add(key)
            kept.append(line)

    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.writelines(kept)
        print(f"{len(kept)} lines -> {a.out}")
    else:
        print("".join(kept), end="")


if __name__ == "__main__":
    main()
