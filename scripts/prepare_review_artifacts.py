#!/usr/bin/env python3
"""Prepare next-phase review artifacts from screened records.

Generates:
  - data/processed/fulltext_screening.csv
  - data/processed/data_extraction.csv
  - data/reports/review_artifact_report.md

Candidates are all records currently marked INCLUDE or UNCERTAIN during
first-pass title/abstract screening.
"""

import csv
from pathlib import Path

INPUT = Path("data/processed/screened.csv")
FULLTEXT_OUT = Path("data/processed/fulltext_screening.csv")
EXTRACTION_OUT = Path("data/processed/data_extraction.csv")
UNCERTAIN_OUT = Path("data/processed/uncertain_title_abstract.csv")
REPORT_OUT = Path("data/reports/review_artifact_report.md")

FULLTEXT_FIELDS = [
    "candidate_id",
    "title",
    "authors",
    "year",
    "venue",
    "doi",
    "url",
    "source",
    "source_set",
    "title_abstract_decision",
    "title_abstract_reason",
    "fulltext_status",
    "fulltext_decision",
    "fulltext_exclusion_reason_code",
    "fulltext_exclusion_reason_detail",
    "reviewer_1",
    "reviewer_2",
    "conflict_status",
    "final_decision",
    "pdf_collected",
    "pdf_path_or_link",
    "notes",
]

EXTRACTION_FIELDS = [
    "study_id",
    "title",
    "authors",
    "year",
    "venue",
    "doi",
    "url",
    "source",
    "domain",
    "institutional_setting",
    "platform_stack",
    "network_model",
    "node_roles",
    "consensus_strategy",
    "finality_model",
    "governance_model",
    "access_control_model",
    "privacy_mechanism",
    "interoperability_strategy",
    "smart_contract_support",
    "workload_description",
    "evaluation_setup",
    "metrics_reported",
    "throughput",
    "latency",
    "fault_tolerance",
    "privacy_overhead",
    "operational_complexity_notes",
    "artifact_code_available",
    "artifact_data_available",
    "artifact_config_available",
    "reproducibility_notes",
    "quality_construct_validity",
    "quality_internal_validity",
    "quality_external_validity",
    "quality_reproducibility",
    "review_notes",
]

FULLTEXT_REASON_CODES = [
    "not_institutional_setting",
    "no_implementation_detail",
    "no_quantitative_or_reproducible_evidence",
    "single_organization_only",
    "policy_or_commentary_only",
    "crypto_market_focus",
    "duplicate_or_unretrievable_full_text",
    "other",
]


def load_candidates():
    with INPUT.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [
        row for row in rows
        if row.get("screen_decision") in {"INCLUDE", "UNCERTAIN"}
    ]


def load_uncertain():
    with INPUT.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [
        row for row in rows
        if row.get("screen_decision") == "UNCERTAIN"
    ]


def write_fulltext(candidates):
    FULLTEXT_OUT.parent.mkdir(parents=True, exist_ok=True)
    with FULLTEXT_OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FULLTEXT_FIELDS)
        writer.writeheader()
        for index, row in enumerate(candidates, start=1):
            writer.writerow(
                {
                    "candidate_id": f"FT-{index:04d}",
                    "title": row.get("title", ""),
                    "authors": row.get("authors", ""),
                    "year": row.get("year", ""),
                    "venue": row.get("venue", ""),
                    "doi": row.get("doi", ""),
                    "url": row.get("url", ""),
                    "source": row.get("source", ""),
                    "source_set": row.get("source_set", ""),
                    "title_abstract_decision": row.get("screen_decision", ""),
                    "title_abstract_reason": row.get("screen_reason", ""),
                    "fulltext_status": "pending",
                    "fulltext_decision": "",
                    "fulltext_exclusion_reason_code": "",
                    "fulltext_exclusion_reason_detail": "",
                    "reviewer_1": "",
                    "reviewer_2": "",
                    "conflict_status": "",
                    "final_decision": "",
                    "pdf_collected": "no",
                    "pdf_path_or_link": "",
                    "notes": "",
                }
            )


