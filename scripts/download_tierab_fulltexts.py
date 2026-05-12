#!/usr/bin/env python3
"""Download and save full-text PDFs for open-access Tier A/B papers.

Reads quality_assessment.csv (tier A/B) and fulltext_screening.csv
(pdf_collected=yes rows with http pdf_path_or_link), attempts to fetch
each paper's full text, and saves PDFs/HTML to data/fulltext/tier-ab/.

Also produces a summary report at data/reports/tierab_download_report.md
and updates fulltext_screening.csv with local_path where newly saved.

Priority order per paper:
  1. Direct PDF URL from pdf_path_or_link
  2. arXiv abs -> arXiv PDF (if doi/url signals arxiv)
  3. OpenAlex OA pdf_url lookup by DOI
  4. OpenAlex OA landing_page_url -> scrape for PDF link
"""

from __future__ import annotations

import csv
import io
import re
import time
from collections import Counter
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from pypdf.errors import EmptyFileError, PdfReadError

ROOT = Path(__file__).resolve().parents[1]
SCREENING = ROOT / "data" / "processed" / "fulltext_screening.csv"
QA_CSV = ROOT / "data" / "processed" / "quality_assessment.csv"
OUT_DIR = ROOT / "data" / "fulltext" / "tier-ab"
REPORT = ROOT / "data" / "reports" / "tierab_download_report.md"

OPENALEX_WORKS = "https://api.openalex.org/works"
MAILTO = "anthony@kumoh.ac.kr"
USER_AGENT = "BCN-SLR-TierAB-Download/1.0"
TIMEOUT = 45
DELAY = 1.2  # polite delay between requests


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _headers(extra: dict | None = None) -> dict:
    h = {"User-Agent": USER_AGENT, "Accept": "application/pdf,text/html,*/*"}
    if extra:
        h.update(extra)
    return h


def _get(url: str, stream: bool = False) -> requests.Response | None:
    try:
        r = requests.get(url, headers=_headers(),
                         timeout=TIMEOUT, stream=stream)
        r.raise_for_status()
        return r
    except Exception:
        return None


def _safe_filename(candidate_id: str, ext: str) -> str:
    return f"{candidate_id}{ext}"


def _arxiv_pdf_url(url: str, doi: str) -> str | None:
    """Convert arXiv abstract URL or DOI to PDF URL."""
    for src in (url, doi):
        if not src:
            continue
        m = re.search(r"arxiv\.org/abs/([^\s/?#]+)", src)
        if m:
            return f"https://arxiv.org/pdf/{m.group(1)}"
        m = re.search(r"arxiv[:/](\d{4}\.\d{4,5})", src, re.I)
        if m:
            return f"https://arxiv.org/pdf/{m.group(1)}"
    return None


def _openalex_oa_urls(doi: str) -> tuple[str | None, str | None]:
    """Return (pdf_url, landing_page_url) from OpenAlex for a given DOI."""
    if not doi:
        return None, None
    url = f"{OPENALEX_WORKS}/https://doi.org/{doi}?mailto={MAILTO}"
    r = _get(url)
    if r is None:
        return None, None
    try:
        data = r.json()
        oa = data.get("open_access", {})
        return oa.get("oa_url"), data.get("primary_location", {}).get("landing_page_url")
    except Exception:
        return None, None


def _scrape_pdf_link(landing_url: str) -> str | None:
    """Try to find a direct PDF link from a landing page."""
    r = _get(landing_url)
    if r is None:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        if href.lower().endswith(".pdf") or "pdf" in href.lower():
            if href.startswith("http"):
                return href
            elif href.startswith("/"):
                from urllib.parse import urlparse
                p = urlparse(landing_url)
                return f"{p.scheme}://{p.netloc}{href}"
    return None


