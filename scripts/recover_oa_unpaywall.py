#!/usr/bin/env python3
"""Recover open-access full texts for paywalled papers via Unpaywall API.

For every paper in fulltext_screening.csv that has no local_path (paywalled),
queries the Unpaywall API by DOI to find a legal OA copy, downloads it, and
saves to data/fulltext/tier-ab/ (Tier A/B) or data/fulltext/oa-recovered/
(Tier C/D). Then re-runs extraction on newly acquired files.

Outputs:
  data/reports/unpaywall_recovery_report.md
  Updated fulltext_screening.csv (local_path column)
"""

from __future__ import annotations

import csv
import io
import time
from collections import Counter
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from pypdf.errors import EmptyFileError, PdfReadError

ROOT = Path(__file__).resolve().parents[1]
SCREENING = ROOT / "data" / "processed" / "fulltext_screening.csv"
QUALITY_CSV = ROOT / "data" / "processed" / "quality_assessment.csv"
TIERAB_DIR = ROOT / "data" / "fulltext" / "tier-ab"
OA_DIR = ROOT / "data" / "fulltext" / "oa-recovered"
REPORT = ROOT / "data" / "reports" / "unpaywall_recovery_report.md"

UNPAYWALL_BASE = "https://api.unpaywall.org/v2"
MAILTO = "anthony@kumoh.ac.kr"
USER_AGENT = "BCN-SLR-OA-Recovery/1.0 (mailto:anthony@kumoh.ac.kr)"
TIMEOUT = 40
DELAY = 1.0   # polite rate limit


def _headers() -> dict:
    return {"User-Agent": USER_AGENT, "Accept": "application/pdf,text/html,*/*"}


def unpaywall_lookup(doi: str) -> dict | None:
    """Return Unpaywall JSON for a DOI, or None on failure."""
    url = f"{UNPAYWALL_BASE}/{doi}?email={MAILTO}"
    try:
        r = requests.get(url, headers=_headers(), timeout=TIMEOUT)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def best_oa_url(data: dict) -> tuple[str | None, str]:
    """Extract the best OA PDF URL from Unpaywall response.
    Returns (url, url_type) where url_type is 'pdf' or 'html'."""
    best = data.get("best_oa_location") or {}
    url_pdf = best.get("url_for_pdf")
    url_landing = best.get("url_for_landing_page") or best.get("url")

    # Try all OA locations for a PDF URL
    for loc in data.get("oa_locations", []):
        if loc.get("url_for_pdf"):
            return loc["url_for_pdf"], "pdf"

    if url_pdf:
        return url_pdf, "pdf"
    if url_landing:
        return url_landing, "html"
    return None, ""


def fetch_url(url: str) -> tuple[bytes | None, str]:
    """Fetch URL, return (content, content_type)."""
    try:
        r = requests.get(url, headers=_headers(), timeout=TIMEOUT, stream=True)
        r.raise_for_status()
        ct = r.headers.get("content-type", "")
        return r.content, ct
    except Exception:
        return None, ""


def scrape_pdf_from_html(html_content: bytes, base_url: str) -> tuple[bytes | None, str]:
    """Try to find and fetch a PDF link from HTML page."""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if ".pdf" in href.lower() or "pdf" in href.lower():
                if href.startswith("http"):
                    pdf_url = href
                elif href.startswith("/"):
                    from urllib.parse import urlparse
                    p = urlparse(base_url)
                    pdf_url = f"{p.scheme}://{p.netloc}{href}"
                else:
                    continue
                content, ct = fetch_url(pdf_url)
                if content and "pdf" in ct:
                    return content, pdf_url
    except Exception:
        pass
    return None, ""


def verify_pdf(content: bytes) -> bool:
    """Return True if content is a readable PDF with extractable text."""
    try:
        reader = PdfReader(io.BytesIO(content))
        text = ""
        for page in reader.pages[:2]:
            text += page.extract_text() or ""
        return len(text.strip()) > 100
    except Exception:
        return False


