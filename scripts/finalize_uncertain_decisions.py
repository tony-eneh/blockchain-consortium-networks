#!/usr/bin/env python3
"""Finalize agent fulltext decisions for the 292 uncertain rows.

Rules applied per uncertain row (title-normalised join across artifacts):

- Promoted to INCLUDE:
    * Listed in `uncertain_likely_include.csv` (second-pass triage).
    * Listed in `accessible_fulltext_review.csv` with agent_fulltext_decision == include.
- Marked EXCLUDE:
    * Listed in `uncertain_likely_exclude.csv` (second-pass triage).
    * Listed in `accessible_fulltext_review.csv` with agent_fulltext_decision == exclude.
    * Listed in `accessible_fulltext_review.csv` with agent_fulltext_decision == needs_human_check
      (conservatively excluded; agent could not satisfy inclusion criteria from the available text).
    * Ambiguous priority bucket == manual_access_check (paywalled / no full-text reachable).
- Anything else: left as fulltext_decision = "" (should not happen given the partition).

Outputs:
  data/processed/fulltext_screening.csv (in place update)
  data/reports/uncertain_finalization_report.md
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULLTEXT_SCREENING = ROOT / "data" / "processed" / "fulltext_screening.csv"
LIKELY_INCLUDE = ROOT / "data" / "processed" / "uncertain_likely_include.csv"
LIKELY_EXCLUDE = ROOT / "data" / "processed" / "uncertain_likely_exclude.csv"
ACCESSIBLE_REVIEW = ROOT / "data" / "processed" / "accessible_fulltext_review.csv"
PRIORITY = ROOT / "data" / "processed" / "ambiguous_review_priority.csv"
REPORT = ROOT / "data" / "reports" / "uncertain_finalization_report.md"


def norm_title(title: str) -> str:
    return re.sub(r"\s+", " ", (title or "").strip().lower())


def load_titles(path: Path, key: str = "title") -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {norm_title(row[key]) for row in csv.DictReader(handle) if row.get(key)}


def load_accessible() -> dict[str, dict]:
    with ACCESSIBLE_REVIEW.open("r", encoding="utf-8", newline="") as handle:
        return {norm_title(row["title"]): row for row in csv.DictReader(handle)}


def load_paywalled_titles() -> set[str]:
    with PRIORITY.open("r", encoding="utf-8", newline="") as handle:
        return {
            norm_title(row["title"])
            for row in csv.DictReader(handle)
            if row.get("priority_bucket") == "manual_access_check"
        }


def main() -> None:
    likely_include = load_titles(LIKELY_INCLUDE)
    likely_exclude = load_titles(LIKELY_EXCLUDE)
    accessible = load_accessible()
    paywalled = load_paywalled_titles()

    with FULLTEXT_SCREENING.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = list(reader.fieldnames or [])

    rule_counts: Counter[str] = Counter()
    decision_counts: Counter[str] = Counter()
    untouched_uncertain: list[str] = []

    for row in rows:
        if row.get("title_abstract_decision") != "UNCERTAIN":
            continue
        key = norm_title(row.get("title", ""))
        decision = ""
        reason_code = ""
        rationale = ""
        rule = ""

        access_row = accessible.get(key)
        if access_row:
            agent_decision = access_row["agent_fulltext_decision"]
            if agent_decision == "include":
                decision, rule = "include", "accessible_review_include"
                reason_code = access_row.get("agent_reason_code", "")
                rationale = (
                    f"Accessible full-text agent review ({access_row.get('agent_confidence','')}): "
                    f"{access_row.get('agent_rationale','')}"
                )
            elif agent_decision == "exclude":
                decision, rule = "exclude", "accessible_review_exclude"
                reason_code = access_row.get("agent_reason_code", "")
                rationale = (
                    f"Accessible full-text agent review ({access_row.get('agent_confidence','')}): "
                    f"{access_row.get('agent_rationale','')}"
                )
            else:  # needs_human_check -> conservative exclude
                decision, rule = "exclude", "accessible_review_needs_human_to_exclude"
                reason_code = "agent_uncertain_full_text"
                rationale = (
                    "Agent reviewed the accessible full text but could not confirm inclusion criteria; "
                    "conservatively excluded pending future human re-screen."
                )
        elif key in likely_include:
            decision, rule = "include", "triage_likely_include_promoted"
            reason_code = ""
            rationale = (
                "Promoted to include based on second-pass uncertain triage "
                "(strong title/abstract signal; full text not retrieved by agent)."
            )
        elif key in likely_exclude:
            decision, rule = "exclude", "triage_likely_exclude"
            reason_code = "second_pass_likely_exclude"
            rationale = (
                "Excluded based on second-pass uncertain triage signals "
                "(no institutional/consortium framing or implementation evidence)."
            )
        elif key in paywalled:
            decision, rule = "exclude", "no_full_text_access"
            reason_code = "no_full_text_access"
            rationale = (
                "Ambiguous record with no open full-text access; excluded for the SLR until full text is procured."
            )
        else:
            untouched_uncertain.append(row.get("candidate_id", ""))
            continue

        row["fulltext_status"] = "agent-finalised"
        row["fulltext_decision"] = decision
        row["fulltext_exclusion_reason_code"] = reason_code if decision == "exclude" else ""
        row["fulltext_exclusion_reason_detail"] = rationale
        row["reviewer_1"] = row.get("reviewer_1") or "agent-fulltext-finalisation"
        row["conflict_status"] = "pending-author-check"
        row["final_decision"] = decision
        row["notes"] = (row.get("notes") + " | " if row.get("notes") else "") + f"finalised:{rule}"

        rule_counts[rule] += 1
        decision_counts[decision] += 1

    with FULLTEXT_SCREENING.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    total_uncertain = sum(1 for r in rows if r.get("title_abstract_decision") == "UNCERTAIN")
    total_include = sum(
        1 for r in rows
        if r.get("title_abstract_decision") == "INCLUDE" or r.get("fulltext_decision") == "include"
    )
    fulltext_include = sum(1 for r in rows if r.get("fulltext_decision") == "include")
    fulltext_exclude = sum(1 for r in rows if r.get("fulltext_decision") == "exclude")
    fulltext_pending = sum(
        1 for r in rows
        if r.get("title_abstract_decision") == "INCLUDE" and not r.get("fulltext_decision")
    )

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT.open("w", encoding="utf-8") as handle:
        handle.write("# Uncertain Decisions Finalisation Report\n\n")
        handle.write(f"- Total uncertain rows processed: {total_uncertain}\n")
        handle.write(f"- Untouched uncertain rows (should be 0): {len(untouched_uncertain)}\n\n")
        handle.write("## Rule application counts\n")
        for rule, count in sorted(rule_counts.items(), key=lambda kv: -kv[1]):
            handle.write(f"- {rule}: {count}\n")
        handle.write("\n## Resulting fulltext decisions for uncertain rows\n")
        for decision, count in sorted(decision_counts.items(), key=lambda kv: -kv[1]):
            handle.write(f"- {decision}: {count}\n")
        handle.write("\n## Updated PRISMA-style screening snapshot\n")
        handle.write(f"- Title/abstract INCLUDE: 571\n")
        handle.write(f"- Title/abstract UNCERTAIN finalised: {total_uncertain}\n")
        handle.write(f"- Full-text agent INCLUDE (uncertain queue): {fulltext_include}\n")
        handle.write(f"- Full-text agent EXCLUDE (uncertain queue): {fulltext_exclude}\n")
        handle.write(f"- Title/abstract INCLUDE still pending full-text screening: {fulltext_pending}\n")
        if untouched_uncertain:
            handle.write("\n## Untouched uncertain ids (investigate)\n")
            for cid in untouched_uncertain:
                handle.write(f"- {cid}\n")

    print(f"Uncertain rows processed: {total_uncertain}")
    print(f"Untouched uncertain: {len(untouched_uncertain)}")
    print(f"Rule counts: {dict(rule_counts)}")
    print(f"Decision counts: {dict(decision_counts)}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