def fetch_fulltext(row: dict) -> tuple[bytes | None, str, str]:
    """
    Attempt to fetch full text for a paper row.
    Returns (content_bytes, source_type, final_url_used).
    content_bytes is None on failure.
    source_type is one of: 'remote_pdf', 'arxiv_pdf', 'openalex_pdf',
                            'landing_html', 'scraped_pdf', 'failed'
    """
    doi = row.get("doi", "").strip()
    url = row.get("pdf_path_or_link", "").strip() or row.get("url", "").strip()

    # 1. arXiv direct
    arxiv_url = _arxiv_pdf_url(url, doi)
    if arxiv_url:
        r = _get(arxiv_url)
        if r and r.headers.get("content-type", "").startswith("application/pdf"):
            return r.content, "arxiv_pdf", arxiv_url

    # 2. Direct PDF link
    if url and url.startswith("http"):
        r = _get(url)
        if r:
            ct = r.headers.get("content-type", "")
            if "pdf" in ct or url.lower().endswith(".pdf"):
                return r.content, "remote_pdf", url
            # It might be HTML - save it
            if "html" in ct:
                return r.content, "landing_html", url

    # 3. OpenAlex OA lookup
    oa_pdf, oa_landing = _openalex_oa_urls(doi)
    if oa_pdf:
        r = _get(oa_pdf)
        if r and "pdf" in r.headers.get("content-type", ""):
            return r.content, "openalex_pdf", oa_pdf

    # 4. Scrape landing page for PDF link
    landing = oa_landing or url
    if landing and landing.startswith("http"):
        scraped = _scrape_pdf_link(landing)
        if scraped:
            r = _get(scraped)
            if r and "pdf" in r.headers.get("content-type", ""):
                return r.content, "scraped_pdf", scraped
        # Fall back to saving the landing HTML
        if oa_landing:
            r = _get(oa_landing)
            if r and "html" in r.headers.get("content-type", ""):
                return r.content, "landing_html", oa_landing

    return None, "failed", ""


