# 03 - Search Strings (PRISMA-S Draft)

## Databases
- IEEE Xplore
- Web of Science Core Collection
- arXiv (via API — `scripts/fetch_arxiv.py`)
- Semantic Scholar → **dropped** (API rate-limited without key)
- **OpenAlex** (via API — `scripts/fetch_openalex.py`, replaces ACM DL + Scopus)

### Source substitution note
ACM Digital Library and Scopus were originally planned but dropped due to access
constraints (ACM requires premium for CSV export; Scopus requires institutional
subscription). Semantic Scholar API was attempted but rate-limited without an API key.
**OpenAlex** (free, open, indexes ~250M works including ACM and Elsevier/Scopus venues)
is used as a replacement source to maintain coverage.

## Query design blocks
- **B1 (technology):** "consortium blockchain" OR "permissioned blockchain" OR "enterprise blockchain" OR "distributed ledger"
- **B2 (institutional setting):** institution* OR "inter-organizational" OR "cross-organizational" OR interbank OR "multi-party"
- **B3 (strategy dimensions):** governance OR consensus OR privacy OR confidentiality OR interoperability OR "cross-chain"
- **B4 (technical evidence):** implement* OR prototype OR benchmark OR evaluation OR experiment*

## Master query (generic)
("consortium blockchain" OR "permissioned blockchain" OR "enterprise blockchain" OR "distributed ledger")
AND
(institution* OR "inter-organizational" OR "cross-organizational" OR interbank OR "multi-party")
AND
(governance OR consensus OR privacy OR confidentiality OR interoperability OR "cross-chain")
AND
(implement* OR prototype OR benchmark OR evaluation OR experiment*)

## Database-specific query variants

### IEEE Xplore
("All Metadata":"consortium blockchain" OR "All Metadata":"permissioned blockchain" OR "All Metadata":"enterprise blockchain" OR "All Metadata":"distributed ledger")
AND
("All Metadata":institution* OR "All Metadata":"inter-organizational" OR "All Metadata":"cross-organizational" OR "All Metadata":interbank OR "All Metadata":"multi-party")
AND
("All Metadata":governance OR "All Metadata":consensus OR "All Metadata":privacy OR "All Metadata":confidentiality OR "All Metadata":interoperability OR "All Metadata":"cross-chain")
AND
("All Metadata":implement* OR "All Metadata":prototype OR "All Metadata":benchmark OR "All Metadata":evaluation OR "All Metadata":experiment*)

### ACM Digital Library
(acmdlTitle:("consortium blockchain" OR "permissioned blockchain" OR "enterprise blockchain" OR "distributed ledger")
OR recordAbstract:("consortium blockchain" OR "permissioned blockchain" OR "enterprise blockchain" OR "distributed ledger"))
AND (institution* OR "inter-organizational" OR "cross-organizational" OR interbank OR "multi-party")
AND (governance OR consensus OR privacy OR confidentiality OR interoperability OR "cross-chain")
AND (implement* OR prototype OR benchmark OR evaluation OR experiment*)

### Scopus
TITLE-ABS-KEY(("consortium blockchain" OR "permissioned blockchain" OR "enterprise blockchain" OR "distributed ledger")
AND (institution* OR "inter-organizational" OR "cross-organizational" OR interbank OR "multi-party")
AND (governance OR consensus OR privacy OR confidentiality OR interoperability OR "cross-chain")
AND (implement* OR prototype OR benchmark OR evaluation OR experiment*))

### Web of Science
TS=(("consortium blockchain" OR "permissioned blockchain" OR "enterprise blockchain" OR "distributed ledger")
AND (institution* OR "inter-organizational" OR "cross-organizational" OR interbank OR "multi-party")
AND (governance OR consensus OR privacy OR confidentiality OR interoperability OR "cross-chain")
AND (implement* OR prototype OR benchmark OR evaluation OR experiment*))

### arXiv (via API)
arXiv's web search cannot handle complex Boolean queries.
We use the official Atom API (`scripts/fetch_arxiv.py`) with multiple focused
sub-queries covering technology × setting × strategy combinations. See script
for the full query list. Date filter: 2021–present.

### Semantic Scholar (dropped)
API rate-limited without an API key. Replaced by OpenAlex.

### OpenAlex (via API)
OpenAlex's Works API (`scripts/fetch_openalex.py`) is queried with keyword
combinations covering the same conceptual blocks. It indexes ACM, Springer,
Elsevier, IEEE, and other venues (~250M works). Date filter: 2021–present.

## Pilot/refinement protocol
1. Run each query and collect top 100 results by relevance/date.
2. Measure precision proxy: fraction of clearly in-scope papers in first 50.
3. Inspect false positives and add exclusion terms only if needed:
   - "cryptocurrency price prediction"
   - "token price"
   - "NFT marketplace"
4. Validate recall proxy with seed papers from related-work anchors.
5. Freeze final query set and timestamp it in protocol registration.

## Export requirements
- Export full metadata: title, authors, year, venue, abstract, DOI, URL, index source.
- Include search date and exact query string per source.
- Keep one raw export file per source before deduplication.
