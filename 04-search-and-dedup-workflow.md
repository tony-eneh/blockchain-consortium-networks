# 04 - Search and Dedup Workflow

## Goal
Run database searches using the frozen queries, export records, and produce a deduplicated master corpus with an audit trail.

## Folder conventions
- Raw exports: `data/raw-search/`
- Deduped outputs: `data/processed/`
- Logs/reports: `data/reports/`

## Required export fields (per source)
- `title`
- `authors`
- `year`
- `venue`
- `abstract`
- `doi`
- `url`
- `source` (ieee/acm/scopus/wos/arxiv)

## File naming
- `data/raw-search/<source>_raw.csv`
  - Example: `ieee_raw.csv`, `acm_raw.csv`, `scopus_raw.csv`

## Execution
1. Run each source query from `03-search-strings.md`.
2. Export one CSV per source into `data/raw-search/`.
3. Run:
   - `python3 scripts/dedup_records.py --input-dir data/raw-search --output-dir data/processed --report-dir data/reports`
4. Review:
   - `data/processed/master_dedup.csv`
   - `data/reports/dedup_report.md`
5. Freeze snapshot by committing raw + processed + report artifacts together.

## Dedup logic (script)
Priority key order:
1. DOI exact match
2. URL exact match
3. Normalized title + year

## PRISMA flow counters to capture
- Records identified (all sources combined)
- Records after duplicates removed
- Records screened (title/abstract)
- Full-text assessed (filled in next stage)

## Notes
- Do not overwrite prior snapshots; use versioned commits.
- Keep raw exports unchanged after ingestion.
