#!/usr/bin/env python3
"""Split second-pass uncertain triage into actionable bucket CSVs."""

import csv
from pathlib import Path

INPUT = Path("data/processed/uncertain_second_pass.csv")
OUT_DIR = Path("data/processed")

BUCKETS = {
    "likely_include": OUT_DIR / "uncertain_likely_include.csv",
    "likely_exclude": OUT_DIR / "uncertain_likely_exclude.csv",
    "needs_manual": OUT_DIR / "uncertain_needs_manual.csv",
}


def main():
    with INPUT.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise SystemExit("No rows found in uncertain_second_pass.csv")

    fields = rows[0].keys()
    for bucket, path in BUCKETS.items():
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                if row.get("second_pass_recommendation") == bucket:
                    writer.writerow(row)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
