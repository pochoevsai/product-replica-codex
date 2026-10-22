#!/usr/bin/env python3
"""Find forbidden target identity terms in source and text files."""
import argparse
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", "coverage", "__pycache__", ".venv"}
TEXT_EXTENSIONS = {".css", ".csv", ".html", ".js", ".jsx", ".json", ".md", ".py", ".scss", ".sh", ".sql", ".ts", ".tsx", ".txt", ".tsx", ".vue", ".yaml", ".yml"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--avoid", action="append", required=True)
    args = parser.parse_args()
    terms = [(term, re.compile(re.escape(term), re.IGNORECASE)) for term in args.avoid if term]
    matches = 0
    root = os.path.abspath(args.path)
    for directory, subdirs, files in os.walk(root):
        subdirs[:] = [name for name in subdirs if name not in SKIP_DIRS]
        for filename in files:
            full = os.path.join(directory, filename)
            if os.path.splitext(filename)[1].lower() not in TEXT_EXTENSIONS:
                continue
            try:
                with open(full, encoding="utf-8", errors="strict") as handle:
                    for line_number, line in enumerate(handle, start=1):
                        for term, pattern in terms:
                            if pattern.search(line):
                                print(f"{os.path.relpath(full, root)}:{line_number}: {term}")
                                matches += 1
            except (OSError, UnicodeError):
                continue
    print(f"Matches: {matches}")
    return 1 if matches else 0

if __name__ == "__main__":
    sys.exit(main())
