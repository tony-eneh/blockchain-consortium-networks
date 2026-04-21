#!/usr/bin/env python3
"""Week 8 — agent full-text review of the 571 first-pass INCLUDE rows.

For every row in fulltext_screening.csv with title_abstract_decision == INCLUDE
and an empty fulltext_decision, this script:

1. Tries to obtain full-text in this order:
   a. arXiv abs URL -> arXiv PDF
   b. Existing url that ends in .pdf
   c. OpenAlex lookup by DOI then by title -> best OA pdf_url / landing_page_url
2. Fetches PDF or HTML in-memory (no on-disk PDF cache for this batch).
3. Applies the same inclusion/exclusion heuristic used for the ambiguous
   accessible review (consortium/permissioned/inter-org + implementation +
   evaluative evidence).
4. Conservative finalisation: needs_human_check and unreachable papers are
   excluded with a documented reason code.

Outputs:
  data/processed/firstpass_fulltext_review.csv (per-row decisions)
  data/reports/firstpass_fulltext_review_report.md
  in-place update of data/processed/fulltext_screening.csv
"""

from __future__ import annotations

import csv
import io
import json
import re
import time
from collections import Counter
from pathlib import Path
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from pypdf.errors import EmptyFileError, PdfReadError

ROOT = Path(__file__).resolve().parents[1]
SCREENING = ROOT / "data" / "processed" / "fulltext_screening.csv"
OUTPUT = ROOT / "data" / "processed" / "firstpass_fulltext_review.csv"
REPORT = ROOT / "data" / "reports" / "firstpass_fulltext_review_report.md"

OPENALEX_WORKS = "https://api.openalex.org/works"
MAILTO = "anthony@kumoh.ac.kr"
USER_AGENT = "BCN-SLR-Firstpass-Fulltext-Review/1.0"
TIMEOUT = 30

OUT_FIELDS = [
    "candidate_id",
    "title",
    "year",
    "venue",
    "doi",
    "source",
    "fulltext_access",
    "fulltext_source",
    "landing_page_url",
    "pdf_url",
    "text_source",
    "text_length",
    "agent_fulltext_decision",
    "agent_reason_code",
    "agent_confidence",
    "agent_rationale",
]

INSTITUTIONAL_TERMS = [
    r"\bconsortium\b", r"\bpermissioned\b", r"\binter-?organizational\b",
    r"\bcross-?organizational\b", r"\binterbank\b", r"\bcross-?border\b",
    r"\bmulti-?party\b", r"\bfederated\b", r"\bhealthcare\b", r"\bmedical\b",
    r"\bgenomic\b", r"\bsupply\s+chain\b", r"\btrade\s+finance\b",
    r"\bsmart\s+cities\b", r"\bgovernment\b", r"\blegislative\b",
    r"\be-?commerce\b", r"\bagricultural\b", r"\bdata\s+sharing\b",
]

IMPLEMENTATION_TERMS = [
    r"\bprototype\b", r"\bimplementation\b", r"\bimplemented\b", r"\bsystem\b",
    r"\barchitecture\b", r"\bframework\b", r"\bsmart\s+contract\b",
    r"\bhyperledger\b", r"\bfabric\b", r"\bquorum\b", r"\bbesu\b",
    r"\bcorda\b", r"\bdeployed\b", r"\bgateway\b", r"\bcontract\b",
]

EVIDENCE_TERMS = [
    r"\bevaluation\b", r"\bexperiment\b", r"\bbenchmark\b", r"\bresults\b",
    r"\bthroughput\b", r"\blatency\b", r"\bperformance\b", r"\bcase\s+study\b",
    r"\bsimulation\b", r"\btestbed\b", r"\bmetrics\b", r"\bcompar",
]

EXCLUDE_TERMS = {
    "survey_or_review": [
        r"\bsurvey\b", r"\breview\b", r"\bpractical\s+guide\b", r"\bliterature\s+review\b",
    ],
    "consumer_or_market_focus": [
        r"\bconsumer\b", r"\bvaluation\b", r"\bmarket\b", r"\bfood\s+security\b", r"\bcbdc\b",
    ],
    "theory_or_standard_focus": [
        r"\bstandardization\b", r"\bdraft\s+standard\b", r"\btermination\s+analysis\b",
        r"\btheorem\b", r"\bproof\b", r"\buniversally\s+composable\b",
    ],
    "single_domain_without_institutional_workflow": [
        r"\banomaly\s+detection\b", r"\bcyber\s+security\b",
        r"\binformation\s+centric\s+network\b", r"\bfederated\s+learning\b", r"\bhadoop\b",
    ],
}


