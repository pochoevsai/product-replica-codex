#!/usr/bin/env python3
"""Check common store-listing constraints and target-name residue."""
import argparse
import json
import re
import sys

LIMITS = {"title": 30, "subtitle": 30, "promotional_text": 170, "keywords": 100, "description": 4000}
RANKING = re.compile(r"\b(number|#?1|best|top|อันดับ|лучший|№\s*1)\b", re.IGNORECASE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path")
    parser.add_argument("--avoid", action="append", default=[])
    args = parser.parse_args()
    with open(args.json_path, encoding="utf-8-sig") as handle:
        data = json.load(handle)
    errors = 0
    text_fields = []
    for field, limit in LIMITS.items():
        value = data.get(field, "")
        if not isinstance(value, str):
            print(f"{field}: SKIP (not a string)")
            continue
        text_fields.append(value)
        status = "PASS" if len(value) <= limit else "FAIL"
        print(f"{field}: {len(value)}/{limit} {status}")
        errors += status == "FAIL"
    combined = "\n".join(text_fields)
    if RANKING.search(combined):
        print("ranking claims: WARNING (review and substantiate or remove)")
    for term in args.avoid:
        if term and term.casefold() in combined.casefold():
            print(f"avoided term: FAIL ({term})")
            errors += 1
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
