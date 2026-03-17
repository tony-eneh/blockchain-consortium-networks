# 03 - Search Strings (PRISMA-S Draft)

## Databases
- IEEE Xplore
- ACM Digital Library
- Scopus
- Web of Science Core Collection
- arXiv

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

### arXiv
("consortium blockchain" OR "permissioned blockchain" OR "enterprise blockchain" OR "distributed ledger")
AND
(institution OR interbank OR consortium OR "cross-organizational" OR "multi-party")
AND
(governance OR consensus OR privacy OR interoperability OR "cross-chain")
AND
(implementation OR prototype OR benchmark OR evaluation OR experiment)

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
