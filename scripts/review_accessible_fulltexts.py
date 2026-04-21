#!/usr/bin/env python3
"""Agent full-text review for accessible ambiguous papers.

Targets the accessible ambiguous queue:
- downloaded_pdf
- open_pdf_link
- open_landing_page

Outputs:
  data/processed/accessible_fulltext_review.csv
  data/reports/accessible_fulltext_review_report.md
  updates data/processed/fulltext_screening.csv for matched rows

This is an agent-reviewed decision aid, not a replacement for final author review.
"""

from __future__ import annotations

import csv
import io
import re
from collections import Counter
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from pypdf.errors import EmptyFileError, PdfReadError

PRIORITY_INPUT = Path("data/processed/ambiguous_review_priority.csv")
FULLTEXT_SCREENING = Path("data/processed/fulltext_screening.csv")
OUTPUT = Path("data/processed/accessible_fulltext_review.csv")
REPORT = Path("data/reports/accessible_fulltext_review_report.md")

TARGET_BUCKETS = {"downloaded_pdf", "open_pdf_link", "open_landing_page"}
USER_AGENT = "BCN-SLR-Agent-Fulltext-Review/1.0"
TIMEOUT = 30

OUTPUT_FIELDS = [
    "uncertain_id",
    "title",
    "year",
    "venue",
    "priority_bucket",
    "text_source",
    "text_available",
    "text_length",
    "agent_fulltext_decision",
    "agent_reason_code",
    "agent_confidence",
    "agent_rationale",
    "landing_page_url",
    "pdf_url",
    "local_pdf_path",
]

INSTITUTIONAL_TERMS = [
    r"\bconsortium\b",
    r"\bpermissioned\b",
    r"\binter-?organizational\b",
    r"\bcross-?organizational\b",
    r"\binterbank\b",
    r"\bcross-?border\b",
    r"\bmulti-?party\b",
    r"\bfederated\b",
    r"\bhealthcare\b",
    r"\bmedical\b",
    r"\bgenomic\b",
    r"\bsupply\s+chain\b",
    r"\btrade\s+finance\b",
    r"\bsmart\s+cities\b",
    r"\bgovernment\b",
    r"\blegislative\b",
    r"\be-?commerce\b",
    r"\bagricultural\b",
    r"\bdata\s+sharing\b",
]

IMPLEMENTATION_TERMS = [
    r"\bprototype\b",
    r"\bimplementation\b",
    r"\bimplemented\b",
    r"\bsystem\b",
    r"\barchitecture\b",
    r"\bframework\b",
    r"\bsmart\s+contract\b",
    r"\bhyperledger\b",
    r"\bfabric\b",
    r"\bquorum\b",
    r"\bbesu\b",
    r"\bcorda\b",
    r"\bdeployed\b",
    r"\bgateway\b",
    r"\bcontract\b",
]

EVIDENCE_TERMS = [
    r"\bevaluation\b",
    r"\bexperiment\b",
    r"\bbenchmark\b",
    r"\bresults\b",
    r"\bthroughput\b",
    r"\blatency\b",
    r"\bperformance\b",
    r"\bcase\s+study\b",
    r"\bsimulation\b",
    r"\btestbed\b",
    r"\bmetrics\b",
    r"\bcompar",
]

EXCLUDE_TERMS = {
    "survey_or_review": [
        r"\bsurvey\b",
        r"\breview\b",
        r"\bpractical\s+guide\b",
        r"\bliterature\s+review\b",
    ],
    "consumer_or_market_focus": [
        r"\bconsumer\b",
        r"\bvaluation\b",
        r"\bmarket\b",
        r"\bfood\s+security\b",
        r"\bcbdc\b",
    ],
    "theory_or_standard_focus": [
        r"\bstandardization\b",
        r"\bdraft\s+standard\b",
        r"\btermination\s+analysis\b",
        r"\btheorem\b",
        r"\bproof\b",
        r"\buniversally\s+composable\b",
    ],
    "single_domain_without_institutional_workflow": [
        r"\banomaly\s+detection\b",
        r"\bcyber\s+security\b",
        r"\binformation\s+centric\s+network\b",
        r"\bfederated\s+learning\b",
        r"\bhadoop\b",
    ],
}


def norm_title(value: str) -> str:
    return re.sub(r"\W+", "", (value or "")).lower()