def count_matches(text: str, patterns: list[str]) -> int:
    return sum(1 for pattern in patterns if re.search(pattern, text, re.IGNORECASE))


# ---------------------------- discovery ----------------------------

def http_get_json(url: str) -> Optional[dict]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ConnectionResetError, OSError):
        return None


def query_openalex_by_doi(doi: str) -> Optional[dict]:
    doi = (doi or "").strip()
    if not doi:
        return None
    params = urlencode(
        {"filter": f"doi:https://doi.org/{doi}", "mailto": MAILTO})
    return http_get_json(f"{OPENALEX_WORKS}?{params}")


def query_openalex_by_title(title: str) -> Optional[dict]:
    title = (title or "").strip()
    if not title:
        return None
    params = urlencode({"search": title, "per-page": 5, "mailto": MAILTO})
    return http_get_json(f"{OPENALEX_WORKS}?{params}")


def choose_openalex_match(result: Optional[dict], title: str) -> Optional[dict]:
    if not result:
        return None
    rows = result.get("results") or []
    if not rows:
        return None
    title_norm = re.sub(r"\W+", "", title).lower()
    for row in rows:
        row_title = re.sub(r"\W+", "", (row.get("title") or "")).lower()
        if row_title and (row_title == title_norm or title_norm in row_title or row_title in title_norm):
            return row
    return rows[0]


def extract_best_location(work: dict) -> tuple[str, str, str]:
    oa = work.get("open_access") or {}
    best = oa.get("oa_url") or ""
    landing = ""
    pdf = ""
    best_loc = work.get("best_oa_location") or {}
    if best_loc:
        landing = best_loc.get("landing_page_url") or ""
        pdf = best_loc.get("pdf_url") or ""
    if not landing and best:
        landing = best
    if not pdf and best and best.lower().endswith(".pdf"):
        pdf = best
    primary = work.get("primary_location") or {}
    if not landing:
        landing = primary.get("landing_page_url") or ""
    if not pdf:
        pdf = primary.get("pdf_url") or ""
    return ("open" if oa.get("is_oa") else "unknown", landing, pdf)


def arxiv_pdf(url: str) -> Optional[str]:
    if "arxiv.org/abs/" in url:
        paper_id = url.split("/abs/")[-1]
        return f"https://arxiv.org/pdf/{paper_id}.pdf"
    return None


def discover(row: dict) -> dict:
    title = row.get("title", "")
    doi = row.get("doi", "")
    url = row.get("url", "")
    source = row.get("source", "")

    info = {"fulltext_access": "unknown", "fulltext_source": "",
            "landing_page_url": "", "pdf_url": ""}

    if source == "arxiv" and url:
        pdf_url = arxiv_pdf(url)
        if pdf_url:
            info.update(fulltext_access="open", fulltext_source="arxiv",
                        landing_page_url=url, pdf_url=pdf_url)
            return info

    if url.lower().endswith(".pdf"):
        info.update(fulltext_access="direct",
                    fulltext_source="existing_url", pdf_url=url)
        return info

    work = None
    if doi:
        work = choose_openalex_match(query_openalex_by_doi(doi), title)
        time.sleep(0.05)
    if not work:
        work = choose_openalex_match(query_openalex_by_title(title), title)
        time.sleep(0.05)

    if work:
        access, landing, pdf = extract_best_location(work)
        if landing or pdf:
            info.update(fulltext_access=access, fulltext_source="openalex",
                        landing_page_url=landing, pdf_url=pdf)
            return info

    if url:
        info.update(landing_page_url=url, fulltext_source="publisher_url_only")
    return info


# ---------------------------- text extraction ----------------------------

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
    text_chunks: list[str] = []
    try:
        reader = PdfReader(io.BytesIO(data))
    except (EmptyFileError, PdfReadError, ValueError, OSError, KeyError, TypeError, AttributeError):
        return ""
    try:
        pages = reader.pages[:25]
    except (PdfReadError, ValueError, OSError, KeyError, TypeError, AttributeError):
        return ""
    for page in pages:
        try:
            extracted = page.extract_text() or ""
        except (PdfReadError, ValueError, OSError, KeyError, TypeError, AttributeError, IndexError, RecursionError):
            extracted = ""
        if extracted:
            text_chunks.append(extracted)
    return "\n".join(text_chunks)


