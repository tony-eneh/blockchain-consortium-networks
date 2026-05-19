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

5. **Screen studies (2-stage)** — `IN PROGRESS (agent pass complete; human validation pending)`
   - Title/abstract screening completed as first-pass triage on all **1,638** records.
   - First-pass title/abstract decisions:
     - `INCLUDE`: **571**
     - `EXCLUDE`: **775**
     - `UNCERTAIN`: **292**
   - Uncertain queue resolved by agent-driven workflow: **143 include / 149 exclude**.
   - Agent full-text review of the **571** first-pass includes: **136 include / 435 exclude** (in-memory PDF + HTML extraction; conservative `needs_human_check` and unreachable papers excluded).
   - **Current full-text screening totals across the 863-candidate pool: `include = 279`, `exclude = 584`.**
   - Dominant agent exclusion bucket: inaccessible or insufficient full text (**491 records total**: 281 `insufficient_fulltext_depth` + 210 `no_full_text_access`). Other top buckets: `second_pass_likely_exclude` (48), `agent_uncertain_full_text` (32), and low-frequency protocol/evidence-fail reasons.
   - Publication caveat: agent-assisted screening must be presented as triage until author spot-check/adjudication is complete.
   - Immediate next work:
     - Author-level confirmation of the 279 agent includes (sampling-based spot-check is sufficient for this iteration).
     - Procure full text for inaccessible/insufficient-access rows where institutional access is available, then re-run the reviewer.
     - Continue deep extraction for the 279 included studies, prioritizing Tier A/B records.
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
     - `paper/figures/prisma_flow.tex` (auto-generated PRISMA 2020 flow figure)

6. **Extract technical data** — `BOOTSTRAPPED + PARTIAL FULL-TEXT EXTRACTION`
   - Extraction sheet generated for the full 863-candidate scaffold; per-include sheet generated for the 279 final includes with abstract-only heuristic seeds for 7 of 37 fields (504 auto-filled cells, all `[auto] `-prefixed).
   - Current synthesis extraction coverage: **95 / 279 studies have `[ft]` full-text fills**; **184 / 279 remain abstract-only `[auto]` signals**.
   - Current taxonomy signals from synthesis artifacts: healthcare (143), supply chain (124), government/public sector (123), finance/banking (103); Ethereum (81), Hyperledger Fabric (80), Bitcoin (55); PoW (55), PBFT (42), BFT-general (41), PoS (39), RAFT (24).
   - Current artifacts:
       - `data/processed/data_extraction.csv` (863-row scaffold)
       - `data/processed/data_extraction_includes.csv` (**NEW** — 279 includes + bootstrap)
       - `data/reports/data_extraction_bootstrap_report.md`
   - Next: full-text rubric pass on tier-A/B (148 papers), manual verification of metric captures, and deep-fill of missing fields for Tier A studies.

7. **Quality assessment** — `SCREENING-STAGE RUBRIC LIVE`
   - Screening-stage rubric (4 PRISMA dimensions × 0–2, total 0–8) implemented and applied to the 279 final includes.
   - Tier distribution: **A 26 / B 122 / C 110 / D 21**. 148/279 (53%) score B or higher → priority queue for the deep-read pass.
   - Caveat: current quality tiers are title/abstract/source-derived triage signals, not final full-text quality scores.
   - Current artifacts:
       - `scripts/quality_assessment.py`
       - `data/processed/quality_assessment.csv`
       - `data/reports/quality_assessment_report.md`
   - Companion spot-check sampler: 40 stratified rows (20 includes × tier + 20 excludes × reason), seed `20260428`.
       - `scripts/sample_spotcheck.py`
       - `data/processed/spotcheck_sample.csv`
       - `data/reports/spotcheck_sample_report.md`
   - Next: complete author spot-check audit; replace abstract-only scores with full-text scores on tier-A/B.

8. **Synthesize evidence** — `BOOTSTRAPPED (VERIFY BEFORE PUBLICATION)`
   - Synthesis CSVs are populated from the 279 included-study set:
      - `data/processed/synthesis_rq1_taxonomy.csv` — 279 rows
      - `data/processed/synthesis_rq2_tradeoffs.csv` — 279 rows
      - `data/processed/synthesis_rq3_interop.csv` — 295 rows (one row per detected pattern; multi-label)
      - `data/processed/synthesis_rq4_gaps.csv` — 279 rows
      - `data/processed/synthesis_domain_platform.csv`
      - `data/reports/synthesis_report.md`
   - Current key signals: throughput reported in 23/279 (8%), latency in 33/279 (11%), fault tolerance in 48/279 (17%), evaluation setup in 80/279 (28%); code artifacts in 35/279 (12%), config/deployment in 18/279 (6%), datasets in 6/279 (2%).
   - Caveat: throughput/latency values were captured heuristically from available text and need unit/context verification before being cited as empirical ranges.

9. **Design reference implementation** — `NOT STARTED`
   - Defer until synthesis identifies dominant strategy gaps and benchmark targets.

10. **Implement prototype** — `NOT STARTED`
    - Waiting on reference architecture definition.

11. **Run experiments** — `NOT STARTED`
    - Waiting on prototype implementation.

12. **Write paper + artifact package** — `IN PROGRESS (draft compiled; claims need tightening)`
   - Manuscript exists in `paper/paper.tex`; compiled PDF exists in `paper/paper.pdf`.
   - Search execution and screening numbers are synchronized with current artifacts, but wording should distinguish completed artifact counts from provisional author-validated counts.
   - PRISMA flow diagram exists at `paper/figures/prisma_flow.tex` and is auto-generated from `data/processed/fulltext_screening.csv`.
   - Results, Discussion, and Conclusion are drafted, but should be revised to frame agent-assisted outputs and abstract-only synthesis as provisional until human validation and full-text rescoring are complete.
   - Known formatting issue: LaTeX build log reports overfull boxes around dense Results tables; shorten or move detailed taxonomy/trade-off tables to appendix before submission.

## Immediate next actions
1. Reviewer fills `human_decision` in `data/processed/spotcheck_sample.csv` (40 rows) and we compute the agent-vs-human agreement rate.
2. Full-text rubric pass on the 148 tier-A/B includes (replaces the abstract-only screening scores in `data/processed/quality_assessment.csv`).
3. Extraction deep-fill on the 26 tier-A papers — populate the 30 non-bootstrapped extraction fields.
4. Manually verify throughput/latency/fault-tolerance metric captures in `data/processed/synthesis_rq2_tradeoffs.csv` before citing numeric ranges in the paper.
5. Procure full text for inaccessible/insufficient-access candidates where institutional access is available, then re-run `scripts/review_firstpass_fulltexts.py` or record them as unavailable with bias discussion.
6. Revise `paper/paper.tex` so the main claims match the current evidence level: agent-assisted triage, 95 full-text extractions, 184 abstract-only signals, screening-stage quality tiers, and OpenAlex substitution for ACM/Scopus.
7. Add/strengthen a protocol-deviation and limitations paragraph covering OpenAlex substitution, open-access bias, missing human adjudication, and heuristic extraction.

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