def count_matches(text: str, patterns: list[str]) -> int:
    return sum(1 for pattern in patterns if re.search(pattern, text, re.IGNORECASE))


def fetch_url(url: str) -> Optional[requests.Response]:
    try:
        response = requests.get(
            url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT, allow_redirects=True)
        response.raise_for_status()
        return response
    except requests.RequestException:
        return None


def extract_pdf_text_bytes(data: bytes) -> str:
    if not data:
        return ""
    text_chunks = []
    try:
        reader = PdfReader(io.BytesIO(data))
    except (EmptyFileError, PdfReadError, ValueError, OSError):
        return ""
    for page in reader.pages[:25]:
        extracted = page.extract_text() or ""
        if extracted:
            text_chunks.append(extracted)
    return "\n".join(text_chunks)


def extract_pdf_text_path(path: Path) -> str:
    if not path.exists() or path.stat().st_size == 0:
        return ""
    text_chunks = []
    try:
        reader = PdfReader(str(path))
    except (EmptyFileError, PdfReadError, ValueError, OSError):
        return ""
    for page in reader.pages[:25]:
        extracted = page.extract_text() or ""
        if extracted:
            text_chunks.append(extracted)
    return "\n".join(text_chunks)


def html_to_text(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text)


def get_text_for_row(row: dict) -> tuple[str, str]:
    local_pdf = row.get("local_pdf_path", "")
    pdf_url = row.get("pdf_url", "")
    landing = row.get("landing_page_url", "")

    if local_pdf:
        path = Path(local_pdf)
        if path.exists():
            return extract_pdf_text_path(path), "local_pdf"

    if pdf_url:
        response = fetch_url(pdf_url)
        if response is not None:
            content_type = (response.headers.get("Content-Type") or "").lower()
            if "pdf" in content_type or pdf_url.lower().endswith(".pdf"):
                try:
                    return extract_pdf_text_bytes(response.content), "remote_pdf"
                except Exception:
                    pass
            else:
                text = html_to_text(response.content)
                if text:
                    return text, "remote_html_from_pdf_url"

    if landing:
        response = fetch_url(landing)
        if response is not None:
            content_type = (response.headers.get("Content-Type") or "").lower()
            if "pdf" in content_type:
                try:
                    return extract_pdf_text_bytes(response.content), "landing_pdf"
                except Exception:
                    pass
            text = html_to_text(response.content)
            if text:
                return text, "landing_html"

    return "", "unavailable"


def review_text(title: str, text: str) -> tuple[str, str, str, str]:
    corpus = f"{title}\n{text}"
    corpus = re.sub(r"\s+", " ", corpus)

    institutional = count_matches(corpus, INSTITUTIONAL_TERMS)
    implementation = count_matches(corpus, IMPLEMENTATION_TERMS)
    evidence = count_matches(corpus, EVIDENCE_TERMS)
    exclude_hits = {key: count_matches(corpus, patterns)
                    for key, patterns in EXCLUDE_TERMS.items()}

    if len(corpus) < 1200:
        return (
            "needs_human_check",
            "insufficient_fulltext_access",
            "low",
            "Accessible text was too limited to make a defensible full-text decision.",
        )

    if exclude_hits["survey_or_review"] >= 1 and implementation == 0:
        return (
            "exclude",
            "policy_or_commentary_only",
            "high",
            "Paper reads as a survey/review/guide rather than a concrete institutional consortium implementation study.",
        )

    if exclude_hits["theory_or_standard_focus"] >= 1 and evidence <= 1 and institutional == 0:
        return (
            "exclude",
            "no_quantitative_or_reproducible_evidence",
            "high",
            "Paper is dominated by theory, standards, or formal analysis without the target institutional implementation context.",
        )

    if institutional >= 2 and implementation >= 2 and evidence >= 1:
        return (
            "include",
            "meets_fulltext_criteria",
            "high",
            "Full text shows institutional or consortium context, concrete blockchain system design or implementation, and evaluative evidence.",
        )

    if institutional >= 1 and implementation >= 2 and evidence >= 2:
        return (
            "include",
            "meets_fulltext_criteria",
            "medium",
            "Paper provides implementation and evaluation detail with at least one credible institutional or interoperability signal.",
        )

    if exclude_hits["consumer_or_market_focus"] >= 1 and institutional <= 1:
        return (
            "exclude",
            "not_institutional_setting",
            "medium",
            "The full text appears to focus on consumer, market, or adoption concerns rather than institutional consortium workflow design.",
        )

    if exclude_hits["single_domain_without_institutional_workflow"] >= 2 and institutional == 0:
        return (
            "exclude",
            "not_institutional_setting",
            "medium",
            "The paper emphasizes a technical domain problem but does not establish the required inter-institutional or consortium workflow setting.",
        )

    if implementation == 0:
        return (
            "exclude",
            "no_implementation_detail",
            "medium",
            "The accessible full text does not provide enough implementation detail for inclusion under the protocol.",
        )

    if evidence == 0:
        return (
            "exclude",
            "no_quantitative_or_reproducible_evidence",
            "medium",
            "The full text lacks quantitative or reproducible technical evidence required by the protocol.",
        )

    return (
        "needs_human_check",
        "borderline_fulltext_case",
        "medium",
        "Full text contains mixed signals and still needs manual judgment against the review scope.",
    )