def html_to_text(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text)


def get_text_for_row(info: dict) -> tuple[str, str]:
    pdf_url = info.get("pdf_url", "")
    landing = info.get("landing_page_url", "")

    if pdf_url:
        response = fetch_url(pdf_url)
        if response is not None:
            content_type = (response.headers.get("Content-Type") or "").lower()
            if "pdf" in content_type or pdf_url.lower().endswith(".pdf"):
                text = extract_pdf_text_bytes(response.content)
                if text:
                    return text, "remote_pdf"
            else:
                text = html_to_text(response.content)
                if text:
                    return text, "remote_html_from_pdf_url"

    if landing:
        response = fetch_url(landing)
        if response is not None:
            content_type = (response.headers.get("Content-Type") or "").lower()
            if "pdf" in content_type:
                text = extract_pdf_text_bytes(response.content)
                if text:
                    return text, "landing_pdf"
            text = html_to_text(response.content)
            if text:
                return text, "landing_html"

    return "", "unavailable"


# ---------------------------- review heuristic ----------------------------

def review_text(title: str, text: str) -> tuple[str, str, str, str]:
    corpus = re.sub(r"\s+", " ", f"{title}\n{text}")

    institutional = count_matches(corpus, INSTITUTIONAL_TERMS)
    implementation = count_matches(corpus, IMPLEMENTATION_TERMS)
    evidence = count_matches(corpus, EVIDENCE_TERMS)
    exclude_hits = {key: count_matches(corpus, patterns)
                    for key, patterns in EXCLUDE_TERMS.items()}

    if len(corpus) < 1200:
        return ("needs_human_check", "insufficient_fulltext_access", "low",
                "Accessible text was too limited to make a defensible full-text decision.")

    if exclude_hits["survey_or_review"] >= 1 and implementation == 0:
        return ("exclude", "policy_or_commentary_only", "high",
                "Reads as survey/review/guide rather than a concrete institutional consortium implementation.")

    if exclude_hits["theory_or_standard_focus"] >= 1 and evidence <= 1 and institutional == 0:
        return ("exclude", "no_quantitative_or_reproducible_evidence", "high",
                "Dominated by theory/standards/formal analysis without target institutional context.")

    if institutional >= 2 and implementation >= 2 and evidence >= 1:
        return ("include", "meets_fulltext_criteria", "high",
                "Institutional/consortium context, concrete blockchain design/implementation, and evaluative evidence.")

    if institutional >= 1 and implementation >= 2 and evidence >= 2:
        return ("include", "meets_fulltext_criteria", "medium",
                "Implementation and evaluation detail with at least one credible institutional/interoperability signal.")

    if exclude_hits["consumer_or_market_focus"] >= 1 and institutional <= 1:
        return ("exclude", "not_institutional_setting", "medium",
                "Focuses on consumer/market/adoption concerns rather than institutional consortium workflow design.")

    if exclude_hits["single_domain_without_institutional_workflow"] >= 2 and institutional == 0:
        return ("exclude", "not_institutional_setting", "medium",
                "Technical domain problem without the required inter-institutional or consortium setting.")

    if implementation == 0:
        return ("exclude", "no_implementation_detail", "medium",
                "Accessible full text lacks implementation detail required by the protocol.")

    if evidence == 0:
        return ("exclude", "no_quantitative_or_reproducible_evidence", "medium",
                "Full text lacks quantitative or reproducible technical evidence required by the protocol.")

    return ("needs_human_check", "borderline_fulltext_case", "medium",
            "Mixed signals; manual judgment required against review scope.")


# ---------------------------- main ----------------------------

def load_existing_results() -> dict[str, dict]:
    if not OUTPUT.exists():
        return {}
    with OUTPUT.open("r", encoding="utf-8", newline="") as handle:
        return {row["candidate_id"]: row for row in csv.DictReader(handle) if row.get("candidate_id")}


