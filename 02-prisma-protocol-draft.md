# 02 - PRISMA Protocol Draft

## Review title
Systematic Review of Blockchain Utilization Strategies in Institutional Consortium Networks, with Technical Reference Implementation Plan.

## Objective
Synthesize technical evidence on how institutions design and deploy consortium blockchain strategies, and derive an experimentally testable reference architecture.

## Standards and reporting
- PRISMA 2020
- PRISMA-S (search strategy reporting)

## Eligibility criteria
### Include
- Peer-reviewed papers, high-quality preprints, and technical reports with implementation detail.
- Institutional multi-party settings (inter-bank, inter-agency, consortium B2B).
- Explicit strategy details (consensus/governance/privacy/interoperability/architecture).
- Quantitative or reproducible technical evaluation outputs.

### Exclude
- Non-technical commentary/policy-only papers.
- No implementation details.
- Single-organization private workflow studies without inter-institutional interaction.
- Crypto-market-only prediction studies unrelated to consortium operations.

## Information sources
- IEEE Xplore
- ACM Digital Library
- Scopus
- Web of Science
- arXiv

## Search strategy (draft)
Core query blocks (to refine in pilot):
- ("consortium blockchain" OR "permissioned blockchain" OR "enterprise blockchain")
- AND (institution* OR interbank OR "cross-organizational" OR "multi-party")
- AND (governance OR consensus OR privacy OR interoperability OR "cross-chain")
- AND (benchmark OR evaluation OR experiment OR implementation)

## Selection process
1. Deduplicate records (Zotero/Rayyan).
2. Title/abstract screening.
3. Full-text screening.
4. Record exclusion reasons.
5. Generate PRISMA flow counts.

### Reviewer process
- Two reviewers screen independently for each phase.
- Conflicts are resolved by discussion; unresolved conflicts go to third-review adjudication.
- Inter-rater agreement will be reported at title/abstract and full-text phases.

## Data extraction fields
- Bibliographic metadata (year, venue, domain).
- Platform/stack (Fabric, Besu, Quorum, Corda, etc.).
- Network model (permissioned/hybrid, node roles, trust assumptions).
- Consensus and finality strategy.
- Governance and access control model.
- Privacy/confidentiality mechanism.
- Interoperability strategy.
- Evaluation setup, workload, and metrics.
- Reproducibility artifacts (code/data/config availability).

## Quality/risk-of-bias rubric (draft dimensions)
- Construct validity (are metrics aligned with claims?).
- Internal validity (confounders controlled?).
- External validity (generalization to institutional contexts?).
- Reproducibility (artifact completeness, setup determinism).

## Synthesis plan
- Build taxonomy across architecture/governance/privacy/interoperability.
- Quantitative narrative synthesis of metric trade-offs.
- Identify evidence concentration and blind spots.
- Produce implementation requirements for reference prototype.

## Protocol registration
- Target registry: OSF
- Status: pending registration after search-string pilot freeze.

### Registration package checklist
- Final protocol text (versioned).
- Research questions and scope boundaries.
- Inclusion/exclusion criteria and rationale.
- Search sources and finalized query strings.
- Screening/extraction templates.
- Quality-assessment rubric and scoring rules.
- Amendments and deviation policy.

## Amendments policy
Any protocol changes after pilot must be logged with rationale, date, and impact on inclusion/synthesis.

## Version control and artifacts
- Protocol versions are tagged in git with change notes.
- Screening, extraction, and quality sheets are stored as CSV with immutable snapshots per milestone.
- Any post-registration deviation is documented both in the protocol appendix and commit history.
