# Data Extraction Bootstrap (279 included studies)

- Output: `data/processed/data_extraction_includes.csv` (279 rows × 37 cols).
- All auto-filled values are prefixed `[auto] ` for reviewer audit.

## Field-fill counts (heuristic, abstract-only)
| Field | Filled |
|-------|--------|
| `domain` | 251 |
| `smart_contract_support` | 92 |
| `platform_stack` | 79 |
| `privacy_mechanism` | 28 |
| `consensus_strategy` | 25 |
| `interoperability_strategy` | 18 |
| `artifact_code_available` | 11 |

## Domain hits
| Domain | Studies |
|--------|---------|
| IoT/edge | 159 |
| healthcare | 105 |
| supply chain | 69 |
| government/public sector | 58 |
| finance/banking | 38 |
| identity | 35 |
| education | 32 |
| energy/utilities | 21 |

## Platform hits
| Platform | Studies |
|----------|---------|
| Hyperledger Fabric | 49 |
| Ethereum | 32 |
| Corda | 5 |
| Hyperledger Besu | 4 |
| Quorum | 3 |
| Cosmos | 1 |
| Hyperledger Sawtooth | 1 |

## Consensus hits
| Consensus | Studies |
|-----------|---------|
| PBFT | 12 |
| RAFT | 6 |
| PoS | 5 |
| PoW | 5 |
| Tendermint | 1 |
| BFT (general) | 1 |
| HotStuff | 1 |
| PoA | 1 |

## Caveat
Heuristics run only on title + abstract because the agent full-text reviewer ran in-memory and did not persist parsed text. These bootstrap hints are intended as starting points for the full Step-6 extraction pass on tier-A/B studies.