def write_extraction(candidates):
    with EXTRACTION_OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXTRACTION_FIELDS)
        writer.writeheader()
        for index, row in enumerate(candidates, start=1):
            writer.writerow(
                {
                    "study_id": f"ST-{index:04d}",
                    "title": row.get("title", ""),
                    "authors": row.get("authors", ""),
                    "year": row.get("year", ""),
                    "venue": row.get("venue", ""),
                    "doi": row.get("doi", ""),
                    "url": row.get("url", ""),
                    "source": row.get("source", ""),
                }
            )


def write_uncertain(uncertain_rows):
    fields = [
        "uncertain_id",
        "title",
        "authors",
        "year",
        "venue",
        "doi",
        "url",
        "source",
        "source_set",
        "screen_reason",
        "manual_review_status",
        "manual_review_decision",
        "manual_review_notes",
    ]
    with UNCERTAIN_OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for index, row in enumerate(uncertain_rows, start=1):
            writer.writerow(
                {
                    "uncertain_id": f"UT-{index:04d}",
                    "title": row.get("title", ""),
                    "authors": row.get("authors", ""),
                    "year": row.get("year", ""),
                    "venue": row.get("venue", ""),
                    "doi": row.get("doi", ""),
                    "url": row.get("url", ""),
                    "source": row.get("source", ""),
                    "source_set": row.get("source_set", ""),
                    "screen_reason": row.get("screen_reason", ""),
                    "manual_review_status": "pending",
                    "manual_review_decision": "",
                    "manual_review_notes": "",
                }
            )


def write_report(candidates, uncertain_rows):
    include_count = sum(1 for row in candidates if row.get(
        "screen_decision") == "INCLUDE")
    uncertain_count = sum(1 for row in candidates if row.get(
        "screen_decision") == "UNCERTAIN")
    with REPORT_OUT.open("w", encoding="utf-8") as handle:
        handle.write("# Review Artifact Preparation Report\n\n")
        handle.write(
            f"- Input screened records considered for next phase: {len(candidates)}\n")
        handle.write(f"- Candidates from `INCLUDE`: {include_count}\n")
        handle.write(f"- Candidates from `UNCERTAIN`: {uncertain_count}\n")
        handle.write(
            f"- Generated full-text screening sheet: `{FULLTEXT_OUT.as_posix()}`\n")
        handle.write(
            f"- Generated data extraction sheet: `{EXTRACTION_OUT.as_posix()}`\n\n")
        handle.write(
            f"- Generated uncertain-only review sheet: `{UNCERTAIN_OUT.as_posix()}`\n\n")
        handle.write("## Full-text exclusion reason codes\n")
        for code in FULLTEXT_REASON_CODES:
            handle.write(f"- {code}\n")

        handle.write("\n## Uncertain-only review sheet\n")
        handle.write(
            f"- Rows requiring manual adjudication: {len(uncertain_rows)}\n")
        handle.write("- `manual_review_status`: pending / reviewed\n")
        handle.write("- `manual_review_decision`: include / exclude\n")


def main():
    candidates = load_candidates()
    uncertain_rows = load_uncertain()
    write_fulltext(candidates)
    write_extraction(candidates)
    write_uncertain(uncertain_rows)
    write_report(candidates, uncertain_rows)
    print(f"Candidates prepared: {len(candidates)}")
    print(f"Uncertain-only rows prepared: {len(uncertain_rows)}")
    print(f"Wrote {FULLTEXT_OUT}")
    print(f"Wrote {EXTRACTION_OUT}")
    print(f"Wrote {UNCERTAIN_OUT}")
    print(f"Wrote {REPORT_OUT}")


if __name__ == "__main__":
    main()