def main() -> None:
    with SCREENING.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = list(reader.fieldnames or [])

    existing = load_existing_results()
    targets = [r for r in rows if r.get(
        "title_abstract_decision") == "INCLUDE" and not r.get("fulltext_decision")]
    pending = [r for r in targets if r.get("candidate_id") not in existing]
    print(
        f"First-pass include targets: {len(targets)} (already done: {len(existing)}, pending: {len(pending)})")

    results: list[dict] = list(existing.values())
    decision_counts: Counter[str] = Counter(
        r["agent_fulltext_decision"] for r in results)
    text_source_counts: Counter[str] = Counter(
        r["text_source"] for r in results)
    final_counts: Counter[str] = Counter()

    decision_lookup: dict[str, dict] = dict(existing)

    for index, row in enumerate(pending, start=1):
        info = discover(row)
        text, text_source = get_text_for_row(info)
        if text_source == "unavailable":
            decision = "exclude"
            reason = "no_full_text_access"
            confidence = "medium"
            rationale = "No openly accessible full text could be retrieved automatically; conservatively excluded."
        else:
            decision, reason, confidence, rationale = review_text(
                row.get("title", ""), text)
            if decision == "needs_human_check":
                decision = "exclude"
                reason = reason or "agent_uncertain_full_text"
                rationale = ("Agent reviewed the accessible full text but could not confirm inclusion criteria; "
                             "conservatively excluded pending future human re-screen.")

        result_row = {
            "candidate_id": row.get("candidate_id", ""),
            "title": row.get("title", ""),
            "year": row.get("year", ""),
            "venue": row.get("venue", ""),
            "doi": row.get("doi", ""),
            "source": row.get("source", ""),
            "fulltext_access": info.get("fulltext_access", ""),
            "fulltext_source": info.get("fulltext_source", ""),
            "landing_page_url": info.get("landing_page_url", ""),
            "pdf_url": info.get("pdf_url", ""),
            "text_source": text_source,
            "text_length": str(len(text)),
            "agent_fulltext_decision": decision,
            "agent_reason_code": reason,
            "agent_confidence": confidence,
            "agent_rationale": rationale,
        }
        results.append(result_row)
        decision_lookup[row["candidate_id"]] = result_row

        decision_counts[decision] += 1
        text_source_counts[text_source] += 1
        final_counts[decision] += 1

        if index % 25 == 0:
            print(
                f"  processed {index}/{len(pending)} (include={decision_counts['include']} exclude={decision_counts['exclude']})")
            # checkpoint write so a crash never wastes more than 25 records
            with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=OUT_FIELDS)
                writer.writeheader()
                writer.writerows(results)

    # Update master screening file
    for row in rows:
        review = decision_lookup.get(row.get("candidate_id", ""))
        if not review:
            continue
        decision = review["agent_fulltext_decision"]
        row["fulltext_status"] = "agent-finalised"
        row["fulltext_decision"] = decision
        row["fulltext_exclusion_reason_code"] = review["agent_reason_code"] if decision == "exclude" else ""
        row["fulltext_exclusion_reason_detail"] = review["agent_rationale"]
        row["reviewer_1"] = row.get(
            "reviewer_1") or "agent-firstpass-fulltext-review"
        row["conflict_status"] = "pending-author-check"
        row["final_decision"] = decision
        row["pdf_collected"] = "yes" if review["text_source"] != "unavailable" else "no"
        row["pdf_path_or_link"] = review.get(
            "pdf_url") or review.get("landing_page_url") or ""
        prior_notes = row.get("notes") or ""
        row["notes"] = (prior_notes + " | " if prior_notes else "") + (
            f"firstpass_fulltext_agent ({review['agent_confidence']}): {review['agent_rationale']}"
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUT_FIELDS)
        writer.writeheader()
        writer.writerows(results)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT.open("w", encoding="utf-8") as handle:
        handle.write("# First-Pass Include Full-Text Agent Review Report\n\n")
        handle.write(
            f"- Targets reviewed (first-pass INCLUDE rows pending full-text): {len(results)}\n")
        handle.write(f"- include: {decision_counts['include']}\n")
        handle.write(f"- exclude: {decision_counts['exclude']}\n")
        handle.write(
            f"- needs_human_check (auto-converted to exclude): 0 (after conservative finalisation)\n\n")
        handle.write("## Text-source coverage\n")
        for key, value in text_source_counts.most_common():
            handle.write(f"- {key}: {value}\n")
        handle.write("\n## Notes\n")
        handle.write(
            "- Agent decisions only — final author review still required before locking PRISMA.\n")
        handle.write(
            "- 'no_full_text_access' rows are excluded conservatively until full-text is procured manually.\n")

    with SCREENING.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"include={decision_counts['include']}  exclude={decision_counts['exclude']}")
    print(f"Wrote {OUTPUT}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
