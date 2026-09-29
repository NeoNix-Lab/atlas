# Sentiment Engine Roadmap

**Status:** CANONICAL BASELINE — Wave 0 Planning  
**Repository:** `Sentiment`  
**Downstream Consumer:** `quant-platform`

This document defines the macro product-progression view. The authoritative atomic dependency and execution model is [`CAPABILITY_DAG.md`](CAPABILITY_DAG.md).

---

## Planning Layers

```text
ROADMAP.md          = Macro product progression and wave checkpoints
CAPABILITY_DAG.md   = Atomic capability dependencies and acceptance propositions
CAPABILITY_MAP.md   = Compact current-state inventory
OPEN_DECISIONS.md   = Unresolved decision gates (DG-A to DG-D)
ADRs + Contracts    = Authoritative semantic specifications
SCOPE.md            = Active bounded mutation scope for the current wave
```

---

## Macro Waves (0 – 5)

```text
Wave 0: Governance, Contracts & Data Schemas (Foundation)
   │
   ▼
Wave 1: Ingestion & Deterministic Line-Rate Engine (Regex + Anti-Spam)
   │
   ▼
Wave 2: Semantic Typing & Scoring via Jev (TypeSafe AI)
   │
   ▼
Wave 3: Multi-Modal Fusion (On-Chain Mempool + Derivatives Microstructure)
   │
   ▼
Wave 4: Latent Predictive Architecture (JEPA Context & Target Encoders)
   │
   ▼
Wave 5: Statistical Validation (IC / DSR) & quant-platform Feature Gateway
```

### Wave 0: Governance, Contracts & Data Schemas
* **Focus:** Repository setup, architecture documentation, data contracts (`CanonicalDocument`, `JevEvaluationContract`), and test fixtures.
* **Atoms Activated:** `B01`, `B04`, `C01`.
* **Deliverable:** Fully reviewed contracts and mock schemas; zero unvalidated code mutations.

### Wave 1: Ingestion & Deterministic Line-Rate Engine
* **Focus:** Build resilient harvesting for Reddit, Telegram, News feeds, and resolving Twitter ingestion (DG-A). Implement line-rate Regex pre-filter to drop $>75\%$ spam.
* **Atoms Activated:** `A01`, `A02`, `A03`, `A04`, `A05`, `B02`, `B03`.
* **Golden Proof:** `WAVE1_GOLDEN_E2E_DETERMINISTIC_INGESTION.md` (Demonstrates end-to-end ingestion, raw storage, and spam rejection on a frozen 1,000-message test corpus).

### Wave 2: Semantic Typing & Scoring via Jev (TypeSafe AI)
* **Focus:** Integrate `typesafe-sdk`, build the async gateway with rate-limiting and circuit breakers, and implement normalized feature vectorization.
* **Atoms Activated:** `C02`, `C03`, `D01`.
* **Golden Proof:** `WAVE2_GOLDEN_E2E_JEV_SEMANTIC_TYPING.md` (Proves zero-failure, deterministic typed extraction across 10,000 live harvested crypto events).

### Wave 3: Multi-Modal Fusion (On-Chain & Derivatives)
* **Focus:** Ingest mempool fee velocity, whale transaction alerts, and Binance/Bybit Funding Rate and Open Interest feeds. Resample into point-in-time time windows.
* **Atoms Activated:** `A06`, `A07`, `D02`, `D03`.
* **Golden Proof:** `WAVE3_GOLDEN_E2E_MULTIMODAL_FUSION.md` (Verifies seamless alignment of social sentiment vectors with real-time financial microstructure).

### Wave 4: Latent Predictive Architecture (JEPA)
* **Focus:** Resolve DG-C (Target State Formulation). Implement Context Encoder, EMA Target Encoder, and Latent Predictor. Self-supervised pre-training loop.
* **Atoms Activated:** `E01`, `E02`, `E03`, `E04`.
* **Golden Proof:** `WAVE4_GOLDEN_E2E_JEPA_REPRESENTATION.md` (Proves non-collapsing latent representations predicting market state transitions).

### Wave 5: Statistical Validation & quant-platform Gateway
* **Focus:** Information Coefficient (IC) evaluation, price-sentiment divergence signal detector, and Zero-Copy Arrow IPC export to `quant-platform`.
* **Atoms Activated:** `F01`, `F02`, `F03`.
* **Golden Proof:** `WAVE5_GOLDEN_E2E_ALPHA_GATEWAY.md` (Demonstrates out-of-sample predictive power and seamless consumption by `quant-platform`).

---

## Decision Gate Family (DG)

| Gate ID | Area | Proposition | Blocking For | Trigger Condition |
|---|---|---|---|---|
| **DG-A** | Ingestion | Social Connector: X / Twitter sourcing strategy (Syndication vs Guest scrapers vs Proxy pool) | `A04` | Selection of sustainable, low-cost harvesting mechanism |
| **DG-B** | Temporal | Re-indexing of delayed arrivals in sliding time-windows without lookahead leakage | `D01` | Specification of `observed_at` watermark and late-data policy |
| **DG-C** | Representation | Formulation of JEPA Target State $y_{t+\Delta t}$ (Log returns vs Realized Vol vs Orderbook Imbalance) | `E01` | Formal mathematical specification of the prediction target |
| **DG-D** | Storage | Feature Store persistence engine (Local DuckDB + Partitioned Parquet vs ClickHouse) | `D03` | Volume projection beyond 100M rows |
