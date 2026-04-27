# Quality Assessment Report (screening-stage rubric)

- Inputs: `data/processed/fulltext_screening.csv`, `data/processed/master_dedup.csv`.
- Output sheet: `data/processed/quality_assessment.csv`.
- Studies scored: **279** (final-decision = include).
- Abstracts available for scoring: **279 / 279**.

## Rubric (each dimension 0–2, total 0–8)
1. **Construct validity** — evaluation vocabulary present in title/abstract.
2. **Internal validity** — peer-reviewed venue and/or explicit comparison/baseline signal.
3. **External validity** — institutional/cross-organizational context markers.
4. **Reproducibility** — artifact/code/data signals; implementation language.

Tiers: A ≥ 6, B 4–5, C 2–3, D 0–1.

## Tier distribution
| Tier | Studies |
|------|---------|
| A | 26 |
| B | 122 |
| C | 110 |
| D | 21 |

## Total-score distribution
| Total | Studies |
|-------|---------|
| 7 | 5 |
| 6 | 21 |
| 5 | 49 |
| 4 | 73 |
| 3 | 71 |
| 2 | 39 |
| 1 | 15 |
| 0 | 6 |

## Caveat
These scores are **screening-stage triage signals only**, derived from title + abstract + source. Final per-study quality scoring requires a full-text rubric pass (Step 7 deep dive) on tier-A/B candidates first.
