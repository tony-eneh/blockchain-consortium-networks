#!/usr/bin/env python3
"""Second-pass triage for uncertain title/abstract records.

This does not replace full-text review. It reduces manual effort by assigning
uncertain records into:
  - likely_include
  - likely_exclude
  - needs_manual

Output:
  data/processed/uncertain_second_pass.csv
  data/reports/uncertain_second_pass_report.md
"""

import csv
import re
from collections import Counter
from pathlib import Path

INPUT = Path("data/processed/screened.csv")
OUT = Path("data/processed/uncertain_second_pass.csv")
REPORT = Path("data/reports/uncertain_second_pass_report.md")

FIELDS = [
    "uncertain_id",
    "title",
    "authors",
    "year",
    "venue",
    "doi",
    "url",
    "source",
    "screen_reason",
    "second_pass_recommendation",
    "confidence",
    "rationale",
    "manual_final_decision",
    "manual_notes",
]

INSTITUTIONAL_STRONG = [
    r"\bconsortium\b",
    r"\bpermissioned\b",
    r"\bprivate\s+blockchain\b",
    r"\bcross-?chain\b",
    r"\binteroperab",
    r"\binterbank\b",
    r"\bcross-?border\b",
    r"\bhealth(care|\s+records?)\b",
    r"\bmedical\b",
    r"\bgenomic\b",
    r"\btrade\s+finance\b",
    r"\bsupply\s+chain\b",
    r"\bgovernment\b",
    r"\blegislative\b",
    r"\bfederated\s+data\s+exchange\b",
    r"\baudit\b",
]

TECHNICAL_EVIDENCE = [
    r"\bimplement",
    r"\bprototype\b",
    r"\barchitecture\b",
    r"\bframework\b",
    r"\bbenchmark\b",
    r"\bevaluat",
    r"\bexperiment",
    r"\bperformance\b",
    r"\bthroughput\b",
    r"\blatency\b",
    r"\bprototype\b",
    r"\bvalidated?\b",
]

LIKELY_EXCLUDE = [
    r"\bdraft\s+standard\b",
    r"\bstandard\b",
    r"\btermination\s+analysis\b",
    r"\buniversally\s+composable\b",
    r"\bproof\s+of\s+conceptual\b",
    r"\btheorem\b",
    r"\bproof\b",
    r"\bquantum-?secured\s+blockchain\b",
    r"\bdynamic\s+consensus\s+algorithm\b",
    r"\bfederated\s+learning\b",
    r"\benergy\s+storage\b",
    r"\bdigital\s+transactions\b",
    r"\beducation\s+data\b",
    r"\bdocument\s+verification\b",
]

REDEEMING_CONTEXT = [
    r"\bconsortium\b",
    r"\bpermissioned\b",
    r"\bprivate\b",
    r"\bcross-?chain\b",
    r"\binteroperab",
    r"\binstitution",
    r"\bmulti-?party\b",
    r"\borganization\b",
]


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def count_any(text: str, patterns: list[str]) -> int:
    return sum(1 for pattern in patterns if re.search(pattern, text, re.IGNORECASE))


def triage(row: dict) -> tuple[str, str, str]:
    title = row.get("title", "")
    abstract = row.get("abstract", "")
    text = f"{title} {abstract}".strip()

    strong_inst = count_any(text, INSTITUTIONAL_STRONG)
    evidence = count_any(text, TECHNICAL_EVIDENCE)
    negative = count_any(text, LIKELY_EXCLUDE)
    redeeming = count_any(text, REDEEMING_CONTEXT)

    if not abstract.strip():
        if negative >= 1 and redeeming == 0:
            return (
                "likely_exclude",
                "medium",
                "No abstract and title points to standard/theory/generic topic without clear institutional consortium context.",
            )
        if strong_inst >= 1:
            return (
                "needs_manual",
                "medium",
                "No abstract available, but title has potentially relevant institutional or consortium signal.",
            )
        return (
            "likely_exclude",
            "low",
            "No abstract and insufficient institutional/technical detail in title.",
        )

    if strong_inst >= 2 and evidence >= 1 and negative == 0:
        return (
            "likely_include",
            "high",
            "Abstract shows institutional or consortium context plus implementation/evaluation signal.",
        )

    if strong_inst >= 1 and evidence >= 2 and negative == 0:
        return (
            "likely_include",
            "medium",
            "Technical evaluation is present and there is at least one meaningful institutional or interoperability signal.",
        )

    if negative >= 2 and redeeming == 0:
        return (
            "likely_exclude",
            "high",
            "Record appears to focus on theory, standards, or generic blockchain use without the target institutional consortium setting.",
        )

    if negative >= 1 and strong_inst == 0:
        return (
            "likely_exclude",
            "medium",
            "Abstract is dominated by generic or off-scope signals and lacks clear institutional-consortium evidence.",
        )

    if strong_inst == 0 and evidence <= 1:
        return (
            "likely_exclude",
            "medium",
            "Weak institutional context and limited evidence of an implementation-focused consortium study.",
        )

    return (
        "needs_manual",
        "medium",
        "Mixed signals: some relevant blockchain/implementation cues, but institutional consortium relevance is not decisive from title/abstract alone.",
    )


def load_uncertain_rows() -> list[dict]:
    with INPUT.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if row.get("screen_decision") == "UNCERTAIN"]


def main():
    rows = load_uncertain_rows()
    results = []
    counts = Counter()
    confidence_counts = Counter()

    for idx, row in enumerate(rows, start=1):
        recommendation, confidence, rationale = triage(row)
        results.append(
            {
                "uncertain_id": f"UT-{idx:04d}",
                "title": row.get("title", ""),
                "authors": row.get("authors", ""),
                "year": row.get("year", ""),
                "venue": row.get("venue", ""),
                "doi": row.get("doi", ""),
                "url": row.get("url", ""),
                "source": row.get("source", ""),
                "screen_reason": row.get("screen_reason", ""),
                "second_pass_recommendation": recommendation,
                "confidence": confidence,
                "rationale": rationale,
                "manual_final_decision": "",
                "manual_notes": "",
            }
        )
        counts[recommendation] += 1
        confidence_counts[confidence] += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(results)

    with REPORT.open("w", encoding="utf-8") as handle:
        handle.write("# Uncertain Record Second-Pass Triage Report\n\n")
        handle.write(f"- Input uncertain records: {len(rows)}\n")
        handle.write(f"- likely_include: {counts['likely_include']}\n")
        handle.write(f"- likely_exclude: {counts['likely_exclude']}\n")
        handle.write(f"- needs_manual: {counts['needs_manual']}\n\n")
        handle.write("## Confidence distribution\n")
        for key in ["high", "medium", "low"]:
            handle.write(f"- {key}: {confidence_counts[key]}\n")
        handle.write("\n## Usage\n")
        handle.write(
            "- Treat `likely_include` and `likely_exclude` as recommendations, not final full-text decisions.\n")
        handle.write("- Prioritize `needs_manual` first for human review.\n")

    print(f"Processed uncertain rows: {len(rows)}")
    print(f"likely_include={counts['likely_include']}")
    print(f"likely_exclude={counts['likely_exclude']}")
    print(f"needs_manual={counts['needs_manual']}")
    print(f"Wrote {OUT}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
