#!/usr/bin/env python3
"""Calculate a transparent feature-coverage score from a CSV matrix."""
import argparse
import csv
import sys

WEIGHTS = {"must": 3, "should": 2, "could": 1}
STATUS = {"done": 1.0, "complete": 1.0, "partial": 0.5}

def truthy(value):
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--strict", action="store_true", help="fail if any must-have is not done")
    args = parser.parse_args()
    total = earned = 0.0
    missing_must = []
    included = 0
    with open(args.csv_path, newline="", encoding="utf-8-sig") as handle:
        for number, row in enumerate(csv.DictReader(handle), start=2):
            priority = str(row.get("priority", "")).strip().lower()
            status = str(row.get("status", "")).strip().lower()
            if priority not in WEIGHTS or status == "out-of-scope" or truthy(row.get("intentional_difference")):
                continue
            included += 1
            weight = WEIGHTS[priority]
            total += weight
            earned += weight * STATUS.get(status, 0.0)
            if priority == "must" and STATUS.get(status, 0.0) < 1.0:
                missing_must.append(row.get("id") or row.get("capability") or f"row {number}")
    score = 100.0 if total == 0 else earned / total * 100
    print(f"Included: {included}")
    print(f"Coverage: {score:.1f}% ({earned:.1f}/{total:.1f} weighted points)")
    if missing_must:
        print("Missing must-haves:")
        for item in missing_must:
            print(f"- {item}")
    else:
        print("Missing must-haves: none")
    return 1 if args.strict and missing_must else 0

if __name__ == "__main__":
    sys.exit(main())
