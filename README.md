# Atlas: Bitcoin Multi-Modal Market Sentiment & Representation Engine

[![Status](https://img.shields.io/badge/Status-Wave%200%20(Closed)-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)]()
[![Architecture](https://img.shields.io/badge/Architecture-Regex%20%7C%20TypeSafe%20Jev%20%7C%20JEPA-green.svg)]()
[![Integration](https://img.shields.io/badge/Downstream-quant--platform-orange.svg)]()

`Atlas` is an institutional-grade, multi-modal market sentiment and state representation engine for Bitcoin (BTC). It processes high-volume social media, mainstream/crypto news, discrete on-chain whale events, mempool metrics, and derivatives positioning into temporally rigorous, point-in-time features designed for direct consumption by [`quant-platform`](../quant-platform).

---

## Key Principles & Technology Stack

1. **Deterministic Line-Rate Pre-Filtering (Regex L1)**:
   - High-throughput compiled regex matching drops $\ge 75\%$ of raw social spam, botnet shilling, and duplicate copy-pasta before consuming AI inference compute.
2. **TypeSafe AI Jev (Semantic L2)**:
   - Non-generative "System One" classification via constrained decoding (`typesafe-sdk`).
   - Evaluates both narrative text sentiment and on-chain capital flow intent (`flow_intent`, `is_immediate_sell_pressure`, `capital_magnitude`) with strong schema guarantees (`Noul`, `Choice`, `Score`) at $\$0.042 / 1\text{M}$ input tokens.
3. **Cross-Modal Point-in-Time Fusion (Feature Store L3)**:
   - Fuses social/news sentiment with on-chain whale intent, mempool velocity, and derivatives positioning (funding rates and open interest).
   - Strict dual timestamping (`published_at` vs `observed_at`) guarantees zero lookahead bias in historical research.
4. **Joint Embedding Predictive Architecture (JEPA L4)**:
   - Predicts future market state transitions in latent representation space without costly autoregressive token generation.
5. **Operator Control Plane (CLI v1)**:
   - Single command-line interface (`atlas`) for daemon lifecycle, interactive pipeline tracing (`atlas probe`), backfilling, and feature export.

---

## Repository & Governance Architecture

This codebase follows the strict governance, traceability, and capability model pioneered in `quant-platform`:

```text
Atlas/
├── docs/
│   ├── product/
│   │   ├── PRODUCT.md                 <- Vision, principles, invariants, non-goals
│   │   ├── CAPABILITY_MAP.md          <- Compact capability inventory (28 atoms)
│   │   ├── CAPABILITY_DAG.md          <- Strict atom dependency graph & acceptance rules
│   │   └── ROADMAP.md                 <- Waves 0 through 5, milestones & decision gates
│   ├── architecture/
│   │   └── TARGET_ARCHITECTURE.md     <- System blueprint, dual on-chain flow, storage tiers
│   └── contracts/
│       ├── OPERATOR_CLI_CONTRACT.md   <- Command line interface syntax, exit codes, output
│       ├── ATLAS_CONFIG_CONTRACT.md   <- Declarative configuration (atlas.toml & .env)
│       ├── CANONICAL_DOCUMENT.md      <- Pydantic schema for canonical documents
│       ├── JEV_EVALUATION_CONTRACT.md <- Narrative & On-Chain Jev question topologies
│       └── FEATURE_ARTIFACT_EXPORT.md <- Parquet schema conforming to quant-platform ADR-0034
├── src/
│   └── atlas/                         <- Core engine packages
│       ├── contracts/                 <- Verified Pydantic models
│       ├── ingestion/                 <- Harvesters and pollers (Wave 1)
│       └── processing/                <- Regex and anti-spam filters (Wave 1)
├── tests/                             <- Unit, contract, and golden E2E test suites
├── SCOPE.md                           <- Active bounded implementation scope
└── pyproject.toml                     <- Dependencies, build configuration, and CLI entrypoint
```

---

## Authority & Documentation Links

- **Product Definition**: [`docs/product/PRODUCT.md`](docs/product/PRODUCT.md)
- **Capability Map**: [`docs/product/CAPABILITY_MAP.md`](docs/product/CAPABILITY_MAP.md)
- **Capability DAG**: [`docs/product/CAPABILITY_DAG.md`](docs/product/CAPABILITY_DAG.md)
- **Roadmap & Waves**: [`docs/product/ROADMAP.md`](docs/product/ROADMAP.md)
- **Target Architecture**: [`docs/architecture/TARGET_ARCHITECTURE.md`](docs/architecture/TARGET_ARCHITECTURE.md)
- **Active Scope**: [`SCOPE.md`](SCOPE.md)
