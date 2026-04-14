#!/usr/bin/env python3
"""Title/abstract screening based on the PRISMA protocol inclusion/exclusion criteria.

Applies rule-based keyword screening to classify each record as:
  - INCLUDE: likely relevant based on title+abstract signals
  - EXCLUDE: clearly out of scope, with coded exclusion reason
  - UNCERTAIN: needs manual review (borderline or missing abstract)

Usage:
    py scripts/screen_title_abstract.py

Reads:  data/processed/master_dedup.csv
Writes: data/processed/screened.csv
        data/reports/screening_report.md
"""

import csv
import re
from collections import Counter
from pathlib import Path

INPUT = Path("data/processed/master_dedup.csv")
OUTPUT = Path("data/processed/screened.csv")
REPORT = Path("data/reports/screening_report.md")

# ── Inclusion signals ──
# Must have at least ONE technology term AND ONE institutional/consortium term
# AND ONE strategy/evaluation term to be considered relevant.

TECH_TERMS = [
    r"\bconsortium\s+blockchain\b",
    r"\bpermissioned\s+(blockchain|ledger|dlt)\b",
    r"\benterprise\s+blockchain\b",
    r"\bhyperledger\s+fabric\b",
    r"\bhyperledger\s+besu\b",
    r"\bcorda\b",
    r"\bquorum\b",
    r"\bdistributed\s+ledger\b",
    r"\bprivate\s+blockchain\b",
    r"\bfederated\s+(blockchain|ledger)\b",
]

INSTITUTIONAL_TERMS = [
    r"\bconsortium\b",
    r"\binter-?institutional\b",
    r"\binter-?organi[sz]ational\b",
    r"\bcross-?organi[sz]ational\b",
    r"\binter-?bank\b",
    r"\binterbank\b",
    r"\bmulti-?party\b",
    r"\bmulti-?organi[sz]ation\b",
    r"\bB2B\b",
    r"\bsupply\s+chain\b",
    r"\btrade\s+finance\b",
    r"\bhealthcare\b",
    r"\bgovernment\b",
    r"\bregulat(or|ory|ion|ed)\b",
    r"\bcross-?border\b",
    r"\bidentity\b",
    r"\bdigital\s+asset\b",
]

STRATEGY_TERMS = [
    r"\bconsensus\b",
    r"\bgovernance\b",
    r"\bprivacy\b",
    r"\bconfidential(ity)?\b",
    r"\binteroperability\b",
    r"\bcross-?chain\b",
    r"\bsmart\s+contract\b",
    r"\baccess\s+control\b",
    r"\bchann?el\b",
    r"\borderering\s+service\b",
    r"\bendorsement\b",
    r"\bpbft\b",
    r"\braft\b",
    r"\bbft\b",
    r"\bzero[\s-]?knowledge\b",
    r"\bbridge\b",
    r"\brelay\b",
    r"\boracle\b",
]

EVIDENCE_TERMS = [
    r"\bimplement(ation|ed|ing)?\b",
    r"\bprototype\b",
    r"\bbenchmark(ing|ed)?\b",
    r"\bevaluat(e|ion|ed|ing)\b",
    r"\bexperiment(al|s|ation)?\b",
    r"\bthroughput\b",
    r"\blatency\b",
    r"\bperformance\b",
    r"\btps\b",
    r"\btransactions?\s+per\s+second\b",
    r"\bdeployment\b",
    r"\btestbed\b",
]

# ── Exclusion signals ──
# Strong signals that a paper is out of scope.

EXCLUDE_CRYPTO_MARKET = [
    r"\bcryptocurrency\s+(price|market|trading|predict)\b",
    r"\bbitcoin\s+(price|market|trading)\b",
    r"\btoken\s+(price|valuation|market)\b",
    r"\bNFT\s+market(place)?\b",
    r"\bdefi\s+(yield|farming|liquidity|token)\b",
    r"\btrading\s+strateg(y|ies)\b",
    r"\bprice\s+predict(ion|ing)\b",
    r"\bstock\s+market\b",
    r"\bcrypto\s+exchange\b",
]

EXCLUDE_PURE_PUBLIC = [
    r"\bpublic\s+blockchain\s+(only|solely)\b",
    r"\bmining\s+(pool|reward|algorithm)\b",
    r"\bproof[\s-]of[\s-]work\s+(mining|energy)\b",
    r"\bbitcoin\s+mining\b",
]

EXCLUDE_NON_TECHNICAL = [
    r"\blegal\s+framework\b(?!.*implement)",
    r"\bpolicy\s+analysis\b(?!.*techni)",
    r"\bsurvey\s+of\s+(public\s+)?opinion\b",
    r"\bsocial\s+impact\s+assessment\b",
    r"\badoption\s+(barriers?|factors?|determinants?)\b(?!.*techni)",
]

EXCLUDE_SINGLE_ORG = [
    r"\bsingle[\s-]organi[sz]ation\b",
    r"\binternal\s+(ledger|record|system)\b(?!.*inter)",
]


def has_match(text: str, patterns: list[str]) -> bool:
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def count_matches(text: str, patterns: list[str]) -> int:
    return sum(1 for pat in patterns if re.search(pat, text, re.IGNORECASE))


