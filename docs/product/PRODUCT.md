# PRODUCT.md

**Project:** Atlas (BTC Multi-Modal Sentiment & Latent Representation Engine)  
**Status:** CANONICAL BASELINE v1.0 — Product Definition  
**Target:** High-throughput, multi-modal Bitcoin market sentiment engine with point-in-time correctness, deterministic regex pre-filtering, TypeSafe Jev semantic typing, JEPA latent representation, and CLI operator control.  
**Canonical Codebase:** `atlas` (Repository: `Sentiment`)  
**CLI Tool:** `atlas`  
**Downstream Consumer & Arbitrator:** `quant-platform` (Feature Store, Alpha Research & Execution)

---

## 1. Product Mission

`Atlas` is the authoritative engine for harvesting, parsing, semantically classifying, and fusing market-wide sentiment signals for Bitcoin (BTC).

The platform transforms unstructured, noisy, and hostile external data streams (social media, mainstream news, regulatory releases, mempool velocity, and derivatives positioning) into temporally rigorous, quantitative features.

### Core Lifecycle Responsibilities:
1. **Multi-Channel Harvesting (L0)**: Ingest raw payloads from social platforms (Reddit, Telegram, and bounded X/Twitter), media (crypto-native, financial wire, regulatory agencies), and market feeds (mempool fees, funding rates, open interest) via resilient asynchronous pollers.
2. **Line-Rate Noise Rejection (L1)**: Filter spam botnets, airdrop shills, and duplicate copy-pasta deterministically using a high-throughput compiled Regex engine before consuming any AI inference budget.
3. **Strongly-Typed Semantic Scoring (L2)**: Extract structured sentiment polarity, credibility standing, and urgency using TypeSafe AI's **Jev** non-generative System-One engine (`Noul`, `Choice`, `Score`).
4. **Multi-Modal Feature Resampling (L3)**: Resample and fuse text sentiment vectors with on-chain mempool pressure and derivatives microstructure into sliding point-in-time windows (1m, 5m, 15m, 1h).
5. **Self-Supervised Latent Representation (L4)**: Learn joint predictive market state transitions using a **JEPA** (Joint Embedding Predictive Architecture) context-target network, bypassing autoregressive token generation.
6. **Feature Artifact Export**: Deliver strictly typed, point-in-time Parquet datasets conforming directly to `quant-platform`'s `FeatureArtifact v1` specification.
7. **Single Operator Interface (CLI v1)**: Provide a comprehensive Command Line Interface (`atlas`) as the sole v1 human-system interaction point for daemon management, backfill execution, pipeline probing, budget protection, and feature export.

---

## 2. Invariants & Product Principles

### 2.1 Separation of Concerns with `quant-platform`
* **`Atlas` is a Feature Producer**: It owns data harvesting, text sanitization, semantic classification, multimodal alignment, representation learning, and intrinsic data quality validation (non-collapse, schema conformity, spam precision).
* **`quant-platform` is the Alpha Arbitrator**: Statistical validation against market outcomes (Information Coefficient on forward returns, Event Studies, Walk-Forward splits, Purge & Embargo, and Deflated Sharpe Ratio / PBO) belongs exclusively to `quant-platform`. `Atlas` never duplicates trading backtests or price candle calculations.

### 2.2 Absolute Point-in-Time Correctness (Dual-Timestamp Invariant)
Every document and derived feature row enforces two distinct UTC timestamps:
* `published_at`: The self-declared creation time at the origin source.
* `observed_at`: The monotonic system clock timestamp recording when the engine first validated and stored the item.

Any feature calculation or training sample for timestamp $T$ strictly forbids data where $\text{observed\_at} > T$, eliminating lookahead leakage by construction.

### 2.3 Cascading Funnel Architecture (Cost & Noise Suppression)
Compute cost and noise are minimized as early as possible in the execution path:
* **Stage 1 (Regex L1)**: Drops $\ge 75\%$ of raw social chatter at sub-millisecond line-rate with zero AI compute cost.
* **Stage 2 (TypeSafe Jev L2)**: Evaluates structured primitives at $\$0.042 / 1\text{M}$ input tokens with zero token generation overhead.
* **Stage 3 (Cross-Modal Fusion L3)**: Fuses text vectors with free real-time on-chain and derivatives feeds.
* **Stage 4 (JEPA L4)**: Predicts latent state transitions without generative hallucinations.

### 2.4 Non-Generative, Typed AI Primitives
The system explicitly rejects free-form conversational LLM prompts. All semantic understanding is constrained to TypeSafe Jev typed outputs:
* `Noul`: Binary probabilities $[0.0, 1.0]$.
* `Choice`: Constrained categorical classifications with predefined criteria.
* `Score`: Ordinal ranked tiers.

### 2.5 CLI-First Operational Control (v1 Boundary)
For version 1.0, the primary operator access point is strictly the Command Line Interface (`atlas`). No web GUI or browser runtime is part of the v1 scope. All monitoring, probing, daemon control, budget guardrails, and data exports are driven via CLI commands and declarative configuration (`atlas.toml`).

### 2.6 WORM Raw Tier Immutability
All harvested payloads (raw JSON, HTML bodies, wire responses) are stored in an append-only Write-Once-Read-Many (WORM) raw tier, content-addressed by SHA-256 hashes. If parsing regexes or semantic prompts change, historical data can be deterministically replayed.

---

## 3. Downstream Consumers

1. **`quant-platform` Feature Engine & Strategy Runtimes**: Consumes exported Parquet feature tables for cross-validation, hypothesis testing, and quantitative trading signals.
2. **System Operator**: Controls and inspects the pipeline through the `atlas` CLI tool and configuration files.

---

## 4. Non-Goals for Version 1.0

1. **No Web GUI or Browser Dashboard**: A visual dashboard is explicitly deferred beyond v1. All v1 interactions are headless and CLI-driven.
2. **No Direct Trading Execution**: `Atlas` does not connect to exchange trading accounts or execute orders.
3. **No Internal Backtesting Engine**: `Atlas` does not calculate Sharpe ratios, simulated PnL, or strategy returns against price candles. That responsibility belongs strictly to `quant-platform`.
4. **No Free-Form Generative Chat**: The engine never generates discursive prose or explanatory summaries.
5. **No Unfiltered Social Firehose Storage**: Raw social media posts that fail the Regex spam filter are dropped immediately from persistent canonical storage.

---

## 5. Technical Success Metrics

1. **Line-Rate Throughput**: Regex pre-filter executes at $> 5,000$ documents/sec per CPU core.
2. **Semantic Latency & Cost**: Jev batched evaluation latency $< 500$ ms; monthly inference cost bounded under **€25/month**.
3. **Intrinsic Feature Quality**:
   * Jev Schema Conformity: $100\%$ valid typed records (zero missing fields, zero parsing failures).
   * JEPA Latent Representation: Non-collapsing state representation verified via VICReg variance criterion ($\text{Var}(z_j) \ge 1.0$) and low cross-dimensional covariance.
4. **Point-in-Time Compliance**: $100\%$ of exported feature rows adhere strictly to $\text{observed\_at} \le T_{\text{window\_close}}$.
