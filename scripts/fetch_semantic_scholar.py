#!/usr/bin/env python3
"""Fetch papers from Semantic Scholar API as a substitute for ACM DL and Scopus.

Semantic Scholar is free, requires no subscription, and indexes ACM, Springer,
Elsevier, and most CS venues — making it a solid replacement when ACM/Scopus
exports are blocked by paywalls.

Usage:
    python scripts/fetch_semantic_scholar.py --output data/raw-search/s2_raw.csv --max-results 500

Rate limit: 100 requests/5 min without API key. Script auto-throttles.
"""

import argparse
import csv
import json
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

S2_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"

# Search queries — Semantic Scholar supports simple keyword search.
# Kept to a minimal set to avoid rate limits (100 req / 5 min without API key).
QUERIES = [
    "consortium blockchain governance",
    "permissioned blockchain interoperability",
    "enterprise blockchain privacy evaluation",
    "Hyperledger Fabric consortium benchmark",
    "blockchain cross-chain institutional",
]

FIELDS = "title,authors,year,venue,abstract,externalIds,url"


def fetch_s2(query: str, max_results: int = 100, year_range: str = "2021-") -> list[dict]:
    """Return papers from Semantic Scholar for a single query."""
    papers = []
    offset = 0
    limit = min(max_results, 100)  # API max per page is 100
    retries = 0
    max_retries = 3

    while offset < max_results:
        params = urlencode({
            "query": query,
            "offset": offset,
            "limit": limit,
            "fields": FIELDS,
            "year": year_range,
        })
        url = f"{S2_SEARCH}?{params}"
        req = Request(url, headers={"User-Agent": "SLR-Search-Bot/1.0"})

        try:
            with urlopen(req) as resp:
                body = json.loads(resp.read())
            retries = 0  # Reset on success
        except HTTPError as e:
            if e.code == 429:
                retries += 1
                if retries > max_retries:
                    print(f"    Giving up after {max_retries} rate-limit retries")
                    break
                wait = 30 * retries
                print(f"    Rate limited, waiting {wait}s (attempt {retries}/{max_retries})...")
                time.sleep(wait)
                continue
            raise

        batch = body.get("data", [])
        if not batch:
            break
        papers.extend(batch)
        offset += len(batch)

        total = body.get("total", 0)
        if offset >= total:
            break

        time.sleep(3.5)  # Polite delay — stay under 100 req / 5 min

    return papers


def normalize(paper: dict) -> dict:
    """Convert S2 paper object to our standard CSV schema."""
    ext_ids = paper.get("externalIds") or {}
    doi = ext_ids.get("DOI", "")
    arxiv_id = ext_ids.get("ArXiv", "")

    authors_list = paper.get("authors") or []
    authors = "; ".join(a.get("name", "") for a in authors_list)

    url = paper.get("url", "")
    if not url and doi:
        url = f"https://doi.org/{doi}"

    return {
        "title": (paper.get("title") or "").strip(),
        "authors": authors,
        "year": str(paper.get("year") or ""),
        "venue": (paper.get("venue") or "").strip(),
        "abstract": (paper.get("abstract") or "").strip(),
        "doi": doi,
        "url": url,
        "source": "semantic_scholar",
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch papers from Semantic Scholar API.")
    parser.add_argument("--output", default="data/raw-search/s2_raw.csv")
    parser.add_argument("--max-results", type=int, default=100,
                        help="Max results per query (default 100)")
    parser.add_argument("--year-from", default="2021",
                        help="Start year filter (default 2021)")
    args = parser.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    year_range = f"{args.year_from}-"
    all_papers: dict[str, dict] = {}

    for i, q in enumerate(QUERIES):
        print(f"[{i+1}/{len(QUERIES)}] {q}")
        raw = fetch_s2(q, max_results=args.max_results, year_range=year_range)
        for p in raw:
            norm = normalize(p)
            if not norm["title"]:
                continue
            # Dedup key: DOI > URL > lowercase title
            key = norm["doi"] or norm["url"] or norm["title"].lower()
            if key not in all_papers:
                all_papers[key] = norm
        print(f"  -> {len(raw)} results ({len(all_papers)} unique so far)")
        time.sleep(2)

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
