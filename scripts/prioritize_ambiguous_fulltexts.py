#!/usr/bin/env python3
"""Create a prioritized review queue for ambiguous papers with full-text discovery data."""

import csv
from collections import Counter
from pathlib import Path

INPUT = Path("data/processed/uncertain_needs_manual_fulltext.csv")
OUTPUT = Path("data/processed/ambiguous_review_priority.csv")
REPORT = Path("data/reports/ambiguous_review_priority_report.md")

FIELDS = [
    "priority_bucket",
    "priority_rank",
    "uncertain_id",
    "title",
    "authors",
    "year",
    "venue",
    "source",
    "screen_reason",
    "second_pass_recommendation",
    "confidence",
    "fulltext_access",
    "fulltext_source",
    "landing_page_url",
    "pdf_url",
    "download_status",
    "local_pdf_path",
    "review_action",
    "notes",
]


def priority_for(row: dict) -> tuple[int, str, str]:
    download_status = row.get("download_status", "")
    fulltext_access = row.get("fulltext_access", "")
    pdf_path = row.get("local_pdf_path", "")
    pdf_url = row.get("pdf_url", "")
    landing = row.get("landing_page_url", "")

    if download_status == "downloaded" and pdf_path:
        return 1, "downloaded_pdf", "Read local PDF first"

    if fulltext_access == "open" and pdf_url:
        return 2, "open_pdf_link", "Open direct PDF link and review"

    if fulltext_access == "open" and landing:
        return 3, "open_landing_page", "Open landing page and retrieve accessible full text"

    if fulltext_access == "unknown" and landing:
        return 4, "manual_access_check", "Check publisher/DOI page manually or through institutional access"

    return 5, "unresolved", "Search manually by title/DOI"


def main():
    with INPUT.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    prioritized = []
    for row in rows:
        rank, bucket, action = priority_for(row)
        prioritized.append(
            {
                "priority_bucket": bucket,
                "priority_rank": rank,
                "uncertain_id": row.get("uncertain_id", ""),
                "title": row.get("title", ""),
                "authors": row.get("authors", ""),
                "year": row.get("year", ""),
                "venue": row.get("venue", ""),
                "source": row.get("source", ""),
                "screen_reason": row.get("screen_reason", ""),
                "second_pass_recommendation": row.get("second_pass_recommendation", ""),
                "confidence": row.get("confidence", ""),
                "fulltext_access": row.get("fulltext_access", ""),
                "fulltext_source": row.get("fulltext_source", ""),
                "landing_page_url": row.get("landing_page_url", ""),
                "pdf_url": row.get("pdf_url", ""),
                "download_status": row.get("download_status", ""),
                "local_pdf_path": row.get("local_pdf_path", ""),
                "review_action": action,
                "notes": row.get("notes", ""),
            }
        )

    prioritized.sort(key=lambda row: (
        row["priority_rank"], row["year"], row["title"]))

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(prioritized)

    counts = Counter(row["priority_bucket"] for row in prioritized)
    with REPORT.open("w", encoding="utf-8") as handle:
        handle.write("# Ambiguous Review Priority Report\n\n")
        handle.write(
            f"- Total ambiguous records prioritized: {len(prioritized)}\n")
        for bucket in [
            "downloaded_pdf",
            "open_pdf_link",
            "open_landing_page",
            "manual_access_check",
            "unresolved",
        ]:
            handle.write(f"- {bucket}: {counts.get(bucket, 0)}\n")
        handle.write("\n## Recommended order\n")
        handle.write("1. Read local PDFs already downloaded.\n")
        handle.write("2. Open direct OA PDF links.\n")
        handle.write("3. Open landing pages with OA access.\n")
        handle.write(
            "4. Use institutional/publisher access for the remaining rows.\n")

    print(f"Wrote {OUTPUT}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
