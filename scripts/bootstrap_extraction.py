"""Bootstrap the per-study data extraction sheet for the 279 included studies.

Pulls from `data_extraction.csv` (master 863-row scaffold) the rows whose
candidate maps to a `final_decision = include`, and pre-fills heuristic
hints for a small subset of the 37 fields where title/abstract evidence is
strong enough to be useful as a starting point. All heuristic fills are
prefixed `[auto] ` so the human reviewer can spot and overwrite them.

Outputs:
  data/processed/data_extraction_includes.csv
  data/reports/data_extraction_bootstrap_report.md
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "data" / "processed" / "data_extraction.csv"
SCREEN = ROOT / "data" / "processed" / "fulltext_screening.csv"
MASTER = ROOT / "data" / "processed" / "master_dedup.csv"
QUALITY = ROOT / "data" / "processed" / "quality_assessment.csv"
OUT_CSV = ROOT / "data" / "processed" / "data_extraction_includes.csv"
OUT_MD = ROOT / "data" / "reports" / "data_extraction_bootstrap_report.md"

PLATFORM_PATTERNS = [
    ("Hyperledger Fabric", re.compile(r"\bhyperledger\s+fabric\b|\bfabric\b", re.I)),
    ("Hyperledger Besu", re.compile(r"\bbesu\b", re.I)),
    ("Quorum", re.compile(r"\bquorum\b", re.I)),
    ("Corda", re.compile(r"\bcorda\b", re.I)),
    ("Ethereum", re.compile(r"\bethereum\b|\bgeth\b", re.I)),
    ("Hyperledger Sawtooth", re.compile(r"\bsawtooth\b", re.I)),
    ("Hyperledger Iroha", re.compile(r"\biroha\b", re.I)),
    ("Polkadot", re.compile(r"\bpolkadot|substrate\b", re.I)),
    ("Cosmos", re.compile(r"\bcosmos\s+sdk|tendermint\b", re.I)),
]

CONSENSUS_PATTERNS = [
    ("PBFT", re.compile(r"\bpbft\b", re.I)),
    ("BFT (general)", re.compile(r"\bbft\b", re.I)),
    ("RAFT", re.compile(r"\braft\b", re.I)),
    ("PoA", re.compile(r"\bpoa\b|\bproof[- ]of[- ]authority\b", re.I)),
    ("PoS", re.compile(r"\bpos\b|\bproof[- ]of[- ]stake\b", re.I)),
    ("PoW", re.compile(r"\bpow\b|\bproof[- ]of[- ]work\b", re.I)),
    ("Tendermint", re.compile(r"\btendermint\b", re.I)),
    ("HotStuff", re.compile(r"\bhotstuff\b", re.I)),
]

DOMAIN_PATTERNS = [
    ("healthcare", re.compile(r"\bhealth\w*|medic\w+|patient|clinical|ehr\b", re.I)),
    ("finance/banking", re.compile(r"\bbank\w*|financ\w+|payment|settle\w+|fintech\b", re.I)),
    ("supply chain", re.compile(r"\bsupply[- ]?chain|logistic\w+|provenance|traceabili\w+\b", re.I)),
    ("government/public sector", re.compile(r"\bgovern\w+|public sector|e[- ]?gov\w+\b", re.I)),
    ("energy/utilities", re.compile(r"\benerg\w+|smart grid|utility|microgrid\b", re.I)),
    ("identity", re.compile(r"\bidentit\w+|did\b|kyc\b|self[- ]?sovereign\b", re.I)),
    ("IoT/edge", re.compile(r"\biot\b|edge|cyber[- ]?physical|industrial internet\b", re.I)),
    ("education", re.compile(r"\beducat\w+|academic|credential|diploma\b", re.I)),
]

INTEROP_PATTERNS = [
    ("cross-chain bridge", re.compile(r"\bcross[- ]?chain|bridge\w*\b", re.I)),
    ("relay/notary", re.compile(r"\brelay\b|notary scheme\b", re.I)),
    ("HTLC", re.compile(r"\bhtlc\b|hash[- ]?time[- ]?lock\b", re.I)),
    ("interledger/IBC", re.compile(r"\binterledger\b|\bibc\b", re.I)),
]

PRIVACY_PATTERNS = [
    ("zero-knowledge", re.compile(r"\bzero[- ]?knowledge|zk[- ]?(snark|stark|rollup)\b", re.I)),
    ("homomorphic encryption", re.compile(r"\bhomomorphic\b", re.I)),
    ("MPC/secure computation", re.compile(r"\bsecure (?:multi[- ]?party|multiparty)|mpc\b", re.I)),
    ("private channels", re.compile(r"\bprivate (?:channel|data|collection)|channels?\b", re.I)),
    ("differential privacy", re.compile(r"\bdifferential privacy\b", re.I)),
]

ARTIFACT_HINT = re.compile(
    r"\b(open[- ]?source|github\.com|gitlab\.com|zenodo|reproduc\w+|"
    r"artifact|public(?:ly)? available|replication package)\b",
    re.I,
)
SC_HINT = re.compile(r"\bsmart contract|chaincode|solidity|vyper\b", re.I)


def _first_match(text: str, patterns) -> str:
    hits = [name for name, rx in patterns if rx.search(text)]
    return ", ".join(dict.fromkeys(hits))


def _load_index(path: Path, key_field: str) -> dict:
    with path.open(encoding="utf-8", newline="") as f:
        return {r[key_field]: r for r in csv.DictReader(f) if r.get(key_field)}


def _abstract_index() -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], dict] = {}
    with MASTER.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = (
                (row.get("title") or "").strip().lower(),
                (row.get("doi") or "").strip().lower(),
            )
            out[key] = row
    return out


def main() -> None:
    extract = _load_index(EXTRACT, "study_id")
    quality = _load_index(QUALITY, "candidate_id")
    abstracts = _abstract_index()

    with SCREEN.open(encoding="utf-8", newline="") as f:
        screen_rows = list(csv.DictReader(f))
    includes = [r for r in screen_rows if r.get("final_decision") == "include"]

    out_rows: list[dict] = []
    fill_counts: Counter[str] = Counter()
    domain_counts: Counter[str] = Counter()
    platform_counts: Counter[str] = Counter()
    consensus_counts: Counter[str] = Counter()

    # We map candidate_id (CAND-####) to study_id (ST-####) by matching
    # title+doi, since the extraction file uses ST-#### IDs.
    extract_by_key: dict[tuple[str, str], dict] = {}
    for sid, row in extract.items():
        key = ((row.get("title") or "").strip().lower(),
               (row.get("doi") or "").strip().lower())
        extract_by_key[key] = row

    for r in includes:
        title = (r.get("title") or "").strip()
        doi = (r.get("doi") or "").strip().lower()
        key = (title.lower(), doi)
        ext = extract_by_key.get(key) or extract_by_key.get((title.lower(), ""))
        if not ext:
            continue  # rare: no scaffold row
        master = abstracts.get(key) or abstracts.get((title.lower(), ""))
        abstract = (master or {}).get("abstract", "") or ""
        text = f"{title}\n{abstract}"
        qrow = quality.get(r.get("candidate_id", ""), {})

        new = dict(ext)  # copy scaffold

        platform = _first_match(text, PLATFORM_PATTERNS)
        consensus = _first_match(text, CONSENSUS_PATTERNS)
        domain = _first_match(text, DOMAIN_PATTERNS)
        interop = _first_match(text, INTEROP_PATTERNS)
        privacy = _first_match(text, PRIVACY_PATTERNS)

        if platform:
            new["platform_stack"] = f"[auto] {platform}"; fill_counts["platform_stack"] += 1
            for p in platform.split(", "):
                platform_counts[p] += 1
        if consensus:
            new["consensus_strategy"] = f"[auto] {consensus}"; fill_counts["consensus_strategy"] += 1
            for c in consensus.split(", "):
                consensus_counts[c] += 1
        if domain:
            new["domain"] = f"[auto] {domain}"; fill_counts["domain"] += 1
            for d in domain.split(", "):
                domain_counts[d] += 1
        if interop:
            new["interoperability_strategy"] = f"[auto] {interop}"; fill_counts["interoperability_strategy"] += 1
        if privacy:
            new["privacy_mechanism"] = f"[auto] {privacy}"; fill_counts["privacy_mechanism"] += 1
        if SC_HINT.search(text):
            new["smart_contract_support"] = "[auto] yes"; fill_counts["smart_contract_support"] += 1
        if ARTIFACT_HINT.search(text):
            new["artifact_code_available"] = "[auto] hinted"; fill_counts["artifact_code_available"] += 1

        new["review_notes"] = (
            f"[bootstrap] tier={qrow.get('tier','?')} "
            f"score={qrow.get('total_score','?')}; "
            "auto-fills are abstract-only hints, verify against full text."
        )
        out_rows.append(new)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(next(iter(extract.values())).keys())
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    lines = [
        "# Data Extraction Bootstrap (279 included studies)",
        "",
        f"- Output: `{OUT_CSV.relative_to(ROOT).as_posix()}` "
        f"({len(out_rows)} rows × {len(fieldnames)} cols).",
        "- All auto-filled values are prefixed `[auto] ` for reviewer audit.",
        "",
        "## Field-fill counts (heuristic, abstract-only)",
        "| Field | Filled |",
        "|-------|--------|",
    ]
    for k, v in fill_counts.most_common():
        lines.append(f"| `{k}` | {v} |")
    lines += [
        "",
        "## Domain hits",
        "| Domain | Studies |",
        "|--------|---------|",
    ]
    for k, v in domain_counts.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Platform hits",
        "| Platform | Studies |",
        "|----------|---------|",
    ]
    for k, v in platform_counts.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Consensus hits",
        "| Consensus | Studies |",
        "|-----------|---------|",
    ]
    for k, v in consensus_counts.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Caveat",
        "Heuristics run only on title + abstract because the agent full-text "
        "reviewer ran in-memory and did not persist parsed text. These "
        "bootstrap hints are intended as starting points for the full Step-6 "
        "extraction pass on tier-A/B studies.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_CSV.relative_to(ROOT)} ({len(out_rows)} rows)")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    print("Fill counts:", dict(fill_counts))


if __name__ == "__main__":
    main()