def load_target_rows() -> list[dict]:
    with PRIORITY_INPUT.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if row.get("priority_bucket") in TARGET_BUCKETS]


def update_fulltext_screening(results: list[dict]) -> None:
    with FULLTEXT_SCREENING.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = rows[0].keys()

    decision_map = {norm_title(row["title"]): row for row in results}

    changed = 0
    for row in rows:
        key = norm_title(row.get("title", ""))
        review = decision_map.get(key)
        if not review:
            continue
        row["fulltext_status"] = "agent-reviewed"
        row["fulltext_decision"] = review["agent_fulltext_decision"]
        row["fulltext_exclusion_reason_code"] = review["agent_reason_code"] if review["agent_fulltext_decision"] == "exclude" else ""
        row["fulltext_exclusion_reason_detail"] = review["agent_rationale"]
        row["reviewer_1"] = "agent-fulltext-review"
        row["conflict_status"] = "pending-author-check"
        row["final_decision"] = ""
        row["pdf_collected"] = "yes" if review["text_source"] != "unavailable" else "no"
        row["pdf_path_or_link"] = review.get("local_pdf_path") or review.get(
            "pdf_url") or review.get("landing_page_url") or ""
        row["notes"] = f"Accessible full-text agent review ({review['agent_confidence']}): {review['agent_rationale']}"
        changed += 1

    with FULLTEXT_SCREENING.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated fulltext_screening rows: {changed}")


def main():
    rows = load_target_rows()
    results = []
    counts = Counter()
    source_counts = Counter()

    for row in rows:
        text, text_source = get_text_for_row(row)
        decision, reason, confidence, rationale = review_text(
            row.get("title", ""), text)
        result = {
            "uncertain_id": row.get("uncertain_id", ""),
            "title": row.get("title", ""),
            "year": row.get("year", ""),
            "venue": row.get("venue", ""),
            "priority_bucket": row.get("priority_bucket", ""),
            "text_source": text_source,
            "text_available": "yes" if text else "no",
            "text_length": str(len(text)),
            "agent_fulltext_decision": decision,
            "agent_reason_code": reason,
            "agent_confidence": confidence,
            "agent_rationale": rationale,
            "landing_page_url": row.get("landing_page_url", ""),
            "pdf_url": row.get("pdf_url", ""),
            "local_pdf_path": row.get("local_pdf_path", ""),
        }
        results.append(result)
        counts[decision] += 1
        source_counts[text_source] += 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(results)

    with REPORT.open("w", encoding="utf-8") as handle:
        handle.write("# Accessible Full-Text Agent Review Report\n\n")
        handle.write(f"- Accessible papers reviewed: {len(results)}\n")
        handle.write(f"- include: {counts['include']}\n")
        handle.write(f"- exclude: {counts['exclude']}\n")
        handle.write(f"- needs_human_check: {counts['needs_human_check']}\n\n")
        handle.write("## Text-source coverage\n")
        for key, value in source_counts.items():
            handle.write(f"- {key}: {value}\n")
        handle.write("\n## Note\n")
        handle.write("- These are agent full-text decisions for accessible papers and should be treated as audit-ready recommendations, not unreviewable ground truth.\n")

    update_fulltext_screening(results)
    print(f"Reviewed accessible papers: {len(results)}")
    print(f"include={counts['include']}")
    print(f"exclude={counts['exclude']}")
    print(f"needs_human_check={counts['needs_human_check']}")
    print(f"Wrote {OUTPUT}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
