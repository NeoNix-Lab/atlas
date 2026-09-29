# Atlas Roadmap

**Project:** Atlas (BTC Multi-Modal Sentiment & Latent Representation Engine)  
**Status:** CANONICAL BASELINE v1.0  
**Authority:** Defines the macro progression across Waves 0 through 5, Decision Gates (DG-A to DG-D), and verifiable Golden E2E Proofs. The atomic dependency model is tracked in [`CAPABILITY_DAG.md`](CAPABILITY_DAG.md).

---

## 1. Planning Layers

```text
ROADMAP.md          = Macro product progression, wave milestones, and golden proofs
CAPABILITY_DAG.md   = Atomic capability dependencies and acceptance propositions
CAPABILITY_MAP.md   = Compact current-state inventory across all 28 atoms
OPEN_DECISIONS.md   = Unresolved decision gates (DG-A to DG-D)
ADRs + Contracts    = Authoritative semantic specifications and schemas
SCOPE.md            = Active bounded mutation scope for the current wave
```

---

## 2. Macro Waves (0 – 5)

```text
Wave 0: Governance, Contracts & Data Schemas (Foundation) [COMPLETE]
   │
   ▼
Wave 1: Ingestion & Deterministic Line-Rate Engine (Scrapers + Regex L1)
   │
   ▼
Wave 2: Semantic Typing (Jev L2) & Operator Control Plane (CLI v1)
   │
   ▼
Wave 3: Multi-Modal Fusion & Point-in-Time Feature Store (Parquet L3)
   │
   ▼
Wave 4: Latent Predictive Architecture (JEPA Context/Target Encoders L4)
   │
   ▼
Wave 5: quant-platform Feature Gateway & Divergence Signals
```

---

### Wave 0: Governance, Contracts & Schemas Foundation
* **Status:** **COMPLETE**
* **Atoms Credited:** `B04` (`CanonicalDocument`), `C01` (`JevEvaluationContract`), `C03` (`SemanticVector`).
* **Deliverables:**
  * System documentation baseline (`PRODUCT.md`, `CAPABILITY_MAP.md`, `CAPABILITY_DAG.md`, `ROADMAP.md`).
  * Target architecture specification (`TARGET_ARCHITECTURE.md`).
  * Frozen contracts (`CANONICAL_DOCUMENT.md`, `JEV_EVALUATION_CONTRACT.md`).
  * Pydantic schema implementations in `src/atlas/contracts/` verified with passing unit tests in `tests/test_contracts.py`.

---

### Wave 1: Ingestion & Deterministic Line-Rate Engine
* **Status:** **READY TO OPEN**
* **Focus:** Build resilient harvesting for Reddit, Telegram, Crypto/Macro News, On-Chain Mempool/Whale streams, and resolve Twitter/X sourcing strategy (DG-A). Implement line-rate compiled Regex engine to drop $\ge 75\%$ of social spam at zero compute cost.
* **Atoms Activated:** `A01`, `A02`, `A03`, `A04` (gated on DG-A), `A05`, `A06` (dual-stream), `A07`, `B01`, `B02`, `B03`.
* **Golden Proof:** `WAVE1_GOLDEN_E2E_DETERMINISTIC_INGESTION.md`
  * Demonstrates end-to-end ingestion from 4 active sources into local WORM storage (`B01`).
  * Proves $> 5,000$ docs/sec line-rate Regex throughput and verified $\ge 75\%$ spam rejection on a frozen 1,000-message test corpus without losing legitimate BTC news.

---

### Wave 2: Semantic Typing & Operator Control Plane (CLI v1)
* **Status:** **PLANNED**
* **Focus:** Integrate `typesafe-sdk`, implement the async Jev client gateway with concurrency control and local response caching. Deliver the canonical `atlas` CLI operator tool and hard budget circuit breakers.
* **Atoms Activated:** `C02`, `G01`, `G02`, `G03`, `G04`.
* **Golden Proof:** `WAVE2_GOLDEN_E2E_JEV_AND_CLI_OPERATOR.md`
  * Demonstrates zero-failure, deterministic typed extraction (`Noul`, `Choice`, `Score`) on 5,000 clean documents across text sentiment and on-chain capital intent.
  * Proves `atlas probe --text "..."` interactive tracing and verifies the `G04` circuit breaker automatically halts calls when the test daily budget cap is reached.

---

### Wave 3: Multi-Modal Fusion & Point-in-Time Feature Store
* **Status:** **PLANNED**
* **Focus:** Build the sliding-window resampler enforcing strict anti-lookahead watermarks. Align text sentiment vectors with continuous mempool fee rates, on-chain whale intent scores, and Binance/Bybit Funding Rate and Open Interest delta into partitioned Parquet feature tables.
* **Atoms Activated:** `D01`, `D02`, `D03`.
* **Golden Proof:** `WAVE3_GOLDEN_E2E_MULTIMODAL_FUSION.md`
  * Verifies point-in-time invariant: zero rows with $\text{observed\_at} > T_{\text{close}}$ exist in any materialized feature bucket.
  * Proves high-speed DuckDB queries over partitioned Parquet tables across 1m, 5m, 15m, and 1h resolutions.

---

### Wave 4: Latent Predictive Architecture (JEPA)
* **Status:** **PLANNED**
* **Focus:** Resolve DG-C (Target State Formulation). Implement the Multimodal Context Encoder, EMA Target Encoder, and Latent Predictor network. Build the self-supervised training loop and prove non-collapse.
* **Atoms Activated:** `E01` (gated on DG-C), `E02`, `E03`, `E04`, `F01`.
* **Golden Proof:** `WAVE4_GOLDEN_E2E_JEPA_REPRESENTATION.md`
  * Proves self-supervised convergence on historical feature splits.
  * Proves the non-collapse theorem: $\text{Var}(z_j) \ge 1.0$ across all embedding dimensions and low cross-covariance, ensuring meaningful latent representations of market dynamics.

---

### Wave 5: quant-platform Feature Gateway & Divergence Signals
* **Status:** **PLANNED**
* **Focus:** Implement the rule-based Divergence Signal Engine (crowd sentiment vs smart money capital flow dislocations). Build the zero-copy Arrow IPC and partitioned Parquet export adapter strictly conforming to `quant-platform`'s `FeatureArtifact v1` (`ADR-0034`).
* **Atoms Activated:** `F02`, `F03`.
* **Golden Proof:** `WAVE5_GOLDEN_E2E_QUANT_PLATFORM_GATEWAY.md`
  * Proves end-to-end delivery of an export package to `quant-platform`.
  * Demonstrates successful ingestion and inspection of Atlas feature sets inside `quant-platform`'s research engine.

---

## 3. Decision Gate Family (DG)

| Gate ID | Area | Proposition | Blocking For | Trigger Condition |
|---|---|---|---|---|
| **DG-A** | Ingestion | Social Connector: X / Twitter sourcing strategy (Syndication endpoints vs Guest scrapers vs Proxy pool) | `A04` | Selection of sustainable, low-cost harvesting mechanism bounded under €20/mo proxy spend |
| **DG-B** | Temporal | Late-arrival re-indexing and window closure watermarking without lookahead leakage | `D01` | Specification of watermark latency threshold $\Delta_{\text{watermark}}$ |
| **DG-C** | Representation | Mathematical formulation of JEPA Target State $y_{t+\Delta t}$ (Forward log returns, realized volatility, and liquidation volume) | `E01` | Formal mathematical specification of the prediction target vector |
| **DG-D** | Storage | Feature Store partitioning scheme and DuckDB indexing scale | `D03` | Volume projection beyond 50M feature rows |
