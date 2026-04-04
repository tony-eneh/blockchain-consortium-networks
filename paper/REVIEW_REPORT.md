# REVIEW_REPORT.md

## Summary
Drafted the empty Results, Discussion, and Conclusion sections for the paper **"Systematic Review of Blockchain Utilization Strategies in Institutional Consortium Networks"** and updated supporting metadata/citations.

## Changes Made

### 1. `main.tex`
- Replaced the author email TODO with `anthony@kumoh.ac.kr`
- Completed the abstract ending with:
  - provisional PRISMA counts
  - dominant platforms/domains
  - key findings on trade-offs and interoperability
- Wrote **Section 4: Results** with draft content for:
  - 4.1 Study Selection
  - 4.2 Study Characteristics
  - 4.3 RQ1 Taxonomy of Blockchain Utilization Strategies
  - 4.4 RQ2 Empirical Trade-Offs
  - 4.5 RQ3 Interoperability Patterns
  - 4.6 RQ4 Gaps and Reference Implementation Requirements
- Added draft tables/figures:
  - textual PRISMA flow placeholder figure
  - aggregate study characteristics table
  - taxonomy table
  - trade-off comparison table
- Wrote **Section 5: Discussion** (~500 words) covering:
  - synthesis of findings
  - practitioner implications
  - comparison with prior surveys
  - limitations / threats to validity
- Wrote **Section 6: Conclusion** (~200 words)
- Marked all newly drafted content with `%% [DRAFT - VERIFY]`
- Simplified the author block to a safer IEEEtran-compatible inline form
- Fixed citation key usage from Unicode form to `olnes2017blockchain`

### 2. `references.bib`
- Expanded bibliography substantially with additional entries relevant to:
  - consortium blockchain architectures
  - benchmarking/performance
  - governance
  - privacy/confidential computing
  - interoperability
  - domain applications
- Added more than 15 new references beyond the initial file contents
- Marked uncertain bibliography items with `%% [DRAFT - VERIFY]`

### 3. `REVIEW_REPORT.md`
- Created this change log file as requested

## Important Notes for Final Verification
- PRISMA counts are explicitly **draft placeholders** and must be reconciled with the actual screening spreadsheet/log
- Some bibliography metadata is intentionally flagged for verification before submission, especially:
  - `thomas2023interop`
  - `milosevic2018unibright`
- LaTeX compilation was **not** verified in-session because `pdflatex`/`bibtex` were not available in the environment
- Other pre-existing TODOs in Background/Methodology remain unchanged

## Suggested Next Checks
1. Verify final screening counts and exclusion reasons
2. Confirm all citation metadata in `references.bib`
3. Compile the paper and fix any formatting/overflow issues in tables
4. Optionally replace the textual PRISMA placeholder with a proper PRISMA diagram figure
