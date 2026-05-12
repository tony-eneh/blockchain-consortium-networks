#!/usr/bin/env python3
"""Full-text data extraction for open-access Tier A/B papers.

Reads each locally-saved PDF/HTML from data/fulltext/tier-ab/, extracts text,
then uses regex and heuristic NLP to fill the 30 empty fields in
data_extraction_includes.csv. All fills are prefixed [ft] to distinguish
full-text extraction from [auto] (abstract-only) and human fills.

Priority: Tier A first (13 papers), then Tier B (63 papers).

Output:
  data/processed/data_extraction_includes.csv  (updated in-place)
  data/reports/extraction_tierab_report.md
"""

from __future__ import annotations

import csv
import io
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from pypdf import PdfReader
from pypdf.errors import EmptyFileError, PdfReadError

ROOT = Path(__file__).resolve().parents[1]
FULLTEXT_DIR = ROOT / "data" / "fulltext" / "tier-ab"
EXTRACTION_CSV = ROOT / "data" / "processed" / "data_extraction_includes.csv"
FULLTEXT_SCREENING = ROOT / "data" / "processed" / "fulltext_screening.csv"
QUALITY_CSV = ROOT / "data" / "processed" / "quality_assessment.csv"
REPORT = ROOT / "data" / "reports" / "extraction_tierab_report.md"

PREFIX = "[ft] "   # marks full-text extraction fills


def console_safe(text: str) -> str:
    """Return text safe to print for the current console encoding."""
    enc = getattr(sys.stdout, "encoding", None) or "utf-8"
    return text.encode(enc, errors="replace").decode(enc, errors="replace")

# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------


def extract_text(path: Path, max_chars: int = 60_000) -> str:
    """Extract plain text from PDF or HTML file."""
    if path.suffix.lower() == ".pdf":
        try:
            reader = PdfReader(str(path))
            parts = []
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    parts.append(t)
                if sum(len(p) for p in parts) >= max_chars:
                    break
            return "\n".join(parts)[:max_chars]
        except (EmptyFileError, PdfReadError, Exception):
            return ""
    elif path.suffix.lower() in (".html", ".htm"):
        try:
            soup = BeautifulSoup(path.read_bytes(), "html.parser")
            # Remove nav/script/style noise
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            return soup.get_text(separator="\n", strip=True)[:max_chars]
        except Exception:
            return ""
    return ""


# ---------------------------------------------------------------------------
# Pattern libraries
# ---------------------------------------------------------------------------

PLATFORM_PATTERNS = [
    ("Hyperledger Fabric", re.compile(r"\bhyperledger\s+fabric\b|\bfabric\b", re.I)),
    ("Hyperledger Besu",   re.compile(r"\bbesu\b", re.I)),
    ("Hyperledger Sawtooth", re.compile(r"\bsawtooth\b", re.I)),
    ("Hyperledger Iroha",  re.compile(r"\biroha\b", re.I)),
    ("Quorum",             re.compile(r"\bquorum\b", re.I)),
    ("Corda",              re.compile(r"\bcorda\b", re.I)),
    ("Ethereum",           re.compile(r"\bethereum\b|\bgeth\b|\bsolidity\b", re.I)),
    ("Polkadot/Substrate", re.compile(r"\bpolkadot\b|\bsubstrate\b", re.I)),
    ("Cosmos/Tendermint",  re.compile(r"\bcosmos\s*sdk\b|\btendermint\b", re.I)),
    ("IOTA",               re.compile(r"\biota\b", re.I)),
    ("Ripple/XRP",         re.compile(r"\bripple\b|\bxrp\b", re.I)),
    ("Stellar",            re.compile(r"\bstellar\b", re.I)),
    ("Bitcoin",            re.compile(r"\bbitcoin\b", re.I)),
    ("Multichain",         re.compile(r"\bmultichain\b", re.I)),
]

