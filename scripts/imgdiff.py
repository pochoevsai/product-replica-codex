#!/usr/bin/env python3
"""Compare supported 8-bit RGB/RGBA PNGs without third-party packages."""
import argparse
import json
import struct
import sys
import zlib

def read_png(path):
    with open(path, "rb") as handle:
        data = handle.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    position = 8
    idat = bytearray()
    width = height = color_type = bit_depth = interlace = None
    while position < len(data):
        length = struct.unpack(">I", data[position:position + 4])[0]
        kind = data[position + 4:position + 8]
        chunk = data[position + 8:position + 8 + length]
        position += 12 + length
        if kind == b"IHDR":
            width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(">IIBBBBB", chunk)
            if bit_depth != 8 or color_type not in (2, 6) or compression != 0 or filtering != 0 or interlace != 0:
                raise ValueError("only non-interlaced 8-bit RGB/RGBA PNGs are supported")
        elif kind == b"IDAT":
            idat.extend(chunk)
        elif kind == b"IEND":
            break
    if width is None or height is None:
        raise ValueError("PNG has no IHDR")
    channels = 3 if color_type == 2 else 4
    raw = zlib.decompress(bytes(idat))
    stride = width * channels
    rows = []
    offset = 0
    previous = bytearray(stride)
    for _ in range(height):
        filter_type = raw[offset]
        current = bytearray(raw[offset + 1:offset + 1 + stride])
        offset += stride + 1
        for index in range(stride):
            left = current[index - channels] if index >= channels else 0
            up = previous[index]
            upper_left = previous[index - channels] if index >= channels else 0
            if filter_type == 1:
                current[index] = (current[index] + left) & 255
            elif filter_type == 2:
                current[index] = (current[index] + up) & 255
            elif filter_type == 3:
                current[index] = (current[index] + ((left + up) // 2)) & 255
            elif filter_type == 4:
                estimate = left + up - upper_left
                distances = (abs(estimate - left), abs(estimate - up), abs(estimate - upper_left))
                current[index] = (current[index] + (left if distances[0] <= distances[1] and distances[0] <= distances[2] else up if distances[1] <= distances[2] else upper_left)) & 255
            elif filter_type != 0:
                raise ValueError(f"unsupported PNG filter: {filter_type}")
        rows.append(current)
        previous = current
    return width, height, channels, rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("original")
    parser.add_argument("clone")
    parser.add_argument("--out", default="diff.json")
    args = parser.parse_args()
    first = read_png(args.original)
    second = read_png(args.clone)
    if first[:2] != second[:2]:
        result = {"same_dimensions": False, "original": first[:2], "clone": second[:2], "changed_pixel_ratio": 1.0}
    else:
        width, height = first[:2]
        changed = 0
        total_error = 0
        total_channels = width * height * 3
        for row_a, row_b in zip(first[3], second[3]):
            for index in range(0, width * first[2], first[2]):
                pixel_a = row_a[index:index + 3]
                pixel_b = row_b[index:index + 3]
                error = sum(abs(a - b) for a, b in zip(pixel_a, pixel_b))
                total_error += error
                changed += error > 0
        result = {"same_dimensions": True, "width": width, "height": height, "changed_pixel_ratio": changed / (width * height), "mean_channel_error": total_error / total_channels}
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, zlib.error) as error:
        print(f"imgdiff: {error}", file=sys.stderr)
        sys.exit(1)
