# Sentiment: Bitcoin Multi-Modal Market Sentiment Engine

[![Status](https://img.shields.io/badge/Status-Wave%200%20(Planning)-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)]()
[![Architecture](https://img.shields.io/badge/Architecture-Regex%20%7C%20TypeSafe%20Jev%20%7C%20JEPA-green.svg)]()

`Sentiment` is an institutional-grade, multi-modal market sentiment engine for Bitcoin (BTC). It processes high-volume social media, mainstream/crypto news, mempool metrics, and derivatives microstructure into temporally rigorous, point-in-time features designed for direct integration with [`quant-platform`](../quant-platform).

---

## Key Principles & Technology Stack

1. **Deterministic Line-Rate Pre-Filtering (Regex L1)**:
   - High-throughput regex matching drops $>75\%$ of raw social spam, botnet shilling, and duplicate copy-pasta before consuming AI inference compute.
2. **TypeSafe AI Jev (Semantic L2)**:
   - Non-generative "System One" classification via constrained decoding (`typesafe-sdk`).
   - Strong schema guarantees (`Noul`, `Choice`, `Score`) with zero JSON hallucination risk at $\$0.042 / 1\text{M}$ input tokens.
3. **Cross-Modal Point-in-Time Fusion (Feature Store L3)**:
   - Fuses social/news sentiment with on-chain mempool velocity and derivatives positioning (funding rates and open interest).
   - Strict dual timestamping (`published_at` vs `observed_at`) to guarantee zero lookahead bias in backtests.
4. **Joint Embedding Predictive Architecture (JEPA L4)**:
   - Predicts future market state transitions in latent representation space without costly autoregressive token generation.

---

## Repository & Governance Architecture

This codebase follows the strict governance, traceability, and capability model pioneered in `quant-platform`:

```text
Sentiment/
├── docs/
│   ├── product/
│   │   ├── PRODUCT.md           <- Vision, principles, invariants, non-goals
│   │   ├── CAPABILITY_MAP.md    <- Compact capability inventory & decision states
│   │   ├── CAPABILITY_DAG.md    <- Strict atom dependency graph & acceptance rules
│   │   └── ROADMAP.md           <- Waves 0 through 5, milestones & decision gates
│   ├── architecture/
│   │   └── TARGET_ARCHITECTURE.md <- System blueprint, storage tiering, data funnel
│   └── contracts/
│       ├── CANONICAL_DOCUMENT.md  <- Pydantic schema for canonical documents
│       └── JEV_EVALUATION_CONTRACT.md <- TypeSafe Jev question topology & scoring
├── src/
│   └── sentiment/               <- Core engine packages
├── tests/                       <- Unit, contract, and golden E2E test suites
├── SCOPE.md                     <- Active bounded implementation scope
└── pyproject.toml               <- Dependencies and build configuration
```

---

## Authority & Documentation Links

- **Product Vision & Invariants**: [`docs/product/PRODUCT.md`](docs/product/PRODUCT.md)
- **Capability Map**: [`docs/product/CAPABILITY_MAP.md`](docs/product/CAPABILITY_MAP.md)
- **Capability DAG**: [`docs/product/CAPABILITY_DAG.md`](docs/product/CAPABILITY_DAG.md)
- **Roadmap & Waves**: [`docs/product/ROADMAP.md`](docs/product/ROADMAP.md)
- **Target Architecture**: [`docs/architecture/TARGET_ARCHITECTURE.md`](docs/architecture/TARGET_ARCHITECTURE.md)
- **Active Scope**: [`SCOPE.md`](SCOPE.md)
