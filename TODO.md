# Systematic Review + Reference Implementation TODO

Topic: **Blockchain utilization strategies between institutions (consortium/inter-institutional networks)**

Standards: **PRISMA 2020**, **PRISMA-S** (search reporting), plus reproducibility artifact package.

## Ordered execution plan

1. **Define review questions (PICOC-framed)**
   - Lock 2-4 technical research questions.
   - Freeze scope: consortium/inter-bank/inter-agency institutional settings.

2. **Write protocol (PRISMA)**
   - Inclusion/exclusion criteria.
   - Outcomes and variables.
   - Quality/risk-of-bias rubric.
   - Analysis and synthesis plan.
   - Register protocol (OSF).

3. **Build search strings and source list**
   - Databases: IEEE Xplore, ACM DL, Scopus, Web of Science, arXiv.
   - Pilot and refine Boolean strings.

4. **Run search and deduplicate**
   - Export records, deduplicate in Zotero/Rayyan.
   - Freeze corpus snapshot and date.

5. **Screen studies (2-stage)**
   - Title/abstract screening.
   - Full-text screening.
   - Record exclusion reasons for PRISMA flow.

6. **Extract technical data**
   - Architecture model, consensus, governance.
   - Privacy/security mechanisms.
   - Interoperability strategy.
   - Performance/economic/operational metrics.
   - Workload and evaluation setup.

7. **Quality assessment**
   - Reproducibility score.
   - Internal/external validity checks.
   - Bias and threats to validity.

8. **Synthesize evidence**
   - Taxonomy of institutional blockchain strategies.
   - Comparative evidence tables.
   - Gap map and open research problems.

9. **Design reference implementation**
   - Architecture for consortium setting.
   - Strategy variants to compare (e.g., governance/consensus/privacy choices).

10. **Implement prototype**
    - Reproducible stack (e.g., Hyperledger Fabric or Besu).
    - Scripts for deployment, workload generation, and measurement.

11. **Run experiments**
    - Throughput, latency, finality.
    - Fault tolerance and recovery.
    - Privacy/security overhead.
    - Operational complexity and cost proxies.

12. **Write paper + artifact package**
    - PRISMA checklist and flow diagram.
    - Methods/results/discussion with technical depth.
    - Public replication artifacts and appendix.

## Deliverable discipline
- Every stage ends with a versioned artifact.
- No claims without traceable evidence (paper/source/experiment log).
- Keep scripts/configs deterministic where possible.