CONSENSUS_PATTERNS = [
    ("PBFT",           re.compile(r"\bpbft\b|\bpractical byzantine\b", re.I)),
    ("HotStuff",       re.compile(r"\bhotstuff\b", re.I)),
    ("Tendermint BFT", re.compile(r"\btendermint\b", re.I)),
    ("BFT (general)",  re.compile(r"\bbyzantine fault\b|\bbft\b", re.I)),
    ("RAFT",           re.compile(r"\braft\b(?!\s*protocol\s+for)", re.I)),
    ("PoA",            re.compile(
        r"\bproof[- ]of[- ]authority\b|\bpoa\b", re.I)),
    ("PoS",            re.compile(r"\bproof[- ]of[- ]stake\b|\bpos\b", re.I)),
    ("PoW",            re.compile(r"\bproof[- ]of[- ]work\b|\bpow\b", re.I)),
    ("DPoS",           re.compile(
        r"\bdelegated\s+proof[- ]of[- ]stake\b|\bdpos\b", re.I)),
    ("Clique (PoA)",   re.compile(r"\bclique\b", re.I)),
    ("QBFT",           re.compile(r"\bqbft\b", re.I)),
    ("Istanbul BFT",   re.compile(r"\bistanbul\s+bft\b|\bibft\b", re.I)),
    ("Mir-BFT",        re.compile(r"\bmir[- ]bft\b", re.I)),
]

PRIVACY_PATTERNS = [
    ("zero-knowledge proofs",
     re.compile(r"\bzero[- ]?knowledge\b|\bzk[- ]?(snark|stark|proof|rollup)\b", re.I)),
    ("homomorphic encryption",  re.compile(r"\bhomomorphic\b", re.I)),
    ("MPC/secure computation",
     re.compile(r"\bsecure\s+(?:multi[- ]?party|multiparty)\s+comp\w+\b|\bmpc\b", re.I)),
    ("private channels",        re.compile(
        r"\bprivate\s+(?:channel|data|collection|transaction)\b", re.I)),
    ("differential privacy",    re.compile(r"\bdifferential\s+privacy\b", re.I)),
    ("ring signatures",         re.compile(r"\bring\s+signature\b", re.I)),
    ("stealth addresses",       re.compile(r"\bstealth\s+address\b", re.I)),
    ("TEE/SGX",
     re.compile(r"\btrusted\s+execution\b|\bsgx\b|\bsecure\s+enclave\b|\btee\b", re.I)),
    ("attribute-based encryption",
     re.compile(r"\battribute[- ]based\s+(?:encrypt|access)\b|\babe\b", re.I)),
    ("proxy re-encryption",
     re.compile(r"\bproxy\s+re[- ]?encrypt\b", re.I)),
    ("tokenisation",            re.compile(r"\btoken(?:is|iz)ation\b", re.I)),
]

INTEROP_PATTERNS = [
    ("cross-chain bridge",
     re.compile(r"\bcross[- ]?chain\b|\bblockchain\s+bridge\b", re.I)),
    ("relay/notary",
     re.compile(r"\brelay\s+(?:node|chain|scheme)\b|\bnotary\s+scheme\b", re.I)),
    ("HTLC",                  re.compile(
        r"\bhtlc\b|\bhash\s+time[- ]?lock\b", re.I)),
    ("interledger/IBC",       re.compile(r"\binterledger\b|\bibc\b", re.I)),
    ("oracle",                re.compile(r"\boracle\b(?!\s+database)", re.I)),
    ("API gateway",           re.compile(
        r"\bapi\s+gateway\b|\brest(?:ful)?\s+api\b", re.I)),
    ("sidechain",             re.compile(r"\bsidechain\b", re.I)),
    ("atomic swap",           re.compile(r"\batomic\s+swap\b", re.I)),
    ("message queue/broker",
     re.compile(r"\bmessage\s+(?:queue|broker|bus)\b|\bkafka\b|\brabbitmq\b", re.I)),
]

