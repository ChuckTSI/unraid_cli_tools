#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path


def mask_json_values(data):
    if isinstance(data, dict):
        return {key: mask_json_values(value) for key, value in data.items()}
    if isinstance(data, list):
        return [mask_json_values(item) for item in data]
    return "XXXXXXXXXXXXXXXX"


def main():
    parser = argparse.ArgumentParser(
        description="Mask JSON values while keeping keys visible."
    )
    parser.add_argument("input_file", help="Path to the source JSON file")
    parser.add_argument(
        "-o",
        "--output",
        help="Optional path to write the masked JSON file. Defaults to stdout.",
    )
    args = parser.parse_args()

    input_path = Path(args.input_file)

    try:
        with input_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {input_path}: {exc}", file=sys.stderr)
        sys.exit(1)

    masked = mask_json_values(data)
    output_text = json.dumps(masked, indent=2) + "\n"

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output_text, encoding="utf-8")
    else:
        sys.stdout.write(output_text)


if __name__ == "__main__":
    main()
