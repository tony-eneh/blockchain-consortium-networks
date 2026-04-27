# Spot-Check Sample (Week 9 author audit)

- Output: `data/processed/spotcheck_sample.csv`.
- Random seed: `20260428` (deterministic).
- Total sampled rows: **40** (includes: 20, excludes: 20).

## Include strata
| Tier | Population | Sampled |
|------|------------|---------|
| A | 26 | 5 |
| B | 122 | 5 |
| C | 110 | 5 |
| D | 21 | 5 |

## Exclude strata (top reasons)
| Reason code | Population | Sampled |
|-------------|------------|---------|
| `insufficient_fulltext_access` | 281 | 4 |
| `no_full_text_access` | 210 | 4 |
| `second_pass_likely_exclude` | 48 | 4 |
| `agent_uncertain_full_text` | 32 | 4 |
| `no_quantitative_or_reproducible_evidence` | 7 | 4 |

## Reviewer instructions
- Open `data/processed/spotcheck_sample.csv`.
- Fill `human_decision` ∈ {`include`, `exclude`, `unsure`} and add `human_notes`.
- Compute agreement rate = matches / total once complete.