DOMAIN_PATTERNS = [
    ("healthcare",              re.compile(
        r"\bhealth\w*\b|\bmedic\w+\b|\bpatient\b|\bclinical\b|\behr\b|\bhospital\b|\bpharmac\w+\b", re.I)),
    ("finance/banking",         re.compile(r"\bbank\w*\b|\bfinanc\w+\b|\bpayment\b|\bsettle\w+\b|\bfintech\b|\bcredit\b|\baudit\b|\binsur\w+\b", re.I)),
    ("supply chain",            re.compile(
        r"\bsupply[- ]?chain\b|\blogistic\w+\b|\bprovenance\b|\btrace\w+\b|\bmanufactur\w+\b", re.I)),
    ("government/public sector",
     re.compile(r"\bgovern\w+\b|\bpublic\s+sector\b|\be[- ]?gov\w+\b|\bvot\w+\b|\bregulat\w+\b", re.I)),
    ("energy/utilities",
     re.compile(r"\benerg\w+\b|\bsmart\s+grid\b|\butility\b|\bmicrogrid\b|\bpower\s+grid\b", re.I)),
    ("identity/PKI",
     re.compile(r"\bidentit\w+\b|\bdid\b|\bkyc\b|\bself[- ]?sovereign\b|\bpki\b|\bcertificat\w+\b", re.I)),
    ("IoT/edge/CPS",
     re.compile(r"\biot\b|\bedge\s+comput\w+\b|\bcyber[- ]?physical\b|\bindust\w+\s+internet\b|\biiot\b", re.I)),
    ("education",               re.compile(
        r"\beducat\w+\b|\bacadem\w+\b|\bcredential\b|\bdiploma\b|\bexam\b", re.I)),
    ("transportation/mobility",
     re.compile(r"\btransport\w+\b|\bvehicl\w+\b|\buav\b|\bdrone\b|\bmobilit\w+\b", re.I)),
    ("agriculture",             re.compile(
        r"\bagric\w+\b|\bfarm\w+\b|\bfood\s+safety\b", re.I)),
]

NETWORK_MODEL_PATTERNS = [
    ("consortium",   re.compile(r"\bconsortium\b|\bfederated\b", re.I)),
    ("permissioned", re.compile(r"\bpermissioned\b", re.I)),
    ("private",      re.compile(r"\bprivate\s+blockchain\b", re.I)),
    ("public",       re.compile(r"\bpublic\s+blockchain\b", re.I)),
    ("hybrid",       re.compile(r"\bhybrid\s+blockchain\b", re.I)),
]

NODE_ROLE_PATTERNS = [
    ("orderer/ordering service", re.compile(r"\border(?:er|ing\s+service)\b", re.I)),
    ("peer/endorser",            re.compile(r"\bendors\w+\b|\bpeer\s+node\b", re.I)),
    ("validator",                re.compile(
        r"\bvalidator\s+node\b|\bvalidating\s+peer\b", re.I)),
    ("miner",                    re.compile(r"\bminer\b", re.I)),
    ("full node",                re.compile(r"\bfull\s+node\b", re.I)),
    ("light client",             re.compile(
        r"\blight(?:weight)?\s+(?:node|client)\b|\bspv\b", re.I)),
    ("anchor peer",              re.compile(r"\banchor\s+peer\b", re.I)),
    ("CA/MSP",
     re.compile(r"\bcertificate\s+authorit\w+\b|\bmembership\s+service\b|\bmsp\b", re.I)),
    ("gateway",                  re.compile(
        r"\bgateway\s+node\b|\bgateway\b", re.I)),
]

GOVERNANCE_PATTERNS = [
    ("DAO/on-chain voting",
     re.compile(r"\bdao\b|\bon[- ]?chain\s+vot\w+\b|\bgovernance\s+token\b", re.I)),
    ("consortium agreement",  re.compile(
        r"\bconsortium\s+(?:agreement|governance|members)\b", re.I)),
    ("regulator-controlled",  re.compile(r"\bregulat\w+\s+(?:node|body|authority)\b", re.I)),
    ("multi-sig policy",
     re.compile(r"\bmulti[- ]?sig\w*\b|\bmultisignature\b", re.I)),
    ("smart contract rules",  re.compile(
        r"\bgovernance\s+(?:smart\s+)?contract\b|\bpolicy\s+contract\b", re.I)),
]

