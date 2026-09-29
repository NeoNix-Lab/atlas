# Capability DAG

**Status:** CANONICAL BASELINE — Wave 0 Planning  
**Repository:** `Sentiment`

This document defines the strict Directed Acyclic Graph (DAG) of dependencies across all atomic capabilities in the `Sentiment` engine.

## Planning Model & Inventory

```text
TOTAL_ATOMS                     = 25
CLASSIFIED_ATOMS                = 25
SEMANTIC_FROZEN_OR_RESOLVED     = 22 / 25 (88.0%)
OPEN_BLOCKING                   = 2 (A04, E01)
OPEN_DEFERABLE                  = 1 (E05)
IMPLEMENTATION_COMPLETE         = 0 / 25 (Wave 0 start)
```

Decision States:
- `FROZEN`: Accepted semantic contract/schema.
- `RESOLVED`: Architecture & ownership accepted; implementation pending.
- `OPEN_BLOCKING`: Must be resolved before the dependent branch can be implemented.
- `OPEN_DEFERABLE`: Explicitly postponed until prerequisite proof or live feed exists.

---

## Architecture Tracks

* **Track A**: Ingestion & Scraping Data Plane
* **Track B**: Deterministic Processing & Lineage
* **Track C**: Semantic AI (TypeSafe Jev)
* **Track D**: Cross-Modal Feature Store & Temporal Alignment
* **Track E**: Latent Representation & JEPA Modeling
* **Track F**: Validation, Alpha Proof & quant-platform Integration

---

## Atomic Capability DAG & Acceptance Criteria

### Track A: Ingestion & Scraping Data Plane

#### `A01` Scraper Resilience & Rate-Limit Engine
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** None
- **Unlocks:** `A02`, `A03`, `A04`, `A05`
- **Acceptance Proposition:** Exponential backoff, jitter, proxy routing abstraction, and automated session/cookie refreshment handling 429/403 HTTP codes without process crash.

#### `A02` Social Connector: Reddit
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `A01`
- **Unlocks:** `B01`
- **Acceptance Proposition:** Async poller for r/Bitcoin, r/CryptoCurrency producing raw submission/comment payloads with author, body, title, created_utc.

#### `A03` Social Connector: Telegram
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `A01`
- **Unlocks:** `B01`
- **Acceptance Proposition:** Client collecting messages from curated public crypto news & analyst channels using MTProto or public web previews.

#### `A04` Social Connector: X / Twitter
- **Decision State:** `OPEN_BLOCKING` (DG-A) | **Impl State:** `MISSING`
- **Dependencies:** `A01`
- **Unlocks:** `B01`
- **Acceptance Proposition:** Harvester collecting cashtag `$BTC` and related tweets under bounded proxy cost, handling rate limits safely.

#### `A05` News & Regulatory Feed Harvester
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `A01`
- **Unlocks:** `B01`
- **Acceptance Proposition:** Poller for RSS feeds (CoinDesk, Cointelegraph, The Block, SEC, CFTC, Fed) + Trafilatura article body extraction.

#### `A06` On-Chain Bitcoin Mempool & Flow Monitor
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** None
- **Unlocks:** `D02`
- **Acceptance Proposition:** Async ingestion of median mempool fee rates, unconfirmed tx count, and whale transaction alerts ($>100$ BTC).

#### `A07` Derivatives Microstructure Monitor
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** None
- **Unlocks:** `D02`
- **Acceptance Proposition:** WebSocket connector capturing Binance/Bybit BTCUSDT Perpetual Funding Rate, Open Interest, and Liquidation cascades.

---

### Track B: Deterministic Processing & Lineage

#### `B01` WORM Raw Storage Tier
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** None
- **Unlocks:** `B02`, `B04`
- **Acceptance Proposition:** Append-only persistence storing raw unparsed payloads partitioned by source and date, indexed by SHA-256 payload digest.

#### `B02` High-Throughput Regex Engine
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `B01`
- **Unlocks:** `B03`
- **Acceptance Proposition:** Pre-compiled regex suite executing $< 200\mu s$ per payload; extracts BTC entity mentions, filters spam signatures (giveaways, airdrop bots, referral schemes).

#### `B03` Anti-Sybil & Duplicate Filter
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `B02`
- **Unlocks:** `B04`
- **Acceptance Proposition:** Locality-sensitive hashing (MinHash/SimHash) to eliminate duplicate copy-paste tweets and spam botnet campaigns across social feeds.

