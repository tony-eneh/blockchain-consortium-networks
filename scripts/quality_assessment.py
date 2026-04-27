"""Automated quality / risk-of-bias screening rubric for the 279 included studies.

This is a *screening-stage* rubric: it scores each study on the four PRISMA
protocol dimensions (construct, internal, external, reproducibility validity)
using deterministic signals available without full-text re-parsing
(venue/source type, year, title + abstract keyword evidence).

It is explicitly NOT a substitute for a per-paper full-text rubric pass; it
gives a triage score so the reviewer can prioritize which of the 279 to
deep-read first.

Inputs:
  data/processed/fulltext_screening.csv  (final include list)
  data/processed/master_dedup.csv        (source of abstracts)

Outputs:
  data/processed/quality_assessment.csv
  data/reports/quality_assessment_report.md
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "processed" / "fulltext_screening.csv"
MASTER = ROOT / "data" / "processed" / "master_dedup.csv"
OUT_CSV = ROOT / "data" / "processed" / "quality_assessment.csv"
OUT_MD = ROOT / "data" / "reports" / "quality_assessment_report.md"

# ── Keyword lexicons ────────────────────────────────────────────────────────
EVAL_KW = re.compile(
    r"\b(throughput|latency|tps|benchmark|evaluat\w+|measur\w+|experiment\w*|"
    r"prototyp\w+|implement\w+|simulation|caliper|hyperledger|fabric|besu|"
    r"quorum|corda|ethereum|geth)\b",
    re.I,
)
BASELINE_KW = re.compile(
    r"\b(baseline|compar\w+|state[- ]of[- ]the[- ]art|benchmark\w*|ablation)\b",
    re.I,
)
GENERALIZATION_KW = re.compile(
    r"\b(institution\w*|consorti\w+|inter[- ]?bank|inter[- ]?organi\w+|"
    r"cross[- ]?organi\w+|multi[- ]?part\w+|enterprise|government|healthcare|"
    r"supply[- ]?chain|finance|regulator\w*)\b",
    re.I,
)
REPRO_KW = re.compile(
    r"\b(open[- ]?source|github|gitlab|zenodo|reproduc\w+|artifact|dataset|"
    r"code (?:available|released)|public(?:ly)? available|replication package)\b",
    re.I,
)

PEER_REVIEWED_SOURCES = {"ieee", "wos", "scopus", "acm"}
PREPRINT_SOURCES = {"arxiv"}
INDEX_SOURCES = {"openalex"}  # quality varies; treat as mixed.


def _load_abstracts() -> dict[tuple[str, str], dict]:
    """Map (normalized_title, doi) → master row (for abstracts)."""
    out: dict[tuple[str, str], dict] = {}
    with MASTER.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = (
                (row.get("title") or "").strip().lower(),
                (row.get("doi") or "").strip().lower(),
            )
            out[key] = row
    return out


def _score_construct(text: str) -> tuple[int, str]:
    hits = len(set(m.group(0).lower() for m in EVAL_KW.finditer(text)))
    if hits >= 3:
        return 2, f"strong evaluation vocabulary ({hits} distinct terms)"
    if hits >= 1:
        return 1, f"some evaluation vocabulary ({hits} terms)"
    return 0, "no evaluation vocabulary detected in title/abstract"


def _score_internal(text: str, source: str) -> tuple[int, str]:
    has_baseline = bool(BASELINE_KW.search(text))
    is_peer = source.lower() in PEER_REVIEWED_SOURCES
    if has_baseline and is_peer:
        return 2, "peer-reviewed venue + baseline/comparison signal"
    if has_baseline or is_peer:
        return 1, "peer-reviewed venue OR baseline signal (not both)"
    return 0, "preprint/index source with no comparison signal"


def _score_external(text: str) -> tuple[int, str]:
    hits = len(set(m.group(0).lower() for m in GENERALIZATION_KW.finditer(text)))
    if hits >= 2:
        return 2, f"institutional/cross-org context explicit ({hits} markers)"
    if hits == 1:
        return 1, "single institutional/domain marker"
    return 0, "no institutional/cross-org marker in title/abstract"


def _score_repro(text: str) -> tuple[int, str]:
    if REPRO_KW.search(text):
        return 2, "explicit artifact/reproducibility signal"
    if re.search(r"\b(implement\w+|prototyp\w+|deploy\w+)\b", text, re.I):
        return 1, "implementation mentioned but no public artifact signal"
    return 0, "no implementation or artifact signal"


def main() -> None:
    abstracts = _load_abstracts()

    with SCREEN.open(encoding="utf-8", newline="") as f:
        screen_rows = list(csv.DictReader(f))

    includes = [r for r in screen_rows if r.get("final_decision") == "include"]

    out_rows: list[dict] = []
    score_dist: Counter[int] = Counter()
    tier_dist: Counter[str] = Counter()

    for r in includes:
        title = (r.get("title") or "").strip()
        doi = (r.get("doi") or "").strip().lower()
        master = abstracts.get((title.lower(), doi)) or abstracts.get((title.lower(), ""))
        abstract = (master or {}).get("abstract", "") or ""
        source = (r.get("source") or "").lower()
        text = f"{title}\n{abstract}"

        c, c_note = _score_construct(text)
        i, i_note = _score_internal(text, source)
        e, e_note = _score_external(text)
        p, p_note = _score_repro(text)
        total = c + i + e + p
        if total >= 6:
            tier = "A"
        elif total >= 4:
            tier = "B"
        elif total >= 2:
            tier = "C"
        else:
            tier = "D"

        score_dist[total] += 1
        tier_dist[tier] += 1
        out_rows.append({
            "candidate_id": r.get("candidate_id", ""),
            "title": title,
            "year": r.get("year", ""),
            "venue": r.get("venue", ""),
            "source": source,
            "doi": r.get("doi", ""),
            "url": r.get("url", ""),
            "construct_score": c,
            "construct_note": c_note,
            "internal_score": i,
            "internal_note": i_note,
            "external_score": e,
            "external_note": e_note,
            "reproducibility_score": p,
            "reproducibility_note": p_note,
            "total_score": total,
            "tier": tier,
            "abstract_available": bool(abstract),
        })

    out_rows.sort(key=lambda x: (-x["total_score"], x["title"]))

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    abs_avail = sum(1 for r in out_rows if r["abstract_available"])
    lines = [
        "# Quality Assessment Report (screening-stage rubric)",
        "",
        f"- Inputs: `{SCREEN.relative_to(ROOT).as_posix()}`, "
        f"`{MASTER.relative_to(ROOT).as_posix()}`.",
        f"- Output sheet: `{OUT_CSV.relative_to(ROOT).as_posix()}`.",
        f"- Studies scored: **{len(out_rows)}** (final-decision = include).",
        f"- Abstracts available for scoring: **{abs_avail} / {len(out_rows)}**.",
        "",
        "## Rubric (each dimension 0–2, total 0–8)",
        "1. **Construct validity** — evaluation vocabulary present in title/abstract.",
        "2. **Internal validity** — peer-reviewed venue and/or explicit comparison/baseline signal.",
        "3. **External validity** — institutional/cross-organizational context markers.",
        "4. **Reproducibility** — artifact/code/data signals; implementation language.",
        "",
        "Tiers: A ≥ 6, B 4–5, C 2–3, D 0–1.",
        "",
        "## Tier distribution",
        "| Tier | Studies |",
        "|------|---------|",
    ]
    for tier in ("A", "B", "C", "D"):
        lines.append(f"| {tier} | {tier_dist.get(tier, 0)} |")
    lines += [
        "",
        "## Total-score distribution",
        "| Total | Studies |",
        "|-------|---------|",
    ]
    for s in range(8, -1, -1):
        if score_dist.get(s):
            lines.append(f"| {s} | {score_dist[s]} |")
    lines += [
        "",
        "## Caveat",
        "These scores are **screening-stage triage signals only**, derived from "
        "title + abstract + source. Final per-study quality scoring requires a "
        "full-text rubric pass (Step 7 deep dive) on tier-A/B candidates first.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_CSV.relative_to(ROOT)} ({len(out_rows)} rows)")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    print("Tier dist:", dict(tier_dist))


if __name__ == "__main__":
    main()