ACCESS_CONTROL_PATTERNS = [
    ("RBAC", re.compile(r"\brbac\b|\brole[- ]?based\s+access\b", re.I)),
    ("ABAC", re.compile(r"\babac\b|\battribute[- ]?based\s+access\b", re.I)),
    ("ACL",  re.compile(r"\bacl\b|\baccess\s+control\s+list\b", re.I)),
    ("PBAC/policy-based",
     re.compile(r"\bpbac\b|\bpolicy[- ]?based\s+access\b", re.I)),
    ("capability-based",  re.compile(r"\bcapabilit\w+\s+(?:token|based)\b", re.I)),
    ("MSP (Fabric)",      re.compile(
        r"\bmembership\s+service\s+provider\b|\bmsp\b", re.I)),
    ("decentralized identity", re.compile(
        r"\bdecentralized\s+identit\w+\b|\bdid\b", re.I)),
]

FINALITY_PATTERNS = [
    ("immediate/deterministic",
     re.compile(r"\bimmediate\s+finalit\w+\b|\bdeterministic\s+finalit\w+\b", re.I)),
    ("probabilistic",           re.compile(
        r"\bprobabilistic\s+finalit\w+\b|\beventual\s+consistency\b", re.I)),
    ("BFT finality",            re.compile(r"\bbft\s+finalit\w+\b", re.I)),
    ("instant (single round)",  re.compile(
        r"\bsingle[- ]?round\b|\binstant\s+finalit\w+\b", re.I)),
]

ARTIFACT_PATTERNS = {
    "artifact_code_available": re.compile(
        r"\b(github\.com|gitlab\.com|open[- ]?source|source\s+code\s+(?:is\s+)?(?:publicly\s+)?available|"
        r"code\s+(?:is\s+)?(?:publicly\s+)?available|implementation\s+(?:is\s+)?(?:publicly\s+)?available)\b",
        re.I,
    ),
    "artifact_data_available": re.compile(
        r"\b(dataset\s+(?:is\s+)?(?:publicly\s+)?available|data\s+(?:is\s+)?(?:publicly\s+)?available|"
        r"zenodo|figshare|dryad|open\s+data)\b",
        re.I,
    ),
    "artifact_config_available": re.compile(
        r"\b(configuration\s+(?:is\s+)?(?:publicly\s+)?available|docker(?:file|[- ]?compose)?\b|"
        r"ansible|terraform|helm\s+chart|deployment\s+script)\b",
        re.I,
    ),
}

SC_POSITIVE = re.compile(
    r"\bsmart\s+contract\b|\bchaincode\b|\bsolidity\b|\bevm\b", re.I)

METRIC_PATTERNS = {
    "throughput":  re.compile(r"\b(throughput|tps|transactions?\s+per\s+second|tx/s)\b", re.I),
    "latency":     re.compile(r"\b(latency|response\s+time|confirmation\s+time|block\s+time|end[- ]to[- ]end\s+delay)\b", re.I),
    "fault_tolerance": re.compile(r"\b(fault\s+toleran\w+|bft\s+threshold|byzantine|node\s+failure|crash\s+toleran\w+)\b", re.I),
    "privacy_overhead": re.compile(r"\b(privacy\s+overhead|computational\s+cost|encryption\s+overhead|zk\s+proof\s+size)\b", re.I),
}

EVAL_SETUP_PATTERNS = [
    ("Hyperledger Caliper", re.compile(r"\bcaliper\b", re.I)),
    ("simulation",          re.compile(r"\bsimulat\w+\b", re.I)),
    ("testbed",             re.compile(
        r"\btestbed\b|\btest\s+network\b|\blocal\s+network\b", re.I)),
    ("prototype",           re.compile(
        r"\bprototype\b|\bproof[- ]of[- ]concept\b|\bpoc\b", re.I)),
    ("cloud deployment",    re.compile(
        r"\baws\b|\bazure\b|\bgcp\b|\bgoogle\s+cloud\b|\bec2\b|\bcloud\s+deploy\w+\b", re.I)),
    ("Raspberry Pi / edge hardware",
     re.compile(r"\braspberry\s+pi\b|\bedge\s+device\b|\biot\s+device\b", re.I)),
    ("Docker/Kubernetes",
     re.compile(r"\bdocker\b|\bkubernetes\b|\bk8s\b|\bcontainer\b", re.I)),
    ("formal verification", re.compile(
        r"\bformal\s+verif\w+\b|\bmodel\s+check\w+\b|\bproverif\b", re.I)),
]