def main() -> None:
    TIERAB_DIR.mkdir(parents=True, exist_ok=True)
    OA_DIR.mkdir(parents=True, exist_ok=True)

    # Load tier map
    cid_to_tier: dict[str, str] = {}
    with open(QUALITY_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid_to_tier[row["candidate_id"]] = row["tier"]

    # Load screening rows
    screening_rows: list[dict] = []
    with open(SCREENING, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        screening_rows = list(reader)

    if "local_path" not in fieldnames:
        fieldnames.append("local_path")

    # Identify candidates: no local_path, has DOI
    candidates = [
        r for r in screening_rows
        if not r.get("local_path", "").strip() and r.get("doi", "").strip()
    ]
    print(f"Papers without local file (have DOI): {len(candidates)}")

    status_counts: Counter = Counter()
    recovered: list[dict] = []
    failed: list[dict] = []

    for i, row in enumerate(candidates, 1):
        cid = row["candidate_id"]
        tier = cid_to_tier.get(cid, "?")
        doi = row["doi"].strip()
        title = row.get("title", "")[:70]
        print(f"[{i:3}/{len(candidates)}] [{tier}] {cid}: {title}")

        # Check if already downloaded since we last ran
        out_dir = TIERAB_DIR if tier in ("A", "B") else OA_DIR
        existing_pdf = out_dir / f"{cid}.pdf"
        existing_html = out_dir / f"{cid}.html"
        if existing_pdf.exists() or existing_html.exists():
            local = existing_pdf if existing_pdf.exists() else existing_html
            print(f"         -> already exists: {local.name}")
            row["local_path"] = str(local.relative_to(ROOT))
            status_counts["already_exists"] += 1
            recovered.append(row)
            continue

        # Unpaywall lookup
        data = unpaywall_lookup(doi)
        time.sleep(DELAY)

        if data is None:
            print(f"         -> Unpaywall: no record")
            status_counts["no_record"] += 1
            failed.append(row)
            continue

        is_oa = data.get("is_oa", False)
        if not is_oa:
            print(f"         -> Unpaywall: confirmed paywalled (is_oa=False)")
            status_counts["confirmed_paywalled"] += 1
            failed.append(row)
            continue

        oa_url, url_type = best_oa_url(data)
        if not oa_url:
            print(f"         -> Unpaywall: is_oa=True but no usable URL")
            status_counts["oa_no_url"] += 1
            failed.append(row)
            continue

        print(f"         -> Unpaywall found: [{url_type}] {oa_url[:80]}")

        # Fetch content
        content, ct = fetch_url(oa_url)
        time.sleep(DELAY)

        if content is None:
            print(f"         -> fetch failed")
            status_counts["fetch_failed"] += 1
            failed.append(row)
            continue

        # If HTML, try to scrape PDF link
        if "html" in ct and url_type != "pdf":
            pdf_content, pdf_url = scrape_pdf_from_html(content, oa_url)
            if pdf_content:
                content = pdf_content
                ct = "application/pdf"
                print(f"         -> scraped PDF from HTML: {pdf_url[:60]}")

        # Determine what we have
        if "pdf" in ct or oa_url.lower().endswith(".pdf"):
            if not verify_pdf(content):
                print(f"         -> PDF not readable (image-only or corrupt)")
                # Save anyway — may still be useful
                ext = ".pdf"
                dl_type = "pdf_no_text"
            else:
                ext = ".pdf"
                dl_type = "pdf"
        else:
            ext = ".html"
            dl_type = "html"

        out_path = out_dir / f"{cid}{ext}"
        try:
            out_path.write_bytes(content)
            size_kb = len(content) // 1024
            print(f"         -> saved {dl_type} ({size_kb} KB) -> {out_path.name}")
            row["local_path"] = str(out_path.relative_to(ROOT))
            status_counts[f"saved_{dl_type}"] += 1
            recovered.append(row)
        except Exception as e:
            print(f"         -> write error: {e}")
            status_counts["write_error"] += 1
            failed.append(row)

    # Update screening CSV
    recovered_map = {r["candidate_id"]: r["local_path"] for r in recovered if r.get("local_path")}
    for row in screening_rows:
        if row["candidate_id"] in recovered_map:
            row["local_path"] = recovered_map[row["candidate_id"]]

    with open(SCREENING, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(screening_rows)

    newly_saved = sum(v for k, v in status_counts.items() if k.startswith("saved_"))
    print(f"\nDone. Newly recovered: {newly_saved}. Summary: {dict(status_counts)}")

    # Report
    import datetime
    lines = [
        "# Unpaywall OA Recovery Report",
        "",
        f"**Date:** {datetime.date.today().isoformat()}",
        f"**Candidates queried:** {len(candidates)}",
        f"**Newly recovered:** {newly_saved}",
        "",
        "## Status breakdown",
        "",
        "| Status | Count |",
        "|--------|-------|",
    ]
    for k, v in sorted(status_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {k} | {v} |")

    lines += [
        "",
        "## Recovered papers",
        "",
        "| candidate_id | tier | title | local_path |",
        "|---|---|---|---|",
    ]
    for r in recovered:
        if r.get("local_path") and not r["local_path"].startswith("data\\fulltext\\tier-ab"):
            # newly recovered (not already_exists in tier-ab)
            pass
        t = r.get("title", "")[:60].replace("|", "/")
        tier = cid_to_tier.get(r["candidate_id"], "?")
        lines.append(f"| {r['candidate_id']} | {tier} | {t} | {r.get('local_path','')} |")

    lines += [
        "",
        "## Next steps",
        "",
        "- Run `scripts/extract_tierab_data.py` to extract fields from newly downloaded papers",
        "- Run `scripts/synthesize_evidence.py` to update synthesis tables",
        "",
    ]

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
