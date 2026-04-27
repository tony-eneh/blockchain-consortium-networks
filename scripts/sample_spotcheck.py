"""Stratified spot-check sample for the Week-9 author-level audit of agent
full-text decisions.

Strata:
  - includes by quality tier (A / B / C / D) → up to 5 each → 20 total.
  - excludes by exclusion-reason code (top buckets) → 4 each → 20 total.

Output:
  data/processed/spotcheck_sample.csv
  data/reports/spotcheck_sample_report.md

Determinism: fixed random seed = 20260428.
"""

from __future__ import annotations

import csv
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "processed" / "fulltext_screening.csv"
QUALITY = ROOT / "data" / "processed" / "quality_assessment.csv"
OUT_CSV = ROOT / "data" / "processed" / "spotcheck_sample.csv"
OUT_MD = ROOT / "data" / "reports" / "spotcheck_sample_report.md"

SEED = 20260428
PER_INCLUDE_TIER = 5  # A/B/C/D
PER_EXCLUDE_REASON = 4
TOP_EXCL_REASONS = 5

FIELDS = [
    "stratum",
    "candidate_id",
    "title",
    "year",
    "venue",
    "source",
    "doi",
    "url",
    "agent_decision",
    "agent_reason_code",
    "agent_reason_detail",
    "tier",
    "total_score",
    "human_decision",     # blank for reviewer
    "human_notes",        # blank for reviewer
]


def main() -> None:
    rng = random.Random(SEED)

    with SCREEN.open(encoding="utf-8", newline="") as f:
        screen_rows = {r["candidate_id"]: r for r in csv.DictReader(f)}

    with QUALITY.open(encoding="utf-8", newline="") as f:
        quality_rows = {r["candidate_id"]: r for r in csv.DictReader(f)}

    # Include strata by tier
    include_by_tier: dict[str, list[str]] = defaultdict(list)
    for cid, qr in quality_rows.items():
        include_by_tier[qr["tier"]].append(cid)

    # Exclude strata by reason
    exclude_by_reason: dict[str, list[str]] = defaultdict(list)
    for cid, sr in screen_rows.items():
        if sr.get("final_decision") == "exclude":
            code = sr.get("fulltext_exclusion_reason_code") or "unspecified"
            exclude_by_reason[code].append(cid)

    top_reasons = sorted(
        exclude_by_reason.items(), key=lambda kv: -len(kv[1])
    )[:TOP_EXCL_REASONS]

    sampled: list[dict] = []

    for tier in ("A", "B", "C", "D"):
        pool = include_by_tier.get(tier, [])
        rng.shuffle(pool)
        picks = pool[:PER_INCLUDE_TIER]
        for cid in picks:
            sr = screen_rows[cid]
            qr = quality_rows[cid]
            sampled.append({
                "stratum": f"include_tier_{tier}",
                "candidate_id": cid,
                "title": sr.get("title", ""),
                "year": sr.get("year", ""),
                "venue": sr.get("venue", ""),
                "source": sr.get("source", ""),
                "doi": sr.get("doi", ""),
                "url": sr.get("url", ""),
                "agent_decision": "include",
                "agent_reason_code": "",
                "agent_reason_detail": "",
                "tier": qr["tier"],
                "total_score": qr["total_score"],
                "human_decision": "",
                "human_notes": "",
            })

    for reason, cids in top_reasons:
        rng.shuffle(cids)
        picks = cids[:PER_EXCLUDE_REASON]
        for cid in picks:
            sr = screen_rows[cid]
            sampled.append({
                "stratum": f"exclude_{reason}",
                "candidate_id": cid,
                "title": sr.get("title", ""),
                "year": sr.get("year", ""),
                "venue": sr.get("venue", ""),
                "source": sr.get("source", ""),
                "doi": sr.get("doi", ""),
                "url": sr.get("url", ""),
                "agent_decision": "exclude",
                "agent_reason_code": reason,
                "agent_reason_detail": sr.get("fulltext_exclusion_reason_detail", ""),
                "tier": "",
                "total_score": "",
                "human_decision": "",
                "human_notes": "",
            })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(sampled)

    inc_n = sum(1 for r in sampled if r["agent_decision"] == "include")
    exc_n = sum(1 for r in sampled if r["agent_decision"] == "exclude")

    lines = [
        "# Spot-Check Sample (Week 9 author audit)",
        "",
        f"- Output: `{OUT_CSV.relative_to(ROOT).as_posix()}`.",
        f"- Random seed: `{SEED}` (deterministic).",
        f"- Total sampled rows: **{len(sampled)}** "
        f"(includes: {inc_n}, excludes: {exc_n}).",
        "",
        "## Include strata",
        "| Tier | Population | Sampled |",
        "|------|------------|---------|",
    ]
    for tier in ("A", "B", "C", "D"):
        pop = len(include_by_tier.get(tier, []))
        sampled_n = sum(1 for r in sampled if r["stratum"] == f"include_tier_{tier}")
        lines.append(f"| {tier} | {pop} | {sampled_n} |")
    lines += [
        "",
        "## Exclude strata (top reasons)",
        "| Reason code | Population | Sampled |",
        "|-------------|------------|---------|",
    ]
    for reason, cids in top_reasons:
        sampled_n = sum(1 for r in sampled if r["stratum"] == f"exclude_{reason}")
        lines.append(f"| `{reason}` | {len(cids)} | {sampled_n} |")
    lines += [
        "",
        "## Reviewer instructions",
        "- Open `data/processed/spotcheck_sample.csv`.",
        "- Fill `human_decision` ∈ {`include`, `exclude`, `unsure`} and add `human_notes`.",
        "- Compute agreement rate = matches / total once complete.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_CSV.relative_to(ROOT)} ({len(sampled)} rows)")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
