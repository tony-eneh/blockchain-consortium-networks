# 01 - Review Questions and Scope (PICOC)

## Problem framing
Institutional actors (banks, regulators, insurers, public agencies, and enterprise consortia) increasingly use permissioned/distributed ledger systems for shared workflows. The technical design space is fragmented, and strategy choices are often made without comparable evidence on performance, governance, interoperability, and operational trade-offs.

## PICOC
- **Population (P):** Institutional multi-party workflows and consortium networks (inter-bank, inter-agency, B2B regulated collaboration).
- **Intervention (I):** Blockchain utilization strategies (platform choice, consensus, governance model, privacy layer, interoperability approach).
- **Comparison (C):** Alternative strategy choices, non-blockchain baselines where reported, and cross-platform implementations.
- **Outcomes (O):** Throughput, latency, finality, fault tolerance, privacy/security guarantees, interoperability performance, operational overhead, and maintainability.
- **Context (C):** Regulated or compliance-sensitive settings with multi-organization trust boundaries.

## Primary research questions (locked)
1. **RQ1:** Which blockchain utilization strategies are reported for institutional consortium workflows, and how can they be taxonomized across architecture, governance, consensus, and privacy dimensions?
2. **RQ2:** What empirical evidence exists on trade-offs among performance, resilience, privacy, and operational complexity for these strategies?
3. **RQ3:** Which interoperability patterns (cross-chain, API-mediated, bridge/oracle, messaging/event-driven) are most effective in institutional settings, and under what constraints?
4. **RQ4:** What design gaps and reproducibility weaknesses remain, and how should a reference implementation be structured to address them?

## Scope boundaries
### In scope
- Technical papers with explicit implementation details.
- Consortium or inter-institutional deployments/prototypes.
- Permissioned, hybrid, or interoperability-focused blockchain strategies.
- Quantitative evaluations or clearly specified engineering outcomes.

### Out of scope
- Purely conceptual/policy/legal papers without technical implementation.
- Single-organization internal ledgers without inter-institutional coordination.
- Cryptocurrency market-trading studies without consortium workflow focus.
- Opinion pieces without method or reproducible evidence.

## Decision notes
- The review is **technical-first** and paired with a **reference implementation** phase.
- PRISMA process quality will be enforced, but contribution target is systems/engineering evidence.
