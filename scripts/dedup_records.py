#!/usr/bin/env python3
import argparse
import csv
import os
import re
from collections import defaultdict
from pathlib import Path


def norm_text(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"\s+", " ", value)
    return value


def read_csv_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = {k.strip(): (v or "").strip() for k, v in row.items()}
            row["_file"] = path.name
            yield row


def build_keys(row):
    doi = norm_text(row.get("doi", ""))
    url = norm_text(row.get("url", ""))
    title = norm_text(row.get("title", ""))
    year = norm_text(row.get("year", ""))
    key_doi = f"doi::{doi}" if doi else ""
    key_url = f"url::{url}" if url else ""
    key_title_year = f"titleyear::{title}::{year}" if title and year else ""
    return key_doi, key_url, key_title_year


def merge_rows(base, incoming):
    for field in ["title", "authors", "year", "venue", "abstract", "doi", "url", "source"]:
        if not base.get(field) and incoming.get(field):
            base[field] = incoming[field]
    base["_sources"].add(incoming.get("source", "") or incoming.get("_file", ""))
    return base


def main():
    parser = argparse.ArgumentParser(description="Deduplicate literature search CSV exports.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--report-dir", required=True)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    report_dir = Path(args.report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(input_dir.glob("*.csv"))
    if not csv_files:
        raise SystemExit(f"No CSV files found in {input_dir}")

    records = []
    per_file_counts = {}
    for path in csv_files:
        rows = list(read_csv_rows(path))
        records.extend(rows)
        per_file_counts[path.name] = len(rows)

    unique = []
    key_to_index = {}
    dedup_reason_counts = defaultdict(int)

    for row in records:
        keys = [k for k in build_keys(row) if k]
        matched_index = None
        matched_reason = None
        for key in keys:
            if key in key_to_index:
                matched_index = key_to_index[key]
                matched_reason = key.split("::", 1)[0]
                break

        if matched_index is None:
            canonical = dict(row)
            canonical["_sources"] = {row.get("source", "") or row.get("_file", "")}
            unique.append(canonical)
            idx = len(unique) - 1
            for key in keys:
                key_to_index[key] = idx
        else:
            dedup_reason_counts[matched_reason] += 1
            unique[matched_index] = merge_rows(unique[matched_index], row)
            for key in keys:
                key_to_index[key] = matched_index

    output_fields = ["title", "authors", "year", "venue", "abstract", "doi", "url", "source", "source_set"]
    out_csv = output_dir / "master_dedup.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=output_fields)
        writer.writeheader()
        for row in unique:
            writer.writerow(
                {
                    "title": row.get("title", ""),
                    "authors": row.get("authors", ""),
                    "year": row.get("year", ""),
                    "venue": row.get("venue", ""),
                    "abstract": row.get("abstract", ""),
                    "doi": row.get("doi", ""),
                    "url": row.get("url", ""),
                    "source": row.get("source", ""),
                    "source_set": ";".join(sorted(s for s in row.get("_sources", set()) if s)),
                }
            )

    report = report_dir / "dedup_report.md"
    with report.open("w", encoding="utf-8") as f:
        f.write("# Deduplication Report\n\n")
        f.write(f"- Input files: {len(csv_files)}\n")
        f.write(f"- Raw records: {len(records)}\n")
        f.write(f"- Unique records: {len(unique)}\n")
        f.write(f"- Duplicates removed: {len(records) - len(unique)}\n\n")
        f.write("## Per-file counts\n")
        for name, count in per_file_counts.items():
            f.write(f"- {name}: {count}\n")
        f.write("\n## Duplicate match reasons\n")
        for reason in ["doi", "url", "titleyear"]:
            f.write(f"- {reason}: {dedup_reason_counts.get(reason, 0)}\n")

    print(f"Wrote {out_csv}")
    print(f"Wrote {report}")


if __name__ == "__main__":
    main()