def screen_record(title: str, abstract: str) -> tuple[str, str]:
    """Return (decision, reason) for a single record."""
    text = f"{title} {abstract}".strip()

    if not text or len(text) < 20:
        return "UNCERTAIN", "no_title_or_abstract"

    # ── Exclusion checks first ──
    if has_match(text, EXCLUDE_CRYPTO_MARKET):
        return "EXCLUDE", "crypto_market_study"

    if has_match(text, EXCLUDE_PURE_PUBLIC) and not has_match(text, TECH_TERMS):
        return "EXCLUDE", "pure_public_blockchain"

    if has_match(text, EXCLUDE_NON_TECHNICAL) and not has_match(text, EVIDENCE_TERMS):
        return "EXCLUDE", "non_technical_commentary"

    if has_match(text, EXCLUDE_SINGLE_ORG) and not has_match(text, INSTITUTIONAL_TERMS):
        return "EXCLUDE", "single_organization"

    # ── Inclusion scoring ──
    has_tech = has_match(text, TECH_TERMS)
    has_inst = has_match(text, INSTITUTIONAL_TERMS)
    has_strat = has_match(text, STRATEGY_TERMS)
    has_evidence = has_match(text, EVIDENCE_TERMS)

    # No abstract — can only screen by title
    if not abstract.strip():
        if has_tech and (has_inst or has_strat):
            return "UNCERTAIN", "no_abstract_but_title_relevant"
        elif has_tech:
            return "UNCERTAIN", "no_abstract_title_partial"
        else:
            return "EXCLUDE", "no_abstract_title_irrelevant"

    # Strong include: technology + institutional + (strategy OR evidence)
    if has_tech and has_inst and (has_strat or has_evidence):
        return "INCLUDE", "full_criteria_match"

    # Medium include: technology + strategy + evidence (institutional implied)
    if has_tech and has_strat and has_evidence:
        return "INCLUDE", "tech_strategy_evidence"

    # Weak include: technology + at least 2 of (institutional, strategy, evidence)
    score = sum([has_inst, has_strat, has_evidence])
    if has_tech and score >= 2:
        return "INCLUDE", "tech_plus_two_dimensions"

    # Borderline: has technology term but limited other signals
    if has_tech and score == 1:
        return "UNCERTAIN", "tech_with_weak_signal"

    # Has institutional + strategy but no specific blockchain tech term
    if has_inst and has_strat and has_evidence:
        # Check for generic blockchain mention
        if re.search(r"\bblockchain\b", text, re.IGNORECASE):
            return "UNCERTAIN", "generic_blockchain_institutional"
        return "EXCLUDE", "no_blockchain_technology"

    # Catch-all: not enough signals
    if has_tech:
        return "UNCERTAIN", "tech_only_no_context"

    return "EXCLUDE", "insufficient_relevance"


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    with INPUT.open("r", encoding="utf-8") as f:
        records = list(csv.DictReader(f))

    results = []
    decision_counts = Counter()
    reason_counts = Counter()

    for row in records:
        title = row.get("title", "")
        abstract = row.get("abstract", "")
        decision, reason = screen_record(title, abstract)
        row["screen_decision"] = decision
        row["screen_reason"] = reason
        results.append(row)
        decision_counts[decision] += 1
        reason_counts[reason] += 1

    # Write screened CSV
    fields = list(results[0].keys())
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    # Write report
    include = decision_counts["INCLUDE"]
    exclude = decision_counts["EXCLUDE"]
    uncertain = decision_counts["UNCERTAIN"]
    total = len(results)

    with REPORT.open("w", encoding="utf-8") as f:
        f.write("# Title/Abstract Screening Report\n\n")
        f.write(f"**Date:** 2026-04-14\n")
        f.write(f"**Input:** {total} deduplicated records\n\n")
        f.write("## Decision Summary\n\n")
        f.write(f"| Decision | Count | % |\n")
        f.write(f"|----------|------:|---:|\n")
        f.write(f"| INCLUDE | {include} | {include*100/total:.1f}% |\n")
        f.write(f"| EXCLUDE | {exclude} | {exclude*100/total:.1f}% |\n")
        f.write(f"| UNCERTAIN | {uncertain} | {uncertain*100/total:.1f}% |\n")
        f.write(f"| **Total** | **{total}** | |\n")
        f.write(f"\n## PRISMA Flow Numbers\n\n")
        f.write(f"- Records after dedup: {total}\n")
        f.write(f"- Records screened (title/abstract): {total}\n")
        f.write(f"- Excluded at title/abstract: {exclude}\n")
        f.write(f"- Uncertain (manual review needed): {uncertain}\n")
        f.write(f"- Passed screening: {include}\n")
        f.write(f"- **Candidates for full-text review: {include + uncertain}**\n")
        f.write(f"\n## Exclusion Reasons\n\n")
        f.write(f"| Reason | Count |\n")
        f.write(f"|--------|------:|\n")
        for reason, count in reason_counts.most_common():
            f.write(f"| {reason} | {count} |\n")

    print(f"Screening complete:")
    print(f"  INCLUDE:   {include}")
    print(f"  EXCLUDE:   {exclude}")
    print(f"  UNCERTAIN: {uncertain}")
    print(f"  Total:     {total}")
    print(f"\nWrote {OUTPUT}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
