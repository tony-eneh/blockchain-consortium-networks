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

5. **Screen studies (2-stage)** — `IN PROGRESS`
   - Title/abstract screening completed as first-pass triage on all **1,638** records.
   - First-pass title/abstract decisions:
     - `INCLUDE`: **571**
     - `EXCLUDE`: **775**
     - `UNCERTAIN`: **292**
   - Uncertain queue fully resolved by agent-driven workflow (no manual backlog):
     - Second-pass triage → `likely_include` **123**, `likely_exclude` **48**, `needs_manual` **121**.
     - Open-access discovery on the 121 needs\_manual rows → **15** PDFs downloaded, **38** open landing/PDF links resolved, **68** paywalled (no open full-text).
     - Agent full-text review of the 53 accessible papers → `include` **20**, `exclude` **1**, `needs_human_check` **32** (conservatively excluded).
     - Finalisation → uncertain partition: **143 include / 149 exclude** (rules in `data/reports/uncertain_finalization_report.md`).
   - Effective candidate pool for author-level full-text screening: **714** records (`571 first-pass include + 143 promoted from uncertain`).
   - Immediate next work:
     - Author-level full-text screening of the 714 candidates (especially the 571 first-pass includes whose `fulltext_status` is still `pending`).
     - Spot-check the 32 agent `needs_human_check` and the 68 paywalled exclusions before locking the PRISMA flow.
     - Record full-text exclusion reasons for PRISMA flow.
   - Current operational artifacts:
     - `data/processed/fulltext_screening.csv`
     - `data/processed/accessible_fulltext_review.csv`
     - `data/processed/ambiguous_review_priority.csv`
     - `data/processed/uncertain_likely_include.csv`, `uncertain_likely_exclude.csv`, `uncertain_needs_manual.csv`, `uncertain_needs_manual_fulltext.csv`
     - `data/reports/review_artifact_report.md`
     - `data/reports/uncertain_second_pass_report.md`
     - `data/reports/ambiguous_fulltext_discovery_report.md`
     - `data/reports/ambiguous_review_priority_report.md`
     - `data/reports/accessible_fulltext_review_report.md`
     - `data/reports/uncertain_finalization_report.md`

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

1. Author-level full-text screening of the **714** candidate pool (priority on the 571 first-pass includes still in `fulltext_status = pending`).
2. Spot-check the agent finalisation: 32 `needs_human_check` exclusions and 68 paywalled exclusions for false negatives.
3. Continue filling `data/processed/data_extraction.csv` for confirmed includes.
4. Update `paper/main.tex` PRISMA flow figure with the finalised uncertain numbers (143 include / 149 exclude) and the new 714-record candidate pool.
5. Refresh weekly slides with the updated screening totals.

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
