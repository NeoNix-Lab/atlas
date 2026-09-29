# Capability DAG

**Project:** Atlas (BTC Multi-Modal Sentiment & Latent Representation Engine)  
**Status:** CANONICAL BASELINE v1.0  
**Authority:** Defines the authoritative Directed Acyclic Graph (DAG) of dependencies, acceptance propositions, decision gates, and execution unlocks across all capability atoms.

---

## 1. Planning Model & Audited Inventory

```text
TOTAL_ATOMS                     = 28
CLASSIFIED_ATOMS                = 28
SEMANTIC_FROZEN_OR_RESOLVED     = 25 / 28 (89.3%)
OPEN_BLOCKING                   = 2 (A04: Twitter Sourcing, E01: JEPA Target State)
OPEN_DEFERABLE                  = 1 (E05: Online Latent Streaming)
IMPLEMENTATION_COMPLETE         = 3 / 28 (B04, C01, C03 verified in Wave 0)
IMPLEMENTATION_MISSING          = 25 / 28 (Wave 1 start)
```

Decision States:
- `FROZEN`: Accepted semantic contract and immutable schema definition.
- `RESOLVED`: Architecture, ownership, and proposition decided; implementation pending.
- `OPEN_BLOCKING`: Must be resolved via Decision Gate (DG) before dependent implementation is authorized.
- `OPEN_DEFERABLE`: Explicitly postponed until prerequisite proof or live feed exists.

Implementation States: `COMPLETE | PARTIAL | MISSING`.

---

## 2. Architecture Tracks & Spines

```text
Track A — Ingestion & Harvesting Data Plane (A01 - A07)
Track B — Deterministic Processing & Lineage (B01 - B04)
Track C — Semantic AI: TypeSafe Jev (C01 - C03)
Track D — Cross-Modal Feature Store & Alignment (D01 - D03)
Track E — Latent Representation & JEPA Modeling (E01 - E05)
Track F — Intrinsic Quality & quant-platform Gateway (F01 - F03)
Track G — Operator Control Plane: CLI v1 (G01 - G04)
```

---

## 3. Atomic Capability Inventory & Dependency DAG

### Track A: Ingestion & Harvesting Data Plane

#### `A01` Scraper Resilience & Rate-Limit Engine
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** None
- **Unlocks:** `A02`, `A03`, `A04`, `A05`
- **Acceptance Proposition:** Exponential backoff with jitter, session/cookie rotation, and proxy interface abstraction handling HTTP 429/403 without pipeline crash.

#### `A02` Social Connector: Reddit
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `A01`
- **Unlocks:** `B01`
- **Acceptance Proposition:** Async poller collecting submissions and top comments from r/Bitcoin and r/CryptoCurrency via RSS/public endpoints.

#### `A03` Social Connector: Telegram
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `A01`
- **Unlocks:** `B01`
- **Acceptance Proposition:** Ingestion client collecting text and media captions from curated public crypto news/analyst channels via MTProto or web previews.

#### `A04` Social Connector: X / Twitter
- **Decision State:** `OPEN_BLOCKING` (DG-A) | **Impl State:** `MISSING`
- **Dependencies:** `A01`
- **Unlocks:** `B01`
- **Acceptance Proposition:** Sourcing strategy resolved per DG-A; collects cashtag `$BTC` mentions under strict token/proxy cost bounds.

#### `A05` News & Regulatory Feed Harvester
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `A01`
- **Unlocks:** `B01`
- **Acceptance Proposition:** Poller for RSS feeds (CoinDesk, Cointelegraph, Decrypt, The Block, SEC, CFTC, Fed) + Trafilatura full article text extractor.

#### `A06` On-Chain Bitcoin Mempool & Capital Flow Monitor
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** None
- **Unlocks:** `B01` (for discrete capital events), `D02` (for continuous metrics)
- **Acceptance Proposition:** Dual-stream ingestion:
  1. *Continuous*: Emits median mempool fee rates (sat/vB) and fee velocity directly to `D02`.
  2. *Discrete Events*: Serializes whale transactions ($>100$ BTC), exchange inflows/outflows, and dormant address movements as `CanonicalDocument` payloads to `B01` for Jev semantic typing.

