#!/usr/bin/env python3
"""Fetch papers from OpenAlex API as a substitute for ACM DL and Scopus.

OpenAlex is completely free, open, no API key required, and indexes
~250M works including ACM, Elsevier/Scopus, Springer, IEEE, etc.

Usage:
    py scripts/fetch_openalex.py --output data/raw-search/openalex_raw.csv

Rate limit: 10 req/sec (very generous). Polite pool with email gets even more.
"""

import argparse
import csv
import json
import time
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

OPENALEX_WORKS = "https://api.openalex.org/works"

# Focused search queries matching our PICOC scope
QUERIES = [
    "consortium blockchain governance",
    "consortium blockchain consensus evaluation",
    "permissioned blockchain interoperability",
    "permissioned blockchain institutional",
    "enterprise blockchain consortium privacy",
    "Hyperledger Fabric consortium benchmark",
    "distributed ledger cross-organizational governance",
    "blockchain cross-chain institutional interoperability",
    "blockchain consortium network performance",
    "permissioned blockchain privacy confidentiality",
]

# Contact email for polite pool (faster rate limits)
MAILTO = "anthony@kumoh.ac.kr"


def fetch_openalex(query: str, max_results: int = 200, year_from: int = 2021) -> list[dict]:
    """Fetch works from OpenAlex for a single search query."""
    papers = []
    page = 1
    per_page = min(max_results, 200)

    while len(papers) < max_results:
        params = urlencode({
            "search": query,
            "filter": f"from_publication_date:{year_from}-01-01,type:article|proceedings-article|preprint",
            "per_page": per_page,
            "page": page,
            "mailto": MAILTO,
        })
        url = f"{OPENALEX_WORKS}?{params}"
        req = Request(url, headers={"User-Agent": "SLR-Search-Bot/1.0"})

        with urlopen(req) as resp:
            body = json.loads(resp.read())

        results = body.get("results", [])
        if not results:
            break

        papers.extend(results)
        page += 1

        meta = body.get("meta", {})
        total = meta.get("count", 0)
        if len(papers) >= total or len(papers) >= max_results:
            break

        time.sleep(0.15)  # Stay well under 10 req/sec

    return papers[:max_results]


def normalize(work: dict) -> dict:
    """Convert OpenAlex work object to our standard CSV schema."""
    # Title
    title = (work.get("title") or "").strip()

    # Authors
    authorships = work.get("authorships") or []
    authors = "; ".join(
        (a.get("author", {}).get("display_name", "") or "")
        for a in authorships
    )

    # Year
    year = str(work.get("publication_year") or "")

    # Venue — from primary_location or host_venue
    venue = ""
    loc = work.get("primary_location") or {}
    source = loc.get("source") or {}
    venue = (source.get("display_name") or "").strip()

    # Abstract — OpenAlex stores inverted index, reconstruct it
    abstract = ""
    inv_index = work.get("abstract_inverted_index")
    if inv_index:
        word_positions = []
        for word, positions in inv_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort()
        abstract = " ".join(w for _, w in word_positions)

    # DOI
    doi_url = work.get("doi") or ""
    doi = doi_url.replace("https://doi.org/", "") if doi_url else ""

    # URL
    url = work.get("doi") or ""
    if not url:
        # Try landing page
        loc = work.get("primary_location") or {}
        url = loc.get("landing_page_url") or ""

    return {
        "title": title,
        "authors": authors,
        "year": year,
        "venue": venue,
        "abstract": abstract,
        "doi": doi,
        "url": url,
        "source": "openalex",
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch papers from OpenAlex API.")
    parser.add_argument("--output", default="data/raw-search/openalex_raw.csv")
    parser.add_argument("--max-results", type=int, default=200,
                        help="Max results per query (default 200)")
    parser.add_argument("--year-from", type=int, default=2021,
                        help="Start year filter (default 2021)")
    args = parser.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    all_papers: dict[str, dict] = {}

    for i, q in enumerate(QUERIES):
        print(f"[{i+1}/{len(QUERIES)}] {q}")
        raw = fetch_openalex(q, max_results=args.max_results, year_from=args.year_from)
        for work in raw:
            norm = normalize(work)
            if not norm["title"]:
                continue
            key = norm["doi"] or norm["url"] or norm["title"].lower()
            if key not in all_papers:
                all_papers[key] = norm
        print(f"  -> {len(raw)} results ({len(all_papers)} unique so far)")
        time.sleep(0.5)

    print(f"\nTotal unique papers: {len(all_papers)}")

    fields = ["title", "authors", "year", "venue", "abstract", "doi", "url", "source"]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in sorted(all_papers.values(), key=lambda r: r["year"], reverse=True):
            writer.writerow(row)

    print(f"Wrote {len(all_papers)} records to {out_path}")


if __name__ == "__main__":
    main()
