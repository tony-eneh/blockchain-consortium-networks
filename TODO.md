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

6. **Extract technical data** — `READY TO START`
    - Extraction sheet has been generated for the 863 candidate studies.
    - Current artifact:
       - `data/processed/data_extraction.csv`
    - Fields cover architecture, consensus, governance, privacy, interoperability, metrics, workload, reproducibility, and quality notes.

7. **Quality assessment** — `NOT STARTED`
   - Need explicit scoring rubric and thresholds.
   - Apply after full-text inclusion list is stable.

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
Begin Step 6 (data extraction) on the 279 agent-included studies.
2. Apply Step 7 (quality assessment rubric) to the same 279.
3. Author-level spot-check of agent decisions (sample include + exclude buckets).
4. Procure full-text for the 491 paywalled candidates and re-run the agent reviewer.
5. Refresh weekly slides with Week-8es and re-run the agent reviewer.
5. Refresh weekly slides with Week-8 totals.

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
