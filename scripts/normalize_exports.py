#!/usr/bin/env python3
"""Normalize raw CSV exports from IEEE Xplore and Web of Science into the
standard schema expected by dedup_records.py.

Usage:
    python scripts/normalize_exports.py

Reads all CSVs in data/raw-search/ and rewrites them in place with the
standard columns: title, authors, year, venue, abstract, doi, url, source

Handles:
  - IEEE Xplore CSV (columns like "Document Title", "Authors", etc.)
  - Web of Science CSV/TSV (columns like "Article Title", "Author Full Names", etc.)
  - Already-normalized files (arxiv_raw.csv, s2_raw.csv) are left unchanged.
"""

import csv
import re
from pathlib import Path

STANDARD_FIELDS = ["title", "authors", "year", "venue", "abstract", "doi", "url", "source"]

# Mapping: standard field -> list of possible source column names (case-insensitive)
COLUMN_MAP = {
    "title": ["title", "document title", "article title", "ti"],
    "authors": ["authors", "author full names", "author names", "au", "author"],
    "year": ["year", "publication year", "py"],
    "venue": ["venue", "publication title", "source title", "journal/book", "so", "journal"],
    "abstract": ["abstract", "ab"],
    "doi": ["doi", "di"],
    "url": ["url", "pdf link", "article url", "ut"],
    "source": ["source"],
}

SOURCE_DETECTION = {
    "ieee": ["ieee", "ieeexplore"],
    "wos": ["wos", "web_of_science", "webofscience"],
    "acm": ["acm"],
    "scopus": ["scopus"],
    "arxiv": ["arxiv"],
    "semantic_scholar": ["s2", "semantic_scholar", "semanticscholar"],
}


def detect_source(filename: str) -> str:
    name = filename.lower().replace("-", "_").replace(" ", "_")
    for source, patterns in SOURCE_DETECTION.items():
        for p in patterns:
            if p in name:
                return source
    return "unknown"


def find_column(headers: list[str], candidates: list[str]) -> str | None:
    header_lower = {h.strip().lower(): h for h in headers}
    for candidate in candidates:
        if candidate in header_lower:
            return header_lower[candidate]
    return None


def extract_year(value: str) -> str:
    """Extract a 4-digit year from various formats."""
    match = re.search(r"(19|20)\d{2}", value or "")
    return match.group(0) if match else ""


def normalize_file(path: Path) -> int:
    """Normalize a single CSV. Returns number of rows written."""
    source = detect_source(path.stem)

    # Read raw content
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        # Try to detect delimiter
        sample = f.read(4096)
        f.seek(0)
        if "\t" in sample and "," not in sample.split("\n")[0]:
            delimiter = "\t"
        else:
            delimiter = ","
        reader = csv.DictReader(f, delimiter=delimiter)
        if reader.fieldnames is None:
            print(f"  SKIP {path.name}: no headers found")
            return 0

        headers = list(reader.fieldnames)

        # Check if already normalized
        header_set = {h.strip().lower() for h in headers}
        if header_set >= set(STANDARD_FIELDS):
            print(f"  SKIP {path.name}: already normalized")
            return 0

        # Build column mapping
        col_map = {}
        for std_field, candidates in COLUMN_MAP.items():
            found = find_column(headers, candidates)
            col_map[std_field] = found

        print(f"  Mapping for {path.name} (source={source}):")
        for std, raw in col_map.items():
            print(f"    {std} <- {raw}")

        rows = []
        for raw_row in reader:
            row = {}
            for std_field in STANDARD_FIELDS:
                raw_col = col_map.get(std_field)
                if raw_col and raw_col in raw_row:
                    row[std_field] = raw_row[raw_col].strip()
                else:
                    row[std_field] = ""

            # Fix year
            if row["year"]:
                row["year"] = extract_year(row["year"])

            # Set source
            if not row["source"]:
                row["source"] = source

            rows.append(row)

    # Write back normalized
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=STANDARD_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def main():
    input_dir = Path("data/raw-search")
    csv_files = sorted(input_dir.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files in {input_dir}")
        return

    for path in csv_files:
        if path.name == "export_template.csv":
            continue
        print(f"\nProcessing {path.name}...")
        count = normalize_file(path)
        if count:
            print(f"  -> {count} rows normalized")


if __name__ == "__main__":
    main()