#### `B04` Canonical Document Contract
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `B01`, `B03`
- **Unlocks:** `C01`, `D01`
- **Acceptance Proposition:** Strict Pydantic model enforcing immutable IDs, source origin, dual timestamping (`published_at` vs `observed_at`), clean text, and extracted entities.

---

### Track C: Semantic AI (TypeSafe Jev)

#### `C01` Jev Schema & Questions Contract
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `B04`
- **Unlocks:** `C02`
- **Acceptance Proposition:** Formal TypeSafe questions definition containing `Noul` (binary relevance/FUD), `Choice` (polarity), and `Score` (impact/credibility).

#### `C02` Jev Async Gateway & Dispatcher
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `C01`
- **Unlocks:** `C03`
- **Acceptance Proposition:** Non-blocking async client managing API token bucket, batch evaluation requests, retries, and local caching of responses.

#### `C03` Semantic Feature Vectorization
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `C02`
- **Unlocks:** `D01`, `D02`
- **Acceptance Proposition:** Deterministic transformation mapping Jev outputs into normalized float columns $[0.0, 1.0]$ and $[-1.0, 1.0]$.

---

### Track D: Cross-Modal Feature Store & Temporal Alignment

#### `D01` Time-Window Resampler (Point-in-Time)
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `B04`, `C03`
- **Unlocks:** `D02`
- **Acceptance Proposition:** Rolling resampler aggregating documents into non-leaking intervals ($1m, 5m, 15m, 1h$) strictly keyed on `observed_at`.

#### `D02` Cross-Modal Feature Matrix
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `A06`, `A07`, `C03`, `D01`
- **Unlocks:** `D03`, `E02`
- **Acceptance Proposition:** Unified tabular row per time bucket combining Jev sentiment aggregates, social volume, mempool pressure, funding rates, and open interest delta.

#### `D03` Canonical Parquet Materialization
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `D02`
- **Unlocks:** `F01`, `F03`
- **Acceptance Proposition:** Partitioned Parquet storage format supporting high-speed scans via DuckDB and PyArrow.

---

### Track E: Latent Representation & JEPA Modeling

#### `E01` JEPA Target State Formulation
- **Decision State:** `OPEN_BLOCKING` (DG-C) | **Impl State:** `MISSING`
- **Dependencies:** `D02`
- **Unlocks:** `E02`, `E03`
- **Acceptance Proposition:** Formal mathematical contract defining the future market target vector (e.g. forward return distribution + realized volatility + liquidation volume).

#### `E02` Multimodal Context Encoder
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `E01`, `D02`
- **Unlocks:** `E03`
- **Acceptance Proposition:** Temporal neural network (Transformer/MLP-Mixer) encoding a historical context window of cross-modal features into latent space $s_t \in \mathbb{R}^d$.

#### `E03` JEPA Target Encoder & Predictor
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `E01`, `E02`
- **Unlocks:** `E04`
- **Acceptance Proposition:** Architecture featuring an Exponential Moving Average (EMA) target encoder and predictor network optimizing latent prediction loss without representational collapse.

#### `E04` Self-Supervised JEPA Pre-training Loop
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `E03`
- **Unlocks:** `E05`, `F01`
- **Acceptance Proposition:** Offline training pipeline converging on historical test splits with non-trivial latent variance (VICReg variance/covariance criteria verified).

#### `E05` Online JEPA Latent Inference
- **Decision State:** `OPEN_DEFERABLE` | **Impl State:** `MISSING`
- **Dependencies:** `E04`
- **Unlocks:** `F03`
- **Acceptance Proposition:** Real-time streaming evaluator updating latent state representations upon arrival of each new temporal bucket.

---

### Track F: Validation, Alpha Proof & Integration

#### `F01` Information Coefficient (IC) Engine
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `D03`, `E04`
- **Unlocks:** `F02`
- **Acceptance Proposition:** Quantitative module evaluating Spearman rank correlation and p-values between features/embeddings and future BTC return horizons.

#### `F02` Divergence Signal Engine
- **Decision State:** `RESOLVED` | **Impl State:** `MISSING`
- **Dependencies:** `F01`
- **Unlocks:** `F03`
- **Acceptance Proposition:** Algorithmic detector identifying extreme dislocations between crowd sentiment and underlying order flow / price action.

#### `F03` quant-platform Gateway Adapter
- **Decision State:** `FROZEN` | **Impl State:** `MISSING`
- **Dependencies:** `D03`, `F01`
- **Unlocks:** Downstream production trading in `quant-platform`
- **Acceptance Proposition:** Zero-copy Arrow IPC / Parquet export adapter matching `quant-platform`'s `FeatureArtifact` contract.