WORKLOAD_PATTERNS = [
    ("YCSB",                re.compile(r"\bYCSB\b|\byahoo\s+cloud\s+serving\b", re.I)),
    ("custom benchmark",    re.compile(r"\bbenchmark\b|\bworkload\b", re.I)),
    ("real-world dataset",
     re.compile(r"\breal[- ]?world\s+data\b|\bproduction\s+data\b", re.I)),
    ("synthetic dataset",   re.compile(r"\bsynthetic\s+(?:data|transaction)\b", re.I)),
    ("trace-driven",
     re.compile(r"\btrace[- ]driven\b|\breal\s+trace\b", re.I)),
]

NUMBER_RE = re.compile(
    r"(\d[\d,\.]*)\s*(tps|tx/s|transactions?\s+per\s+second)", re.I)
LATENCY_RE = re.compile(
    r"(\d[\d,\.]*)\s*(ms|milliseconds?|seconds?|μs)\b", re.I)


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

def _match_patterns(text: str, patterns: list) -> list[str]:
    """Return list of matched labels from pattern list."""
    found = []
    for label, pat in patterns:
        if pat.search(text):
            found.append(label)
    return found


def _extract_throughput(text: str) -> str:
    matches = NUMBER_RE.findall(text)
    if matches:
        values = [m[0].replace(",", "") for m in matches[:3]]
        return PREFIX + "; ".join(values) + " TPS"
    return ""


def _extract_latency(text: str) -> str:
    matches = LATENCY_RE.findall(text)
    if matches:
        vals = [f"{m[0]} {m[1]}" for m in matches[:3]]
        return PREFIX + "; ".join(vals)
    return ""


