#!/usr/bin/env python3
"""Discover and optionally download open full-texts for ambiguous papers.

Input:
  data/processed/uncertain_needs_manual.csv

Outputs:
  data/processed/uncertain_needs_manual_fulltext.csv
  data/reports/ambiguous_fulltext_discovery_report.md
  data/fulltext/ambiguous/*.pdf  (for directly downloadable PDFs)

Strategy:
- arXiv rows: derive direct PDF URL from abs URL and download.
- DOI rows: query OpenAlex for OA locations and PDF URLs.
- Title fallback: query OpenAlex title search when DOI lookup fails.
- Existing URLs that already look like PDFs are tested and downloaded.

This only targets open/directly accessible full texts. It will not bypass
publisher paywalls.
"""

from __future__ import annotations

import csv
import json
import re
import time
from pathlib import Path
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

INPUT = Path("data/processed/uncertain_needs_manual.csv")
OUTPUT = Path("data/processed/uncertain_needs_manual_fulltext.csv")
REPORT = Path("data/reports/ambiguous_fulltext_discovery_report.md")
DOWNLOAD_DIR = Path("data/fulltext/ambiguous")

OPENALEX_WORKS = "https://api.openalex.org/works"
MAILTO = "anthony@kumoh.ac.kr"
USER_AGENT = "BCN-SLR-Fulltext-Discovery/1.0"

OUT_FIELDS = [
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
    "fulltext_found",
    "fulltext_access",
    "fulltext_source",
    "landing_page_url",
    "pdf_url",
    "download_status",
    "local_pdf_path",
    "notes",
]


def slugify(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return text[:80] or "paper"


def http_get_json(url: str) -> Optional[dict]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None


def head_or_get(url: str) -> tuple[bool, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=25) as resp:
            content_type = (resp.headers.get("Content-Type") or "").lower()
            final_url = resp.geturl()
            return True, f"{content_type}|{final_url}"
    except (HTTPError, URLError, TimeoutError) as exc:
        return False, str(exc)


def download_file(url: str, dest: Path) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=30) as resp:
            content_type = (resp.headers.get("Content-Type") or "").lower()
            if "pdf" not in content_type and not resp.geturl().lower().endswith(".pdf"):
                return f"skipped_non_pdf:{content_type}"
            data = resp.read()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            return "downloaded"
    except (HTTPError, URLError, TimeoutError, ConnectionResetError, OSError) as exc:
        return f"download_failed:{exc}"


def arxiv_pdf(url: str) -> Optional[str]:
    if "arxiv.org/abs/" in url:
        paper_id = url.split("/abs/")[-1]
        return f"https://arxiv.org/pdf/{paper_id}.pdf"
    return None


def query_openalex_by_doi(doi: str) -> Optional[dict]:
    doi = doi.strip()
    if not doi:
        return None
    params = urlencode(
        {"filter": f"doi:https://doi.org/{doi}", "mailto": MAILTO})
    return http_get_json(f"{OPENALEX_WORKS}?{params}")


def query_openalex_by_title(title: str) -> Optional[dict]:
    title = title.strip()
    if not title:
        return None
    params = urlencode({"search": title, "per-page": 5, "mailto": MAILTO})
    return http_get_json(f"{OPENALEX_WORKS}?{params}")


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

    return (
        "open" if oa.get("is_oa") else "unknown",
        landing,
        pdf,
    )


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


def discover(row: dict) -> dict:
    title = row.get("title", "")
    doi = row.get("doi", "")
    url = row.get("url", "")
    source = row.get("source", "")

    result = {
        **{field: row.get(field, "") for field in [
            "uncertain_id", "title", "authors", "year", "venue", "doi", "url",
            "source", "screen_reason", "second_pass_recommendation", "confidence",
        ]},
        "fulltext_found": "no",
        "fulltext_access": "unknown",
        "fulltext_source": "",
        "landing_page_url": "",
        "pdf_url": "",
        "download_status": "not_attempted",
        "local_pdf_path": "",
        "notes": "",
    }

    if source == "arxiv" and url:
        pdf_url = arxiv_pdf(url)
        if pdf_url:
            result["fulltext_found"] = "yes"
            result["fulltext_access"] = "open"
            result["fulltext_source"] = "arxiv"
            result["landing_page_url"] = url
            result["pdf_url"] = pdf_url
            return result

    if url.lower().endswith(".pdf"):
        ok, note = head_or_get(url)
        if ok:
            result["fulltext_found"] = "yes"
            result["fulltext_access"] = "direct"
            result["fulltext_source"] = "existing_url"
            result["pdf_url"] = url
            result["notes"] = note
            return result

    work = None
    if doi:
        work = choose_openalex_match(query_openalex_by_doi(doi), title)
        time.sleep(0.1)
    if not work:
        work = choose_openalex_match(query_openalex_by_title(title), title)
        time.sleep(0.1)

    if work:
        access, landing, pdf = extract_best_location(work)
        if landing or pdf:
            result["fulltext_found"] = "yes"
            result["fulltext_access"] = access
            result["fulltext_source"] = "openalex"
            result["landing_page_url"] = landing
            result["pdf_url"] = pdf
            return result

    if url:
        result["landing_page_url"] = url
        result["fulltext_source"] = "publisher_url_only"
        result["notes"] = "No OA PDF discovered automatically; publisher or abstract page available."

    return result


def main():
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    with INPUT.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    discovered = []
    found_count = 0
    downloaded_count = 0
    open_count = 0

    for row in rows:
        try:
            entry = discover(row)

            pdf_url = entry.get("pdf_url", "")
            if entry["fulltext_found"] == "yes":
                found_count += 1
            if entry["fulltext_access"] in {"open", "direct"}:
                open_count += 1
            if pdf_url:
                filename = f"{entry['uncertain_id']}-{slugify(entry['title'])}.pdf"
                dest = DOWNLOAD_DIR / filename
                status = download_file(pdf_url, dest)
                entry["download_status"] = status
                if status == "downloaded":
                    entry["local_pdf_path"] = dest.as_posix()
                    downloaded_count += 1
            discovered.append(entry)
        except Exception as exc:
            discovered.append(
                {
                    **{field: row.get(field, "") for field in [
                        "uncertain_id", "title", "authors", "year", "venue", "doi", "url",
                        "source", "screen_reason", "second_pass_recommendation", "confidence",
                    ]},
                    "fulltext_found": "no",
                    "fulltext_access": "error",
                    "fulltext_source": "",
                    "landing_page_url": row.get("url", ""),
                    "pdf_url": "",
                    "download_status": f"row_failed:{exc}",
                    "local_pdf_path": "",
                    "notes": "Unexpected error during discovery; row retained for manual follow-up.",
                }
            )

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUT_FIELDS)
        writer.writeheader()
        writer.writerows(discovered)

    with REPORT.open("w", encoding="utf-8") as handle:
        handle.write("# Ambiguous Full-Text Discovery Report\n\n")
        handle.write(f"- Input ambiguous manual-review records: {len(rows)}\n")
        handle.write(f"- Full-text location found: {found_count}\n")
        handle.write(f"- Open/direct access detected: {open_count}\n")
        handle.write(f"- PDFs downloaded locally: {downloaded_count}\n")
        handle.write(f"- Download folder: `{DOWNLOAD_DIR.as_posix()}`\n")

    print(f"Processed manual-review records: {len(rows)}")
    print(f"fulltext_found={found_count}")
    print(f"open_or_direct={open_count}")
    print(f"downloaded={downloaded_count}")
    print(f"Wrote {OUTPUT}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
