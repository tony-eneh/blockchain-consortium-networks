# Blockchain Utilization Strategies in Institutional Consortium Networks

A PRISMA 2020 systematic review of blockchain utilization strategies for institutional consortium networks — covering architecture, governance, consensus, privacy, and interoperability dimensions.

**Affiliation:** Networked Systems Laboratory (NSL), Kumoh National Institute of Technology (KIT), Gumi, South Korea
**Project:** Purecertificate

## Research Questions

| # | Question |
|---|---------|
| RQ1 | Which blockchain utilization strategies are reported for institutional consortium workflows, and how can they be taxonomized across architecture, governance, consensus, and privacy dimensions? |
| RQ2 | What empirical evidence exists on trade-offs among performance, resilience, privacy, and operational complexity for these strategies? |
| RQ3 | Which interoperability patterns (cross-chain, API-mediated, bridge/oracle, messaging/event-driven) are most effective in institutional settings, and under what constraints? |
| RQ4 | What design gaps and reproducibility weaknesses remain, and how should a reference implementation be structured to address them? |

## Scope

- **Population:** Institutional multi-party workflows and consortium networks (inter-bank, inter-agency, B2B regulated collaboration).
- **Intervention:** Blockchain utilization strategies (platform choice, consensus, governance model, privacy layer, interoperability approach).
- **Comparison:** Alternative strategy choices, non-blockchain baselines where reported, and cross-platform implementations.
- **Outcomes:** Throughput, latency, finality, fault tolerance, privacy/security guarantees, interoperability performance, operational overhead, and maintainability.
- **Context:** Regulated or compliance-sensitive settings with multi-organization trust boundaries.

## Repository Structure

```
├── 01-rqs-scope.md              # Research questions and PICOC scope
├── 02-prisma-protocol-draft.md  # PRISMA protocol (eligibility, extraction, synthesis)
├── 03-search-strings.md         # Database-specific search queries (PRISMA-S)
├── 04-search-and-dedup-workflow.md  # Search execution and deduplication workflow
├── TODO.md                      # Ordered execution plan
├── data/
│   ├── raw-search/              # Raw CSV exports per database
│   ├── processed/               # Deduplicated master corpus
│   └── reports/                 # Dedup reports and PRISMA flow counts
└── scripts/
    └── dedup_records.py         # Record deduplication script
```

## Databases

- IEEE Xplore
- ACM Digital Library
- Scopus
- Web of Science Core Collection
- arXiv

## Workflow

1. **Define** research questions and scope ([01-rqs-scope.md](01-rqs-scope.md))
2. **Draft** PRISMA protocol ([02-prisma-protocol-draft.md](02-prisma-protocol-draft.md))
3. **Build** search strings per database ([03-search-strings.md](03-search-strings.md))
4. **Run** searches and deduplicate records ([04-search-and-dedup-workflow.md](04-search-and-dedup-workflow.md))
5. **Screen** studies (title/abstract → full-text)
6. **Extract** technical data and assess quality
7. **Synthesize** taxonomy, evidence tables, and gap map
8. **Design and implement** reference architecture for experimental validation

## Usage

Export search results as CSV into `data/raw-search/` (one file per source), then deduplicate:

```bash
python3 scripts/dedup_records.py \
  --input-dir data/raw-search \
  --output-dir data/processed \
  --report-dir data/reports
```

### Build the LaTeX Paper

Build from the `paper/` directory with `latexmk`:

```powershell
cd paper
latexmk -pdf -interaction=nonstopmode -file-line-error paper.tex
```

If a previous build was interrupted and left `paper.synctex(busy)` behind, delete that file before rebuilding.

## Standards

- [PRISMA 2020](http://www.prisma-statement.org/) — reporting guideline
- [PRISMA-S](https://doi.org/10.1186/s13643-020-01542-z) — search strategy reporting extension

## License

All rights reserved. This repository contains unpublished research materials.