def _short_snippet(text: str, pattern: re.Pattern, context: int = 120) -> str:
    """Return a short snippet around the first match of pattern."""
    m = pattern.search(text)
    if not m:
        return ""
    start = max(0, m.start() - context // 2)
    end = min(len(text), m.end() + context // 2)
    snippet = text[start:end].replace("\n", " ").strip()
    return snippet


def extract_fields(text: str, existing: dict) -> dict:
    """
    Given full text and existing row dict, return dict of updated fields.
    Only fills fields that are currently empty or contain only [auto] fills.
    """
    updates: dict[str, str] = {}

    def should_fill(field: str) -> bool:
        val = existing.get(field, "").strip()
        return not val or val.startswith("[auto]")

    def set_field(field: str, value: str) -> None:
        if should_fill(field) and value:
            updates[field] = value

    # Domain
    domains = _match_patterns(text, DOMAIN_PATTERNS)
    if domains:
        set_field("domain", PREFIX + "; ".join(domains))

    # Platform stack
    platforms = _match_patterns(text, PLATFORM_PATTERNS)
    if platforms:
        set_field("platform_stack", PREFIX + "; ".join(platforms))

    # Network model
    net_models = _match_patterns(text, NETWORK_MODEL_PATTERNS)
    if net_models:
        set_field("network_model", PREFIX + "; ".join(net_models))

    # Node roles
    roles = _match_patterns(text, NODE_ROLE_PATTERNS)
    if roles:
        set_field("node_roles", PREFIX + "; ".join(roles))

    # Consensus
    consensus = _match_patterns(text, CONSENSUS_PATTERNS)
    if consensus:
        set_field("consensus_strategy", PREFIX + "; ".join(consensus))

    # Finality
    finality = _match_patterns(text, FINALITY_PATTERNS)
    if finality:
        set_field("finality_model", PREFIX + "; ".join(finality))

    # Governance
    gov = _match_patterns(text, GOVERNANCE_PATTERNS)
    if gov:
        set_field("governance_model", PREFIX + "; ".join(gov))

    # Access control
    ac = _match_patterns(text, ACCESS_CONTROL_PATTERNS)
    if ac:
        set_field("access_control_model", PREFIX + "; ".join(ac))

    # Privacy mechanisms
    priv = _match_patterns(text, PRIVACY_PATTERNS)
    if priv:
        set_field("privacy_mechanism", PREFIX + "; ".join(priv))

    # Interoperability
    interop = _match_patterns(text, INTEROP_PATTERNS)
    if interop:
        set_field("interoperability_strategy", PREFIX + "; ".join(interop))

    # Smart contract support
    if should_fill("smart_contract_support"):
        sc = "yes" if SC_POSITIVE.search(text) else "not mentioned"
        set_field("smart_contract_support", PREFIX + sc)

    # Workload
    workloads = _match_patterns(text, WORKLOAD_PATTERNS)
    if workloads:
        set_field("workload_description", PREFIX + "; ".join(workloads))

    # Evaluation setup
    eval_setups = _match_patterns(text, EVAL_SETUP_PATTERNS)
    if eval_setups:
        set_field("evaluation_setup", PREFIX + "; ".join(eval_setups))

    # Metrics reported
    metrics = []
    for metric, pat in METRIC_PATTERNS.items():
        if pat.search(text):
            metrics.append(metric)
    if metrics:
        set_field("metrics_reported", PREFIX + "; ".join(metrics))

    # Throughput value
    tp = _extract_throughput(text)
    if tp:
        set_field("throughput", tp)

    # Latency value
    lat = _extract_latency(text)
    if lat:
        set_field("latency", lat)

    # Fault tolerance mentioned
    if should_fill("fault_tolerance"):
        ft_m = METRIC_PATTERNS["fault_tolerance"].search(text)
        if ft_m:
            snippet = _short_snippet(
                text, METRIC_PATTERNS["fault_tolerance"], 160)
            set_field("fault_tolerance", PREFIX + snippet[:200])

    # Privacy overhead mentioned
    if should_fill("privacy_overhead"):
        po_m = METRIC_PATTERNS["privacy_overhead"].search(text)
        if po_m:
            snippet = _short_snippet(
                text, METRIC_PATTERNS["privacy_overhead"], 160)
            set_field("privacy_overhead", PREFIX + snippet[:200])

    # Artifacts
    for art_field, pat in ARTIFACT_PATTERNS.items():
        if should_fill(art_field):
            if pat.search(text):
                snippet = _short_snippet(text, pat, 200)
                set_field(art_field, PREFIX + "yes — " + snippet[:180])
            else:
                set_field(art_field, PREFIX + "not found in full text")

    # Reproducibility notes: combine artifact signals
    if should_fill("reproducibility_notes"):
        repro_signals = []
        for art_field, pat in ARTIFACT_PATTERNS.items():
            if pat.search(text):
                repro_signals.append(art_field.replace(
                    "artifact_", "").replace("_", " "))
        if repro_signals:
            set_field("reproducibility_notes", PREFIX +
                      "signals found: " + "; ".join(repro_signals))
        else:
            set_field("reproducibility_notes", PREFIX +
                      "no reproducibility signals in full text")

    # Institutional setting: look for named organizations / countries
    if should_fill("institutional_setting"):
        org_pat = re.compile(
            r"\b(university|hospital|bank|ministry|government|consortium\s+of|"
            r"agency|authority|regulator|multinational|enterprise)\b",
            re.I,
        )
        orgs = list(dict.fromkeys(m.group(0)
                    for m in org_pat.finditer(text)))[:6]
        if orgs:
            set_field("institutional_setting", PREFIX + "; ".join(orgs))

    # Operational complexity notes
    if should_fill("operational_complexity_notes"):
        comp_pat = re.compile(
            r"\b(scalab\w+|overhead|complexity|deploy\w+\s+(?:cost|time)|"
            r"maintenance|administration|latency\s+overhead|resource\s+constraint)\b",
            re.I,
        )
        mentions = list(dict.fromkeys(m.group(0)
                        for m in comp_pat.finditer(text)))[:6]
        if mentions:
            set_field("operational_complexity_notes",
                      PREFIX + "; ".join(mentions))

    return updates


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # Load quality assessment for tier
    cid_to_tier: dict[str, str] = {}
    with open(QUALITY_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid_to_tier[row["candidate_id"]] = row["tier"]

    # Load fulltext_screening DOI/URL -> candidate_id + local_path
    doi_to_ft: dict[str, dict] = {}
    url_to_ft: dict[str, dict] = {}
    with open(FULLTEXT_SCREENING, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["doi"].strip():
                doi_to_ft[row["doi"].strip()] = row
            if row["url"].strip():
                url_to_ft[row["url"].strip()] = row

    # Load extraction CSV
    rows: list[dict] = []
    with open(EXTRACTION_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # Build index
    updated_count = 0
    failed_text = 0
    skipped_no_file = 0
    field_fill_counts: dict[str, int] = defaultdict(int)
    tier_a_done = []
    tier_b_done = []

    # Sort: Tier A first
    def sort_key(r):
        doi = r["doi"].strip()
        url = r["url"].strip()
        ft_row = doi_to_ft.get(doi) or url_to_ft.get(url)
        if not ft_row:
            return 99
        cid = ft_row["candidate_id"]
        tier = cid_to_tier.get(cid, "Z")
        return 0 if tier == "A" else (1 if tier == "B" else 2)

    sorted_rows = sorted(rows, key=sort_key)

    processed_study_ids = set()

    for row in sorted_rows:
        doi = row["doi"].strip()
        url = row["url"].strip()
        ft_row = doi_to_ft.get(doi) or url_to_ft.get(url)
        if not ft_row:
            continue

        cid = ft_row["candidate_id"]
        tier = cid_to_tier.get(cid, "")
        if tier not in ("A", "B"):
            continue

        local_path_str = ft_row.get("local_path", "").strip()
        if not local_path_str:
            skipped_no_file += 1
            continue

        local_path = ROOT / local_path_str
        if not local_path.exists():
            skipped_no_file += 1
            continue

        sid = row["study_id"]
        print(console_safe(f"[{tier}] {sid} ({cid}): {row['title'][:70]}"))

        text = extract_text(local_path)
        if not text.strip():
            print(f"  -> WARNING: no text extracted from {local_path.name}")
            failed_text += 1
            continue

        print(f"  -> {len(text):,} chars extracted from {local_path.name}")

        updates = extract_fields(text, row)
        if updates:
            for field, val in updates.items():
                row[field] = val
                field_fill_counts[field] += 1
            updated_count += 1
            print(
                f"  -> filled {len(updates)} fields: {', '.join(updates.keys())}")
        else:
            print(f"  -> no new fields to fill (all already populated)")

        processed_study_ids.add(sid)
        if tier == "A":
            tier_a_done.append(sid)
        else:
            tier_b_done.append(sid)

    # Write updated CSV preserving original row order
    row_map = {r["study_id"]: r for r in sorted_rows}
    final_rows = [row_map.get(r["study_id"], r) for r in rows]

    with open(EXTRACTION_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(final_rows)

    print(
        f"\nDone. Updated {updated_count} rows. Skipped (no file): {skipped_no_file}. Failed text extraction: {failed_text}.")

    # Report
    report_lines = [
        "# Tier A/B Full-Text Data Extraction Report",
        "",
        f"**Date:** {__import__('datetime').date.today().isoformat()}",
        f"**Papers processed:** {len(processed_study_ids)} ({len(tier_a_done)} Tier A, {len(tier_b_done)} Tier B)",
        f"**Rows updated:** {updated_count}",
        f"**Skipped (no local file):** {skipped_no_file}",
        f"**Failed text extraction:** {failed_text}",
        "",
        "## Field fill counts",
        "",
        "| Field | Papers filled |",
        "|-------|--------------|",
    ]
    for field, count in sorted(field_fill_counts.items(), key=lambda x: -x[1]):
        report_lines.append(f"| {field} | {count} |")

    report_lines += [
        "",
        "## Tier A papers processed",
        "",
    ]
    for sid in tier_a_done:
        report_lines.append(f"- {sid}")

    report_lines += [
        "",
        "## Notes",
        "",
        "- All fills prefixed `[ft]` (full-text extraction). Verify against original paper.",
        "- Numerical values (throughput, latency) are heuristic — check units in paper.",
        "- Papers with no local file skipped — use institutional VPN to obtain paywalled papers.",
        "",
    ]

    REPORT.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Report written to {REPORT}")


if __name__ == "__main__":
    main()