def extract_text_preview(content: bytes, source_type: str, max_chars: int = 500) -> str:
    """Extract a short text preview to verify content quality."""
    try:
        if source_type in ("remote_pdf", "arxiv_pdf", "openalex_pdf", "scraped_pdf"):
            reader = PdfReader(io.BytesIO(content))
            text = ""
            for page in reader.pages[:3]:
                text += page.extract_text() or ""
                if len(text) > max_chars:
                    break
            return text[:max_chars].strip()
        elif source_type == "landing_html":
            soup = BeautifulSoup(content, "html.parser")
            return soup.get_text(separator=" ", strip=True)[:max_chars]
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load Tier A/B candidate IDs
    tier_ab: dict[str, str] = {}
    with open(QA_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["tier"] in ("A", "B"):
                tier_ab[row["candidate_id"]] = row["tier"]

    print(
        f"Tier A/B total: {len(tier_ab)} ({sum(1 for t in tier_ab.values() if t == 'A')} A, {sum(1 for t in tier_ab.values() if t == 'B')} B)")

    # Load fulltext_screening rows for Tier A/B with pdf_collected=yes
    screening_rows: list[dict] = []
    with open(SCREENING, encoding="utf-8") as f:
        screening_rows = list(csv.DictReader(f))

    fieldnames = list(screening_rows[0].keys()) if screening_rows else []
    if "local_path" not in fieldnames:
        fieldnames.append("local_path")

    candidates = [
        r for r in screening_rows
        if r["candidate_id"] in tier_ab and r.get("pdf_collected", "") == "yes"
    ]
    print(f"Open-access Tier A/B candidates: {len(candidates)}")

    # Track results
    results: list[dict] = []
    status_counts: Counter = Counter()

    for i, row in enumerate(candidates, 1):
        cid = row["candidate_id"]
        tier = tier_ab[cid]
        title = row.get("title", "")[:80]
        print(f"[{i:3}/{len(candidates)}] {tier} {cid}: {title}")

        # Skip if already downloaded
        existing_pdf = OUT_DIR / _safe_filename(cid, ".pdf")
        existing_html = OUT_DIR / _safe_filename(cid, ".html")
        if existing_pdf.exists():
            print(f"         -> already have PDF, skipping")
            results.append({**row, "local_path": str(existing_pdf.relative_to(ROOT)),
                           "download_status": "already_exists", "source_type": "remote_pdf"})
            status_counts["already_exists"] += 1
            continue
        if existing_html.exists():
            print(f"         -> already have HTML, skipping")
            results.append({**row, "local_path": str(existing_html.relative_to(ROOT)),
                           "download_status": "already_exists", "source_type": "landing_html"})
            status_counts["already_exists"] += 1
            continue

        content, source_type, final_url = fetch_fulltext(row)
        time.sleep(DELAY)

        if content is None:
            print(f"         -> FAILED to fetch")
            results.append(
                {**row, "local_path": "", "download_status": "failed", "source_type": "failed"})
            status_counts["failed"] += 1
            continue

        # Determine extension
        ext = ".pdf" if source_type in (
            "remote_pdf", "arxiv_pdf", "openalex_pdf", "scraped_pdf") else ".html"
        out_path = OUT_DIR / _safe_filename(cid, ext)

        try:
            out_path.write_bytes(content)
            preview = extract_text_preview(content, source_type)
            size_kb = len(content) // 1024
            print(
                f"         -> saved {source_type} ({size_kb} KB) -> {out_path.name}")
            if not preview.strip():
                print(
                    f"         -> WARNING: empty text extracted (may be image-only PDF)")
                status_counts["saved_no_text"] += 1
                dl_status = "saved_no_text"
            else:
                status_counts["saved"] += 1
                dl_status = "saved"
            rel_path = str(out_path.relative_to(ROOT))
            results.append({**row, "local_path": rel_path,
                           "download_status": dl_status, "source_type": source_type})
        except Exception as e:
            print(f"         -> ERROR writing file: {e}")
            results.append(
                {**row, "local_path": "", "download_status": "write_error", "source_type": source_type})
            status_counts["write_error"] += 1

    # Update fulltext_screening.csv with local_path for downloaded rows
    result_map = {r["candidate_id"]: r for r in results}
    updated_screening = []
    for row in screening_rows:
        cid = row["candidate_id"]
        if cid in result_map and result_map[cid].get("local_path"):
            row = dict(row)
            row["local_path"] = result_map[cid]["local_path"]
        updated_screening.append(row)

    # Add local_path column if missing
    write_fields = fieldnames
    with open(SCREENING, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=write_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(updated_screening)

    print(f"\nDone. Summary: {dict(status_counts)}")

    # Write report
    total = len(candidates)
    saved = status_counts["saved"] + status_counts["already_exists"]
    saved_no_text = status_counts["saved_no_text"]
    failed = status_counts["failed"]

    tier_a_saved = sum(1 for r in results if tier_ab.get(r["candidate_id"]) == "A" and r.get(
        "download_status") in ("saved", "already_exists", "saved_no_text"))
    tier_b_saved = sum(1 for r in results if tier_ab.get(r["candidate_id"]) == "B" and r.get(
        "download_status") in ("saved", "already_exists", "saved_no_text"))

    failed_rows = [r for r in results if r.get("download_status") == "failed"]

    report_lines = [
        "# Tier A/B Full-Text Download Report",
        "",
        f"**Date:** {__import__('datetime').date.today().isoformat()}",
        f"**Target:** {total} open-access Tier A/B papers",
        "",
        "## Summary",
        "",
        f"| Status | Count |",
        f"|--------|-------|",
        f"| Saved (text extractable) | {status_counts['saved'] + status_counts['already_exists']} |",
        f"| Saved (image-only / no text) | {saved_no_text} |",
        f"| Failed | {failed} |",
        f"| **Total attempted** | **{total}** |",
        "",
        f"**Tier A saved:** {tier_a_saved} / {sum(1 for t in tier_ab.values() if t == 'A')} Tier-A papers",
        f"**Tier B saved:** {tier_b_saved} / {sum(1 for t in tier_ab.values() if t == 'B')} Tier-B papers",
        "",
        "## Files saved to",
        "",
        f"`data/fulltext/tier-ab/` ({saved + saved_no_text} files)",
        "",
    ]

    if failed_rows:
        report_lines += [
            "## Failed Downloads",
            "",
            "| candidate_id | title | doi |",
            "|---|---|---|",
        ]
        for r in failed_rows:
            t = r.get("title", "")[:60].replace("|", "/")
            d = r.get("doi", "")
            report_lines.append(f"| {r['candidate_id']} | {t} | {d} |")
        report_lines.append("")

    report_lines += [
        "## Next Steps",
        "",
        "1. For image-only PDFs, consider OCR (e.g. `pytesseract`) or manual copy-paste.",
        "2. For failed downloads, try institutional VPN access and re-run this script.",
        "3. Run `scripts/extract_tierab_data.py` (to be written) to fill extraction fields.",
        "",
    ]

    REPORT.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Report written to {REPORT}")


if __name__ == "__main__":
    main()
