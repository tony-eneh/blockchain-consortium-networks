#!/usr/bin/env python3
"""Fetch arXiv papers via the official API and export to CSV.

Usage:
    python scripts/fetch_arxiv.py --output data/raw-search/arxiv_raw.csv --max-results 200

The query is intentionally simplified (arXiv API handles Boolean poorly with
long phrases) and split into multiple sub-queries to maximise recall.
"""

import argparse
import csv
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

ARXIV_API = "http://export.arxiv.org/api/query"

# Sub-queries designed for arXiv's limited Boolean support.
# We combine technology + setting terms, keeping them short.
QUERIES = [
    'all:"consortium blockchain" AND all:governance',
    'all:"consortium blockchain" AND all:consensus',
    'all:"consortium blockchain" AND all:privacy',
    'all:"consortium blockchain" AND all:interoperability',
    'all:"permissioned blockchain" AND all:institution',
    'all:"permissioned blockchain" AND all:consortium',
    'all:"permissioned blockchain" AND all:interoperability',
    'all:"enterprise blockchain" AND all:consortium',
    'all:"enterprise blockchain" AND all:governance',
    'all:"distributed ledger" AND all:consortium AND all:governance',
    'all:"distributed ledger" AND all:interbank',
    'all:"Hyperledger Fabric" AND all:consortium AND all:evaluation',
    'all:"Hyperledger Fabric" AND all:interoperability',
    'all:blockchain AND all:"cross-chain" AND all:institution',
    'all:blockchain AND all:"cross-chain" AND all:consortium',
]

NS = {"atom": "http://www.w3.org/2005/Atom"}


def fetch_query(query: str, max_results: int = 100) -> list[dict]:
    """Return list of paper dicts for a single arXiv API query."""
    params = urlencode({
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    })
    url = f"{ARXIV_API}?{params}"
    with urlopen(url) as resp:
        data = resp.read()

    root = ET.fromstring(data)
    results = []
    for entry in root.findall("atom:entry", NS):
        title_el = entry.find("atom:title", NS)
        summary_el = entry.find("atom:summary", NS)
        published_el = entry.find("atom:published", NS)
        id_el = entry.find("atom:id", NS)

        authors = []
        for author in entry.findall("atom:author", NS):
            name = author.find("atom:name", NS)
            if name is not None and name.text:
                authors.append(name.text.strip())

        title = re.sub(r"\s+", " ", (title_el.text or "").strip()) if title_el is not None else ""
        abstract = re.sub(r"\s+", " ", (summary_el.text or "").strip()) if summary_el is not None else ""
        year = (published_el.text or "")[:4] if published_el is not None else ""
        arxiv_url = (id_el.text or "").strip() if id_el is not None else ""

        # Extract arXiv ID for DOI-like reference
        arxiv_id = arxiv_url.split("/abs/")[-1] if "/abs/" in arxiv_url else ""

        if not title:
            continue

        results.append({
            "title": title,
            "authors": "; ".join(authors),
            "year": year,
            "venue": "arXiv",
            "abstract": abstract,
            "doi": f"10.48550/arXiv.{arxiv_id}" if arxiv_id else "",
            "url": arxiv_url,
            "source": "arxiv",
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch arXiv papers for systematic review.")
    parser.add_argument("--output", default="data/raw-search/arxiv_raw.csv")
    parser.add_argument("--max-results", type=int, default=100,
                        help="Max results per sub-query (default 100)")
    args = parser.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    all_papers: dict[str, dict] = {}  # keyed by URL to dedup across sub-queries

    for i, q in enumerate(QUERIES):
        print(f"[{i+1}/{len(QUERIES)}] {q}")
        papers = fetch_query(q, max_results=args.max_results)
        for p in papers:
            key = p["url"] or p["title"].lower()
            if key not in all_papers:
                all_papers[key] = p
        print(f"  -> {len(papers)} results ({len(all_papers)} unique so far)")
        time.sleep(3)  # Be polite to arXiv API (rate limit: 1 req / 3 sec)

    # Filter to 2021+
    filtered = [p for p in all_papers.values() if p["year"] >= "2021"]
    print(f"\nTotal unique: {len(all_papers)}, after 2021+ filter: {len(filtered)}")

    fields = ["title", "authors", "year", "venue", "abstract", "doi", "url", "source"]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in sorted(filtered, key=lambda r: r["year"], reverse=True):
            writer.writerow(row)

    print(f"Wrote {len(filtered)} records to {out_path}")


if __name__ == "__main__":
    main()
