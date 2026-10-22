#!/usr/bin/env python3
"""Check WCAG contrast for token pairs using only the standard library."""
import argparse
import json
import re
import sys

HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

def rgb(value):
    match = HEX.match(str(value).strip())
    if not match:
        raise ValueError(f"unsupported color: {value!r}")
    raw = match.group(1)
    if len(raw) == 3:
        raw = "".join(char * 2 for char in raw)
    return tuple(int(raw[index:index + 2], 16) / 255 for index in (0, 2, 4))

def luminance(value):
    channels = []
    for channel in rgb(value):
        channels.append(channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]

def ratio(foreground, background):
    first, second = luminance(foreground), luminance(background)
    return (max(first, second) + 0.05) / (min(first, second) + 0.05)

def pairs(value, path="tokens"):
    if isinstance(value, dict):
        if "foreground" in value and "background" in value:
            yield path, value["foreground"], value["background"]
        for key, child in value.items():
            yield from pairs(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from pairs(child, f"{path}[{index}]")

def report(name, foreground, background):
    value = ratio(foreground, background)
    normal = value >= 4.5
    large = value >= 3.0
    aaa_normal = value >= 7.0
    print(f"{name}: {foreground} on {background} = {value:.2f}:1 | AA normal={'PASS' if normal else 'FAIL'} large={'PASS' if large else 'FAIL'} | AAA normal={'PASS' if aaa_normal else 'FAIL'}")
    return normal and large

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", nargs="?")
    parser.add_argument("--foreground")
    parser.add_argument("--background")
    args = parser.parse_args()
    failed = False
    if args.foreground or args.background:
        if not args.foreground or not args.background:
            parser.error("--foreground and --background must be used together")
        try:
            failed = not report("direct", args.foreground, args.background)
        except ValueError as error:
            parser.error(str(error))
    elif args.json_path:
        with open(args.json_path, encoding="utf-8-sig") as handle:
            data = json.load(handle)
        found = 0
        for name, foreground, background in pairs(data):
            try:
                failed = (not report(name, foreground, background)) or failed
                found += 1
            except ValueError as error:
                print(f"{name}: SKIP ({error})")
        if not found:
            print("No objects with foreground/background pairs found.")
    else:
        parser.error("provide a JSON path or both color flags")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
