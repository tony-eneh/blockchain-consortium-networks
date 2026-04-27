# Systematic Review + Reference Implementation TODO

Topic: **Blockchain utilization strategies between institutions (consortium/inter-institutional networks)**

Standards: **PRISMA 2020**, **PRISMA-S** (search reporting), plus reproducibility artifact package.

## Ordered execution plan

1. **Define review questions (PICOC-framed)** — `DONE`
   - Locked 4 technical research questions.
   - Scope frozen to institutional consortium / inter-organizational settings.

2. **Write protocol (PRISMA)** — `DONE (draft)`
   - Inclusion/exclusion criteria defined.
   - Outcomes, variables, quality dimensions, and synthesis plan drafted.
   - OSF registration still pending.

3. **Build search strings and source list** — `DONE`
   - Final operational sources used in repo: IEEE Xplore, Web of Science, arXiv API, OpenAlex API.
   - ACM DL and Scopus were planned originally but not used because of export/search access constraints.

4. **Run search and deduplicate** — `DONE`
   - Raw records identified: **1,707**.
   - Unique records after deduplication: **1,638**.
   - Artifact snapshot:
     - `data/raw-search/*.csv`
     - `data/processed/master_dedup.csv`
     - `data/reports/dedup_report.md`

5. **Screen studies (2-stage)** — `IN PROGRESS (agent pass complete)`
   - Title/abstract screening completed as first-pass triage on all **1,638** records.
   - First-pass title/abstract decisions:
     - `INCLUDE`: **571**
     - `EXCLUDE`: **775**
     - `UNCERTAIN`: **292**
   - Uncertain queue resolved by agent-driven workflow: **143 include / 149 exclude**.
   - Agent full-text review of the **571** first-pass includes: **136 include / 435 exclude** (in-memory PDF + HTML extraction; conservative `needs_human_check` and unreachable papers excluded).
   - **Current full-text screening totals across the 863-candidate pool: `include = 279`, `exclude = 584`.**
   - Dominant agent exclusion reason: no open-access full text (491 records). Other buckets: triage exclude (48), agent borderline (34), protocol fail (11).
   - Immediate next work:
     - Author-level confirmation of the 279 agent includes (sampling-based spot-check is sufficient for this iteration).
     - Procure full-text for the 491 paywalled rows where institutional access is available, then re-run the reviewer.
     - Begin populating `data/processed/data_extraction.csv` for the 279 included studies.
   - Current operational artifacts:
     - `data/processed/fulltext_screening.csv` (single source of truth)
     - `data/processed/firstpass_fulltext_review.csv`
     - `data/processed/accessible_fulltext_review.csv`
     - `data/processed/ambiguous_review_priority.csv`
     - `data/processed/uncertain_likely_include.csv`, `uncertain_likely_exclude.csv`, `uncertain_needs_manual.csv`, `uncertain_needs_manual_fulltext.csv`
     - `data/reports/review_artifact_report.md`
     - `data/reports/uncertain_second_pass_report.md`
     - `data/reports/ambiguous_fulltext_discovery_report.md`
     - `data/reports/ambiguous_review_priority_report.md`
     - `data/reports/accessible_fulltext_review_report.md`
     - `data/reports/uncertain_finalization_report.md`
     - `data/reports/firstpass_fulltext_review_report.md`
     - `paper/figures/prisma_flow.tex` (auto-generated PRISMA 2020 flow figure)md`
     - `paper/figures/prisma_flow.tex` (auto-generated PRISMA 2020 flow figure)

6. **Extract technical data** — `BOOTSTRAPPED (Week 9)`
    - Extraction sheet generated for the full 863-candidate scaffold; per-include sheet generated for the 279 final includes with abstract-only heuristic seeds for 7 of 37 fields (504 auto-filled cells, all `[auto] `-prefixed).
    - Heuristic taxonomy signal so far: 159 IoT/edge, 105 healthcare, 69 supply-chain, 49 Fabric, 32 Ethereum, 12 PBFT.
    - Current artifacts:
       - `data/processed/data_extraction.csv` (863-row scaffold)
       - `data/processed/data_extraction_includes.csv` (**NEW** — 279 includes + bootstrap)
       - `data/reports/data_extraction_bootstrap_report.md`
    - Next: full-text rubric pass on tier-A/B (148 papers) to fill the remaining 30 fields.

7. **Quality assessment** — `RUBRIC LIVE (Week 9)`
   - Screening-stage rubric (4 PRISMA dimensions × 0–2, total 0–8) implemented and applied to the 279 final includes.
   - Tier distribution: **A 26 / B 122 / C 110 / D 21**. 148/279 (53%) score B or higher → priority queue for the deep-read pass.
   - Current artifacts:
       - `scripts/quality_assessment.py`
       - `data/processed/quality_assessment.csv`
       - `data/reports/quality_assessment_report.md`
   - Companion spot-check sampler: 40 stratified rows (20 includes × tier + 20 excludes × reason), seed `20260428`.
       - `scripts/sample_spotcheck.py`
       - `data/processed/spotcheck_sample.csv`
       - `data/reports/spotcheck_sample_report.md`
   - Next: complete author spot-check audit; replace abstract-only scores with full-text scores on tier-A/B.

8. **Synthesize evidence** — `NOT STARTED`
   - Taxonomy, evidence tables, and gap map depend on extracted full-text dataset.

9. **Design reference implementation** — `NOT STARTED`
   - Defer until synthesis identifies dominant strategy gaps and benchmark targets.

10. **Implement prototype** — `NOT STARTED`
    - Waiting on reference architecture definition.

11. **Run experiments** — `NOT STARTED`
    - Waiting on prototype implementation.

12. **Write paper + artifact package** — `IN PROGRESS`
    - Intro/method/results skeleton exists in `paper/main.tex`.
    - Search execution and preliminary screening numbers should be kept synchronized with repo artifacts.
    - PRISMA flow diagram, final results tables, discussion, and conclusion remain incomplete.

## Immediate next actions
1. Reviewer fills `human_decision` in `data/processed/spotcheck_sample.csv` (40 rows) and we compute the agent-vs-human agreement rate.
2. Full-text rubric pass on the 148 tier-A/B includes (replaces the abstract-only screening scores in `data/processed/quality_assessment.csv`).
3. Extraction deep-fill on the 26 tier-A papers — populate the 30 non-bootstrapped extraction fields.
4. Procure full-text for the 491 paywalled candidates and re-run `scripts/review_firstpass_fulltexts.py`.
5. Begin Step 8 synthesis: taxonomy tables grouped by domain × platform × consensus once tier-A extractions are complete.

## Current evidence snapshot

- Search date used in current artifacts: **2026-04-14**.
- Source counts:
  - IEEE Xplore: **386**
  - Web of Science: **50**
  - arXiv: **49**
  - OpenAlex: **1,222**
- Dedup removed: **69** (`40` DOI matches, `29` title+year matches).
- Screening report: `data/reports/screening_report.md`.

## Deliverable discipline
- Every stage ends with a versioned artifact.
- No claims without traceable evidence (paper/source/experiment log).
- Keep scripts/configs deterministic where possible.