#### `A07` Derivatives Microstructure Monitor
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** None
- **Unlocks:** `D02`
- **Acceptance Proposition:** Real-time WebSocket connector capturing Binance and Bybit BTCUSDT Perpetual Funding Rates, Open Interest delta, and Liquidation volume.

---

### Track B: Deterministic Processing & Lineage

#### `B01` WORM Raw Storage Tier
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `A02`, `A03`, `A04`, `A05`, `A06`
- **Unlocks:** `B02`
- **Acceptance Proposition:** Append-only local storage storing raw gzipped payloads (`data/raw/<source>/YYYY-MM-DD/<hash>.json.gz`) with SHA-256 payload digest.

#### `B02` High-Throughput Regex Engine
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `B01`
- **Unlocks:** `B03`
- **Acceptance Proposition:** Compiled regex suite executing $< 200 \mu s$ per document; extracts `$BTC` entities and drops $\ge 75\%$ spam (giveaways, airdrop bot templates, referral links).

#### `B03` Anti-Sybil & Duplicate Filter
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `B02`
- **Unlocks:** `B04`
- **Acceptance Proposition:** MinHash/SimHash near-duplicate detector dropping botnet copy-pasta across social feeds within a sliding 60-minute window.

#### `B04` Canonical Document Contract
- **Decision State:** `FROZEN` | **Impl State:** `COMPLETE`
- **Dependencies:** `B01`, `B03`
- **Unlocks:** `C01`, `D01`
- **Acceptance Proposition:** Pydantic model enforcing immutable IDs, source origin, UTC dual-timestamping (`published_at` vs `observed_at`), clean text, and extracted entities. *Verified in Wave 0 unit tests.*

---

### Track C: Semantic AI (TypeSafe Jev)

#### `C01` Jev Schema & Questions Contract
- **Decision State:** `FROZEN` | **Impl State:** `COMPLETE`
- **Dependencies:** `B04`
- **Unlocks:** `C02`
- **Acceptance Proposition:** Strongly-typed question definitions (`Noul`, `Choice`, `Score`) covering text sentiment polarity, credibility, urgency, and on-chain capital flow intent. *Verified in Wave 0.*

#### `C02` Jev Async Gateway & Dispatcher
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `C01`, `G04`
- **Unlocks:** `C03`
- **Acceptance Proposition:** Non-blocking async client managing API token bucket, batch evaluation requests, retries, and local response caching against `api.typesafe.ai`.

#### `C03` Semantic Feature Vectorization
- **Decision State:** `RESOLVED` | **Impl State:** `COMPLETE`
- **Dependencies:** `C02`
- **Unlocks:** `D01`, `D02`
- **Acceptance Proposition:** Deterministic factory mapping raw Jev outputs into normalized float columns $[0.0, 1.0]$ and $[-1.0, 1.0]$ (`SemanticVector`). *Verified in Wave 0.*

---

### Track D: Cross-Modal Feature Store & Temporal Alignment

#### `D01` Time-Window Resampler (Point-in-Time)
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `B04`, `C03`
- **Unlocks:** `D02`
- **Acceptance Proposition:** Rolling resampler aggregating documents into non-leaking intervals ($1m, 5m, 15m, 1h$) strictly keyed on `observed_at \le T_{\text{close}}`.

#### `D02` Cross-Modal Feature Matrix
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `A06`, `A07`, `C03`, `D01`
- **Unlocks:** `D03`, `E02`
- **Acceptance Proposition:** Unified tabular row per time bucket combining Jev sentiment aggregates, social volume, mempool pressure, whale intent scores, funding rates, and open interest delta.

#### `D03` Canonical Parquet Materialization
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `D02`
- **Unlocks:** `F01`, `F03`
- **Acceptance Proposition:** Partitioned Parquet feature tables partitioned by resolution and date (`data/features/resolution=<window>/year=YYYY/month=MM/part-*.parquet`).

---

### Track E: Latent Representation & JEPA Modeling

#### `E01` JEPA Target State Formulation
- **Decision State:** `OPEN_BLOCKING` (DG-C) | **Impl State:** `MISSING`
- **Dependencies:** `D02`
- **Unlocks:** `E02`, `E03`
- **Acceptance Proposition:** Formal mathematical contract defining the future market target vector $y_{t+\Delta t}$ (forward price volatility, log return distribution, and liquidation volume).

#### `E02` Multimodal Context Encoder
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `E01`, `D02`
- **Unlocks:** `E03`
- **Acceptance Proposition:** Temporal neural network (Transformer or MLP-Mixer) encoding a historical context window of cross-modal features into latent space $s_t \in \mathbb{R}^d$.

#### `E03` JEPA Target Encoder & Predictor
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `E01`, `E02`
- **Unlocks:** `E04`
- **Acceptance Proposition:** Dual-encoder architecture with an Exponential Moving Average (EMA) target encoder and a predictor network optimizing latent prediction loss without collapse.

#### `E04` Self-Supervised JEPA Pre-training Loop
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `E03`
- **Unlocks:** `E05`, `F01`
- **Acceptance Proposition:** Offline training pipeline converging on historical test splits with non-trivial latent variance (VICReg variance/covariance criteria verified).

#### `E05` Online JEPA Latent Inference
- **Decision State:** `OPEN_DEFERABLE` | **Impl State:** `MISSING`
- **Dependencies:** `E04`
- **Unlocks:** `F03`
- **Acceptance Proposition:** Streaming evaluator updating latent state representations upon completion of each temporal feature bucket.

---

### Track F: Intrinsic Quality & quant-platform Gateway

#### `F01` Intrinsic Representation & Non-Collapse Proof
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `E04`
- **Unlocks:** `F02`, `F03`
- **Acceptance Proposition:** Quantitative validation script proving that JEPA latent vectors satisfy $\text{Var}(z_j) \ge 1.0$ across all dimensions and exhibit low covariance, confirming non-collapsed representations.

#### `F02` Divergence Signal Engine
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `D02`, `F01`
- **Unlocks:** `F03`
- **Acceptance Proposition:** Rule-based algorithmic detector flagging severe dislocations between crowd emotion (social sentiment) and smart money flow (on-chain whale intent + derivatives positioning).

#### `F03` quant-platform Feature Gateway
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `D03`, `F01`, `F02`
- **Unlocks:** Downstream production trading & alpha research in `quant-platform`
- **Acceptance Proposition:** Export adapter generating partitioned Parquet datasets strictly conforming to `quant-platform`'s `FeatureArtifact v1` specification (`ADR-0034`).

---

### Track G: Operator Control Plane (CLI v1)

#### `G01` Configuration Engine (`atlas.toml`)
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** None
- **Unlocks:** `G02`, `G03`, `G04`
- **Acceptance Proposition:** Pydantic-backed declarative configuration parser for `atlas.toml` and `.env`, validating source switches, polling intervals, and dollar budget limits.

#### `G02` CLI Runtime Controller (`atlas`)
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `G01`
- **Unlocks:** `G03`
- **Acceptance Proposition:** Click/Rich CLI providing `atlas daemon start/stop/status`, `atlas backfill`, and `atlas export` commands with graceful signal handling (SIGINT/SIGTERM).

#### `G03` Pipeline Probe & Diagnostic Tool
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `B02`, `C02`, `G02`
- **Unlocks:** None (Operational tool)
- **Acceptance Proposition:** CLI command (`atlas probe --text "..."`) that executes a dry-run trace across Regex L1 and Jev L2, rendering intermediate matches, tokens, and the resulting `SemanticVector` in a Rich terminal table.

#### `G04` Budget Guardrail & Circuit Breaker
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `G01`
- **Unlocks:** `C02`
- **Acceptance Proposition:** State engine tracking daily and monthly USD spend on TypeSafe AI; automatically halts AI calls and engages "Regex-Only" fallback if limits are exceeded.
